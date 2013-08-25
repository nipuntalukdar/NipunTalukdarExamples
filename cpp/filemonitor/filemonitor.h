#ifndef __FILEMONITOR__
#define __FILEMONITOR__

#include <pthread.h>
#include <string>
#include <set>
#include <deque>
#include <unordered_map>
#include <boost/shared_ptr.hpp>


using std::string;
using std::set;
using std::deque;
using std::unordered_map;


class FileProcessor;

class FileMonitor 
{
    public:
        enum FileEventType
        {
            FILE_CREATED,
            FILE_DELETED,
            FILE_MODIFIED,
            FILE_WRITTEN_AND_CLOSED,
            FILE_MONITOR_REMOVED_WATCH,
            FILE_MONITOR_EXITED
        };
        class FileProcessorWatch
        {
            public:
                FileProcessorWatch(int watchd, FileProcessor* fptr);
                bool delegateEvent(const string& dir, const string& filepath, FileEventType evtype);
                inline int getWatchDescriptor();
            private:
                int _wd;
                FileProcessor* _fpr; 
        };

        struct Watch
        {
            string _dir;
            set<string> _files;
            FileProcessor *_fpr;
            bool _add;
            Watch(const string& dir, const set<string>& files, FileProcessor*& fpr,
                    bool add):
                _dir(dir), _files(files), _fpr(fpr), _add(add)
            {
            }
        };

        static boost::shared_ptr<FileMonitor> getInstance();
        ~FileMonitor();
        bool addDirWatch(const string& dir, FileProcessor* fpr);
        bool addDirWatch(const string& dir, const set<string>& interested_files,
                FileProcessor* fpr);
        bool removeWatch(const string& dir);
        bool startWatch();
        bool stopWatch();
        void wait();
        int getCurrentWatches(set<string>& watchdirs );

    private:

        int _ifd;
        bool _closed;
        pthread_rwlock_t _rwmutex;
        pthread_mutex_t _worklock;
        pthread_t _thread;
        pthread_t _thread_worker;
        unordered_map <string, FileProcessorWatch *> _watches;
        unordered_map <int, string> _watches_rev_look;
        unordered_map <string, set<string> > _interested_files;
        deque <Watch *> _add_rm_watches;
        static boost::shared_ptr<FileMonitor> _fmon;
        FileMonitor();
        FileMonitor(const FileMonitor& );
        FileMonitor& operator=(const FileMonitor&);
        void _rDlock();
        bool _rDunlock(bool whattoret);
        void _wRlock();
        bool _wRunlock(bool whattoret);
        void _cleanUp();
        bool _notInterested(const void* data);
        bool _handleEvent(const void* data);
        bool _handleMove(const void* data);
        bool _handleMod(const void* data);
        bool _handleWrite(const void* data);
        bool _handleDelete(const void* data);
        bool _queAddRemoveWatch(Watch *watch);
        bool _unqueAddRemoveWatch();
        bool _addDirWatch(const string& dir, FileProcessor* fpr);
        bool _addDirWatch(const string& dir, const set<string>& interested_files,
                FileProcessor* fpr);
        bool _removeWatch(const string& dir);
        const string& _getWatchDir(int wd) const;
        static void* _start(void* args);
        static void* _startWorker(void *args);

};

class FileProcessor
{
    public:
        virtual bool handleFileEvent(const string& dir, const string& filename, 
                const FileMonitor::FileEventType& fev_type) = 0;
};

#endif
