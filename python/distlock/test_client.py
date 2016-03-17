import threading
import uuid
from time import sleep
from twisted.internet import reactor
from logsettings_client import init_logging
from distlockcommcli import LockClient

class test_runner(threading.Thread):
    def __init__(self, lc):
        threading.Thread.__init__(self)
        self.lc =lc

    def run(self):
        print 'Started'
        sleep(1)
        self.lc.write_lock('MyLock3')
        self.lc.unlock('MyLock3')
        '''
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.get_lock_details('MyLock2')
        self.lc.unlock('MyLock')
        '''

def main():
    init_logging()
    lc = LockClient(uuid.uuid1().hex, [('localhost', 8000)])
    t = test_runner(lc)
    t.start()
    reactor.run()

if __name__ == '__main__':
    main()
