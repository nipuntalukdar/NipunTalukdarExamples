from Queue import Queue

READ = 1
WRITE = 2
UNLOCK = 3
class store:
    locks = {}
    q = Queue()

    @classmethod
    def enque_lock(cls, lock, lockmode):
        if lockmode != READ and lockmode != WRITE:
            return False
        if lock not in cls.locks:
            cls.locks[lock] = []
        if lockmode not in cls.locks[lock]:
            cls.locks[lock].append(lockmode)
            q.put(lock)
        return True
    
    @classmethod
    def enque_unlock(cls, lock, lockmode):
        if lockmode != UNLOCK:
            return False
        if lock not in cls.locks:
            cls.locks[lock] = []
        if lockmode not in cls.locks[lock]:
            cls.locks[lock].append(lockmode)
            q.put(lock)
        return True
    
    @classmethod
    def deque_lock(cls, lock, lockmode):
        if lock not in cls.locks:
            return False
        if lockmode not in cls.locks[lock]:
            return False
        cls.locks[lock].remove(lockmode)
        if len(cls.locks[lock]) == 0:
            del cls.locks[lock]
        return True
    
    def run(self):
        while self.keep_running:
            lck = q.get(True, 2)
            lockops = store.locks[lock]
            # send the read or write or unlock operation to server
            # lockclient.lockop(lock, lockops[0])

if __name__ == '__main__':
    store.enque_lock('a', READ)
    store.enque_lock('a', READ)
    store.enque_lock('a', WRITE)
    store.enque_lock('b', READ)
