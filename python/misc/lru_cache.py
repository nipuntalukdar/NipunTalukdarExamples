from threading import Lock


'''
Class LruCache implements an LRU cache
'''

class LruCache(object):

    def __init__(self, maxobjcount):
        self.__vals = {}
        self.__accessed = []
        self.lock = Lock()
        if maxobjcount < 2:
            maxobjcount = 2
        self.__maxcount = maxobjcount
        self.__cur_count = 0

    def add(self, key, val):
        if val is None:
            raise Exception("None is not allowed as value")
        with self.lock:
            if key in self.__vals:
                return False
            self.__vals[key] = val
            self.__accessed.append(key)
            self.__cur_count += 1
            if self.__cur_count > self.__maxcount:
                keyremove = self.__accessed[0]
                del self.__vals[keyremove]
                self.__accessed.pop(0)
                self.__cur_count -= 1
            return True

    def get(self, key):
        with self.lock:
            val = self.__vals.get(key)
            if val is None:
                raise Exception("Key not found")
            if self.__accessed.index(key) != len(self.__accessed) - 1:
                self.__accessed.remove(key)
                self.__accessed.append(key)
            return val 

    def delkey(self, key):
        with self.lock:
            try:
                del self.__vals[key]
                self.__accessed.remove(key)
                self.__cur_count -= 1
                return True
            except:
                return False


if __name__ == '__main__':
    cache = LruCache(2)
    cache.add(1,2 )
    cache.add(2,3)
    cache.add(3,4)
