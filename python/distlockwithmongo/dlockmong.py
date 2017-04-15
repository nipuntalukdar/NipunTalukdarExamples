from threading import Thread, Lock
from time import sleep, time
from datetime import datetime
from pymongo import MongoClient
from uuid import uuid1
import atexit


class DistLockMongo(Thread):
    def __init__(self, host='localhost', port=27017, db='lockdb'):
        Thread.__init__(self)
        self.__mylocks__ = {}
        self.__lock__ = Lock()
        self.__mhost__ = host
        self.__mport__ = port
        self.__mclient__ = MongoClient(host, port)
        db = self.__mclient__[db]
        self.__lockcollection__ = db['lockcols']
        self.__myid__ = uuid1().hex
        self.__keep_running = True

    def __del__(self):
        self.__cleanup()
    
    def __remove_lock__(self, lock, retry=False):
        while True:
            try:
                self.__lockcollection__.delete_one({'_id' : lock, 'owner' : self.__myid__})
                return
            except:
                if not retry:
                    return
                else:
                    sleep(0.1)
   
    def __aquire_lock(self, lock):
        with self.__lock__:
            if lock in self.__mylocks__:
                return True
            try:
                self.__lockcollection__.insert_one({'_id' : lock, 'owner': self.__myid__, 'time' : datetime.utcnow()}) 
                self.__mylocks__[lock] = time() + 10
                return True
            except Exception as e:
                print(e)
                return False

    def stop(self):
        self.__keep_running = False

    def release(self, lock, wait=True):
        with self.__lock__:
            if lock not in self.__mylocks__:
                return
        self.__remove_lock__(lock, wait)
        with self.__lock__:
            del self.__mylocks__[lock]

    def lock(self, lock, maxwait=0):
        wait_till = 0 
        if maxwait > 0:
            wait_till = time() + maxwait
        
        while not self.__aquire_lock(lock):
            if time() >= wait_till:
                return False
            sleep(0.2)
        return True 

    def __cleanup(self):
        with self.__lock__:
            cur_locks = self.__mylocks__.keys()
        for lock in cur_locks:
            print('Releasing {}'.format(lock))
            self.release(lock, False)
        
    def run(self):
        cur_locks = []
        while self.__keep_running:
            with self.__lock__:
                cur_locks = self.__mylocks__.keys()
            for lock in cur_locks:
                try:
                    with self.__lock__:
                        if lock in self.__mylocks__ and self.__mylocks__[lock] < time():
                            self.__mylocks__[lock] = time()
                            print('Updating time for {}'.format(lock))
                        else:
                            continue
                    self.__lockcollection__.update_one({'_id' : lock, 'owner' : self.__myid__,}, 
                        {'$set' : {'time': datetime.utcnow()}})
                    with self.__lock__:
                        if lock in self.__mylocks__:
                            self.__mylocks__[lock] = time() + 10
                except:
                    pass
                if not self.__keep_running:
                    break
            sleep(2)
        self.__cleanup()

dlock = DistLockMongo()
dlock.setDaemon(True)
dlock.start()

@atexit.register
def exithandler():
    dlock.stop()
    sleep(4)

if __name__ == '__main__':
    print(dlock.lock('lock1'))
    print(dlock.lock('lock2'))
    print(dlock.lock('lock3'))
    sleep(60)
