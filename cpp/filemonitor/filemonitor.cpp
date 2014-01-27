#include <sys/inotify.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <iostream>
#include <set>
#include <boost/thread.hpp>
#include "filemonitor.h"

using std::cout;
using std::endl;
using std::set;
using std::cin;

boost::shared_ptr < FileMonitor > FileMonitor::_fmon;

boost::shared_ptr < FileMonitor > FileMonitor::getInstance ()
{
    if (!_fmon)
    _fmon = boost::shared_ptr < FileMonitor > (new FileMonitor ());
    return _fmon;
}

void FileMonitor::wait()
{
    if (_thread)
        pthread_join(_thread, 0);
    _thread = 0;
    if (_thread_worker)
        pthread_join(_thread_worker, 0);
}

FileMonitor::FileMonitor ()
{
    _ifd = inotify_init ();
    _thread = 0;
    _thread_worker = 0;
    _closed = false;
    pthread_rwlock_init (&_rwmutex, 0);
    pthread_create(&_thread, 0, _start, this);    
    pthread_create(&_thread_worker, 0, _startWorker, this);
}

// Non recursive watch
bool FileMonitor::addDirWatch (const string & dir, FileProcessor* fpr)
{
    set <string> files;
    struct stat statbuf;

    if (stat (dir.c_str (), &statbuf) < 0 || !S_ISDIR (statbuf.st_mode)) {
        return false;
    }
    Watch *w = new Watch(dir, files, fpr, true);
    return _queAddRemoveWatch(w);
}

bool FileMonitor::removeWatch (const string & dir)
{
    set <string> files;
    FileProcessor *fpr = 0;
    return _queAddRemoveWatch(new Watch(dir, files, fpr, false));
    
}

//Non recursive only for a set of specified files in the dir
//
bool FileMonitor::addDirWatch (const string & dir, const set<string>& files, FileProcessor* fpr)
{
    struct stat statbuf;
    if (stat (dir.c_str (), &statbuf) < 0 || !S_ISDIR (statbuf.st_mode)) {
        return false;
    }
    Watch *w = new Watch(dir, files, fpr, true);
    return _queAddRemoveWatch(w);
}

bool FileMonitor::_addDirWatch (const string & dir, FileProcessor* fpr)
{
    _wRlock ();
    if (_ifd <= 0)
        return _wRunlock (false);

    if (_watches.find (dir) != _watches.end ())
        return _wRunlock (false);

    int wd = inotify_add_watch (_ifd, dir.c_str (), IN_CREATE | IN_DELETE 
            | IN_MOVED_FROM | IN_MOVE_SELF | IN_DELETE_SELF 
            // | IN_MODIFY 
            | IN_MOVED_TO
            | IN_CLOSE_WRITE );
    if (wd < 0)
        return _wRunlock (false);
    _watches[dir] = new FileProcessorWatch(wd, fpr);
    _watches_rev_look[wd] = dir;
    return _wRunlock (true);
}

//Interseted only in a list of files, nonrecursive
bool FileMonitor::_addDirWatch (const string & dir, const set <string>& filestowatch,
        FileProcessor* fpr )
{
    _wRlock ();
    if (_ifd <= 0)
        return _wRunlock (false);

    if (_watches.find (dir) != _watches.end ())
        return _wRunlock (false);

    int wd = inotify_add_watch (_ifd, dir.c_str (), IN_CREATE | IN_DELETE 
            | IN_MOVED_FROM | IN_MOVE_SELF | IN_MODIFY | IN_MOVED_TO
            | IN_CLOSE_WRITE | IN_DELETE_SELF);
    if (wd < 0)
        return _wRunlock (false);
    _watches[dir] = new FileProcessorWatch(wd, fpr);
    _watches_rev_look[wd] = dir;
    _interested_files[dir] = filestowatch;
    return _wRunlock (true);
}

bool FileMonitor::_removeWatch (const string & dir)
{
    _wRlock ();
    if (_ifd <= 0)
        return _wRunlock (false);

    unordered_map < string, FileProcessorWatch* >::iterator it = _watches.find (dir);
    if (_watches.end () == it)
        return _wRunlock (false);
    _interested_files.erase(dir);

    inotify_rm_watch (_ifd, it->second->getWatchDescriptor());
    _watches_rev_look.erase(it->second->getWatchDescriptor());
    delete it->second;
    _watches.erase(it);

    return _wRunlock (true);
}

