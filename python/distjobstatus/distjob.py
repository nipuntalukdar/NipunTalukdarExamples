import sys
from atexit import register
from time import sleep
from random import randint
import logging
import uuid
import hashlib
from redis import ConnectionPool, Redis
from kazoo.client import KazooClient

SUBMITTED = 'subm'
PROCESSED = 'prcd'
ZIPPED = 'zpd'
UPLOADED = 'uploaded'

inited = False

ALLOWED_COMMANDS = ['watcher', 'jobsubmitter', 'jobexecutor']

def state_listener(state):
    print state

def create_path_if_not_exists(zk, path):
    if not zk.exists(path):
        try:
            zk.ensure_path(path)
        except Exeception as e:
            print e
            return False
    return True

def stop_zk(zk):
    if inited:
        zk.stop()

def init():
    global inited
    zk = None
    try:
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.add_listener(state_listener)
        zk.start()
        register(stop_zk, zk)
        create_path_if_not_exists(zk, '/jobs')
        create_path_if_not_exists(zk, '/watchers')
        create_path_if_not_exists(zk, '/watchlocks')
        create_path_if_not_exists(zk, '/executors')
    except Exception as e:
        print e
        if zk is not None:
            zk.stop()
        sys.exit(1)

    inited = True
    return zk

class job_watcher:
    def register_myself(self):
        self.zk.create('/watchers/' + self.myid, ephemeral=True)

    def __init__(self, zk):
        self.zk = zk
        self.myid = uuid.uuid4().hex
        self.register_myself()
        self.myjobs = {}
        children = zk.get_children('/jobs', watch=self)
        self.alljobs = set(children)
        children = zk.get_children('/watchers', watch=self)
        self.watchers = children
        self.myindex = self.watchers.index(self.myid)
        self.num_watchers = len(self.watchers)
        self.lock_my_job_watches()
    
    def unlock_my_jobs(self):
        for job, lock in self.myjobs.items():
            lock.release()
            print "Unlocked " + job
        self.myjobs.clear()

    def lock_my_job_watches(self):
        self.unlock_my_jobs()
        for child in self.alljobs:
            slot = abs(hash(child)) % self.num_watchers
            if slot != self.myindex:
                continue
            lock = self.zk.Lock('/watchlocks/' + child)
            try:
                if lock.acquire(blocking=True, timeout=1):
                    self.myjobs[child] = lock
            except Exception as e:
                print "Lock problem ", e
            else:
                print "Locked " + child

    def __call__(self, event):
        if event.path == '/jobs':
            children = self.zk.get_children('/jobs', watch=self)
            self.alljobs = set(children)
        else:
            self.watchers = self.zk.get_children('/watchers', watch=self)
            self.num_watchers = len(self.watchers)
            self.myindex = self.watchers.index(self.myid)

        print self.watchers
        print self.alljobs
        print self.myjobs
        self.lock_my_job_watches()

class job_executor:

    def register_myself(self):
        self.zk.create('/executors/' + self.workerid, ephemeral=True)

    def __init__(self, zk):
        self.zk = zk
        self.myid = uuid.uuid4().hex
        self.register_myself()
        self.myjobs = {}
        children = zk.get_children('/jobs', watch=self)
        self.alljobs = set(children)
        children = zk.get_children('/executors', watch=self)
        self.executors = children
        self.myindex = self.executors.index(self.myid)
        self.num_executors = len(self.executors)
        self.execute()
    
    def execute(self):
        self.myjobs.clear()
        self.my_jobs = filter(lambda x : (x % self.num_executors) == self.myindex, self.alljobs) 
        self.execute_jobs()

    def execute_jobs(self):

        
    def __call__(self, event):
        if event.path == '/jobs':
            children = self.zk.get_children('/jobs', watch=self)
            self.alljobs = set(children)
        else:
            self.executors = self.zk.get_children('/executors', watch=self)
            self.num_executors = len(self.executors)
            self.myindex = self.executors.index(self.myid)

        print self.executors
        print self.alljobs
        print self.myjobs
        self.execute()

def job_submitter_main():
    try:
        zk = init()
        cpool = ConnectionPool(host='localhost', port=6379, db=0)
        r = Redis(connection_pool=cpool)
        i = randint(1000, 100000)
        jobname = uuid.uuid4().hex
        queues = {0 : jobname +"_0", 1 : jobname + "_1", 2 : jobname + "_2" } 
        added_nums = set()
        added = 0
        while i > 0:
            value = randint(5000, 1000000)
            if value not in added_nums:
                added_nums.add(value)
                part = (value & 3) % 3
                r.lpush(queues[part], randint(5000, 1000000))
                added += 1
            i -= 1
         
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.add_listener(state_listener)
        zk.start()
        value = SUBMITTED + "=" + str(added)
        zk.create('/jobs/' + jobname, value = value)
        zk.stop()

    except Exception as e:
        print 'Big problem', e
        sys.exit(1)
    print "Job submitted " + jobname
    

def watcher_main():
    zk = init()
    x = job_watcher(zk)
    sleep(10)
 
if __name__ == '__main__':
    if len(sys.argv)  < 2:
        print "Usage: " + sys.argv[0] + " command"
        print "Valid commands are : " + ', '.join(ALLOWED_COMMANDS)
        sys.exit(1)
    
    logging.basicConfig()

    if sys.argv[1] not in ALLOWED_COMMANDS:
        print sys.argv[1] + " not a valid command"
        sys.exit(1)
    
    if sys.argv[1] == 'watcher':
        watcher_main()
    elif sys.argv[1] == 'jobsubmitter':
        job_submitter_main()