bool FileMonitor::_notInterested(const void *data)
{
   const inotify_event *event = static_cast< const inotify_event *>(data);
   unordered_map<int, string> :: iterator it = _watches_rev_look.find(event->wd);
   if (_watches_rev_look.end() == it)
       return true;
   cout << "Came here 3 \n";

   if (event->mask & IN_MOVE_SELF || event->mask & IN_DELETE_SELF) {
        // One of the watched directory is moved or deleted
        // Treat move also as delete, 
        string removeddir = it->second;
        unordered_map<string, FileProcessorWatch *>:: iterator fit = _watches.find(removeddir);
        if (_watches.end() != fit) {
            fit->second->delegateEvent(removeddir, "", FILE_MONITOR_REMOVED_WATCH); 
            delete fit->second;
            _watches.erase(fit);
        }
        inotify_rm_watch(_ifd, event->wd); 
       _watches_rev_look.erase(event->wd);
       return true;
   }
   
   unordered_map<string, set<string> > :: iterator it2 
       = _interested_files.find(it->second);

   if (it2 != _interested_files.end()) {
        if (it2->second.find(event->name) == it2->second.end())
            return true;
   }
   return false;
}

const string& FileMonitor::_getWatchDir(int wd) const
{
    static string never_returned = "";

    unordered_map<int, string> ::const_iterator it = _watches_rev_look.find(wd);

    if (_watches_rev_look.end() != it) {
        return it->second; 
    }
    return never_returned;
}


bool FileMonitor::_handleMove(const void *data)
{
    const inotify_event *event = static_cast<const inotify_event *>(data);
    FileEventType etype = FILE_DELETED;

    //If moved to, treat is as a new file
    if (event->mask & IN_MOVED_TO) 
        etype = FILE_CREATED;

    int wd = event->wd;
    return _watches[ _watches_rev_look[wd] ]->delegateEvent(_getWatchDir(wd), 
            event->name , etype);

    
}

bool FileMonitor::_handleWrite(const void *data)
{
    const inotify_event *event = static_cast<const inotify_event *>(data);
    int wd = event->wd;
    return _watches[ _watches_rev_look[wd] ]->delegateEvent(_getWatchDir(wd), 
            event->name , FILE_WRITTEN_AND_CLOSED);
}

bool FileMonitor::_handleDelete(const void *data)
{
    const inotify_event *event = static_cast<const inotify_event *>(data);
    int wd = event->wd;
    cout << "Came here 2\n";
    return _watches[ _watches_rev_look[wd] ]->delegateEvent(_getWatchDir(wd), 
            event->name , FILE_DELETED);
}

bool FileMonitor::_queAddRemoveWatch(Watch* watch)
{
    pthread_mutex_lock(&_worklock);
    _add_rm_watches.push_back(watch);
    pthread_mutex_unlock(&_worklock);
    return true;
}

bool FileMonitor::_unqueAddRemoveWatch()
{
    int i = 0;
    pthread_t t1 = pthread_self();
    pthread_mutex_lock(&_worklock);
    while (!_add_rm_watches.empty()) {
        i++;
        Watch *w = _add_rm_watches.front();
        if (w->_add) {
           if (w->_files.empty()){
               _addDirWatch(w->_dir, w->_fpr);
           } else {
               _addDirWatch(w->_dir, w->_files, w->_fpr);
           }
        } else {
            _removeWatch(w->_dir);
        }
        delete w;
        _add_rm_watches.pop_front();
        if (64 == i)//yield time
            break;
    }
    pthread_mutex_unlock(&_worklock);
    return true;
}

void FileMonitor::_cleanUp()
{
    unordered_map < string, FileProcessorWatch* >::iterator it = _watches.begin ();
    while (_watches.end () != it) {
        inotify_rm_watch (_ifd, it->second->getWatchDescriptor());
        delete it->second;
        ++it;
    }
    _watches.clear ();
    close (_ifd);

}

bool FileMonitor::_handleEvent(const void *data)
{
    const inotify_event *event = static_cast<const inotify_event *>(data);
    _rDlock();
    cout << "Came here 1\n";

    if (_notInterested(event))
        return _rDunlock(false);
    
    if (event->mask & IN_DELETE) {
        _handleDelete(event);
    } else if (event->mask & IN_MOVE) {
        _handleMove(event);   
    } else if (event->mask & IN_CLOSE_WRITE) {
        _handleWrite(event);
    } 

    return _rDunlock(true);
    // We don't care any other file events
}


// Stop watch and make the watching thread exit

bool FileMonitor::stopWatch()
{
    _wRlock();
    _cleanUp();
    close(_ifd);
    _closed = true;
    return _wRunlock(true);
}

void* FileMonitor::_startWorker(void *args)
{
    boost::posix_time::milliseconds msecs(250);
    FileMonitor *fmon = static_cast<FileMonitor *> (args);
    while (true) {
        boost::this_thread::sleep(msecs);
        fmon->_unqueAddRemoveWatch();
    }
    return 0;
}

void* FileMonitor::_start(void *args)
{
    int buflen = (sizeof (struct inotify_event) + 32) * 512;
    char events[buflen];
    int length = 0, i = 0;
    struct inotify_event *cur_event = 0;
    FileMonitor *fmon = static_cast<FileMonitor *> (args);
    sigset_t sigset;

    sigemptyset(&sigset);
    sigaddset(&sigset, SIGINT);
    pthread_sigmask(SIG_BLOCK, &sigset, NULL);


    while (true) {
        if (fmon->_closed)
            break;
        length = read (fmon->_ifd, events, buflen);
        if ((length < 0 && EINTR != errno) || (EBADF == errno)){
            break;
        }
        i = 0;
        while (i < length) {
            cur_event = (struct inotify_event *) &events[i];
            fmon->_handleEvent(cur_event);
            i += sizeof(inotify_event) + cur_event->len;
        }
    }
    return 0;
}

void FileMonitor::_rDlock ()
{
    pthread_rwlock_rdlock (&_rwmutex);
}

bool FileMonitor::_rDunlock (bool retval)
{
    pthread_rwlock_unlock (&_rwmutex);
    return retval;
}

void FileMonitor::_wRlock ()
{
    pthread_rwlock_wrlock (&_rwmutex);
}

bool FileMonitor::_wRunlock (bool retval)
{
    pthread_rwlock_unlock (&_rwmutex);
    return retval;
}

int FileMonitor::getCurrentWatches(set<string>& watchdirs)
{
    _rDlock();
    int retval = 0;
    unordered_map<string, FileProcessorWatch *> :: const_iterator it = _watches.begin();
    while (_watches.end() != it) {
        retval++;
        watchdirs.insert(it->first);
        ++it;
    }
    _rDunlock(true);
    return retval;
}

FileMonitor::~FileMonitor ()
{
    _wRlock();
    _cleanUp();
    close(_ifd);
    _closed = true;
    _wRunlock(true);
    pthread_rwlock_destroy (&_rwmutex);
}

FileMonitor::FileProcessorWatch::FileProcessorWatch(int wd, FileProcessor* ptr):
    _wd(wd), _fpr(ptr)
{
}

bool FileMonitor::FileProcessorWatch::delegateEvent(const string& dir, const string& file, FileEventType evtype)
{
    return _fpr->handleFileEvent(dir, file, evtype);
}

int FileMonitor::FileProcessorWatch::getWatchDescriptor()
{
    return _wd;
}

// Below code is for unit tests

class MyFileProcessor : public  FileProcessor
{
    public :
        MyFileProcessor(const char *name)
        {
            _name = name;
        }
        MyFileProcessor()
        {
            _name = "noname";
        }
        bool handleFileEvent(const string& dir, const string& filename, 
                const FileMonitor::FileEventType& etype)
        {
            cout << "Came here \n";
            cout << dir << "/" << filename ;
            if (FileMonitor::FILE_CREATED == etype){
                cout << "Created \n";
            } else if (FileMonitor::FILE_DELETED == etype){
                cout << "Deleted \n";
            } else if (FileMonitor::FILE_WRITTEN_AND_CLOSED == etype){
                cout << "Writtent and closed \n";
            } else if (FileMonitor::FILE_MONITOR_REMOVED_WATCH == etype) {
                cout << "Removed watch for " << dir << endl;
            } 

            return true;
        }
    private:
        string _name;

};

void* waitforthread(void *args)
{
    boost::shared_ptr<FileMonitor> *fmon = static_cast<boost::shared_ptr<FileMonitor> *> (args);
    (*fmon)->wait();
    exit(0);
}

int main ()
{
    boost::shared_ptr < FileMonitor > a = FileMonitor::getInstance ();
    MyFileProcessor *fpr = new MyFileProcessor("HiUnitTest");

    set<string> files;
    files.insert("t1");
    files.insert("t2");
    set<string> dirunderwatch;
    a->addDirWatch("/root/tempdir", files, fpr );
    a->addDirWatch("/home/nipun/work", fpr);
    a->addDirWatch("/home/nipun/test", fpr);
    int i = 0;
    int j = 0;
    int round = 0;
    string choice;
    pthread_t thread;

    pthread_create(&thread, 0, waitforthread, &a);
    boost::posix_time::milliseconds msecs(2500);

    while(1) {
        i = 0;
        j = 0;
        round++;
        boost::this_thread::sleep(msecs);
        cout << "Currently watching below dirs\n" ; 
        dirunderwatch.clear();
        a->getCurrentWatches(dirunderwatch);
        set<string>::iterator it =  dirunderwatch.begin();
        while (it != dirunderwatch.end()) {
            cout << i++ << ": "  << *it  << endl;  
            it++;
        }
        cout << "Which one you want to remove , enter -1 if you don't want to remove" ;
        cin >> choice;
        j = atoi(choice.c_str());
        i = 0;
        it = dirunderwatch.begin();
        for (; it != dirunderwatch.end(); ++it, ++i){
            if (i == j) {
                a->removeWatch(*it);
                break;
            }
        }
        cout << "Any directory you want to add, enter NO if you don't want any";
        choice = "";
        cin >> choice ;
        if (choice.size()) {
            a->addDirWatch(choice, fpr);
        }
        if (round == 200)
        {
            // Stop watch test
            a->stopWatch();

        }
    }
    return 0;
}
