import sys
from atexit import register
from time import sleep
from random import randint
import logging
import uuid
import hashlib
from redis import ConnectionPool, Redis
from kazoo.client import KazooClient
from math import sqrt
from threading import Thread, Lock, Condition

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


def stop_zk(zkwrapper):
    zkwrapper.stop()

def init_redis():
    pool = ConnectionPool(host='localhost', port=6379, db=0)
    r = Redis(connection_pool=pool)
    return r


class zk_wrapper:
    def __init__(self, zk):
        self.zk = zk
        self.state = ''
        register(stop_zk, self)

    def stop(self):
        self.zk.stop()
        
    def __call__(self, state):
        self.state = state
     

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
        print 'Zk problem ', e
        if zk is not None:
            zk.stop()
        sys.exit(1)

    inited = True
    return zk

class job_watcher:
    def register_myself(self):
        self.zk.create('/watchers/' + self.myid, ephemeral=True)

    def __init__(self):
        self.lock = Lock()
        self.zk = init()
        self.redis = init_redis()
        self.myid = uuid.uuid4().hex
        self.register_myself()
        self.my_jobs = {}
        children = self.zk.get_children('/jobs', watch=self)
        self.alljobs = children
        children = self.zk.get_children('/watchers', watch=self)
        self.watchers = children
        self.myindex = self.watchers.index(self.myid)
        self.num_watchers = len(self.watchers)
        self.lock_my_job_watches()
        self.job_watcher_thread = Thread(target=self, args = [None])
        self.job_watcher_thread.start()
    
    def unlock_my_jobs(self):
        self.lock.acquire()
        for job, lock in self.my_jobs.items():
            try:
                lock.release()
            except Exception as e:
                print 'Unlocking issue'
        self.my_jobs.clear()
        self.lock.release()

    def stop_monitoring(self):
        self.stall_monitor = True
    
    def start_monitoring(self):
        self.stall_monitor = False

    def watch_for_completion(self):
        jobcount = {}
        self.lock.acquire()
        for job in self.my_jobs:
            try:
                vals = self.zk.get('/jobs/' + job)
                stat, count = vals[0].split('=')
                jobcount[job] = {'count': int(count), 'stat': stat}
            except Exception as e:
                print 'Job watch error ', e
                self.lock.release()
                return
        self.lock.release()
        times = 0 
        while (not self.stall_monitor) and (times < 4):
            times += 1
            temp = ''
            self.lock.acquire()
            for job in self.my_jobs:
                try:
                    if (job not in jobcount) or jobcount[job]['stat'] != PROCESSED:
                        continue
                    processedcount = self.redis.hlen(job + '_completed')
                    if processedcount == jobcount[job]['count'] or processedcount == 0:
                        self.my_jobs[job].release()
                        self.zk.delete('/watchlocks/' + job)
                        self.redis.delete(job + '_completed')
                        self.zk.delete('/jobs/' + job)
                        print 'Job finished ' + job
                        temp = job
                        break
                except Exception as e:
                    print 'Monitor error ', e
            if temp != '':
                del self.my_jobs[temp]
                sleep(0.4)
            self.lock.release()

    def run(self):
        while True:
            if self.stall_monitor:
                sleep(1)
                continue
            self.watch_for_completion() 

    def lock_my_job_watches(self):
        self.stop_monitoring()
        self.unlock_my_jobs()
        self.lock.acquire()
        for child in self.alljobs:
            slot = abs(hash(child)) % self.num_watchers
            if slot != self.myindex:
                continue
            lock = self.zk.Lock('/watchlocks/' + child)
            try:
                if lock.acquire(blocking=True, timeout = 1):
                    self.my_jobs[child] = lock
            except Exception as e:
                print 'Lock problem ', e
        self.lock.release()
        if len(self.my_jobs) > 0:
            self.start_monitoring()

    def __call__(self, event):
        if event is None:
            '''
            I am not the zookeeper event callback
            '''
            self.run()
        if event.path == '/jobs':
            children = self.zk.get_children('/jobs', watch=self)
            self.alljobs = children
        else:
            self.watchers = self.zk.get_children('/watchers', watch=self)
            self.num_watchers = len(self.watchers)
            self.myindex = self.watchers.index(self.myid)
        self.lock_my_job_watches()

class job_executor:

    def register_myself(self):
        self.zk.create('/executors/' + self.myid, ephemeral=True)

    def __init__(self):
        zk = init()
        self.zk = zk
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.some_change = 0
        self.redis = init_redis()
        self.myid = uuid.uuid4().hex
        self.register_myself()
        self.my_jobs = {}
        children = zk.get_children('/jobs', watch=self)
        self.alljobs = children
        children = zk.get_children('/executors', watch=self)
        self.executors = children
        self.myindex = self.executors.index(self.myid)
        self.num_executors = len(self.executors)
        self.keep_running = True
        self.executor_thread = Thread(target=self, args=[None])
        self.executor_thread.start()
    
    def execute(self):
        self.my_jobs = filter(lambda x : (self.alljobs.index(x) % self.num_executors) 
                == self.myindex, self.alljobs) 
        self.execute_jobs()

    def execute_jobs(self):
        some_change = self.some_change
        def isprime(number):
            number = abs(number)
            if number <= 1:
                return False
            if number <= 3:
                return True
            if number & 1 == 0:
                return False
            end = int(sqrt(number))
            i = 3
            while i <= end:
                if number % i == 0:
                    return False
                i += 2
            return True

        if some_change != self.some_change: 
            return
        jobs = set()

        for job in self.my_jobs:
            if some_change != self.some_change:
                return
            try:
                jobval = self.zk.get('/jobs/' + job)
                stat, counts = jobval[0].split('=')
                if stat == SUBMITTED:
                    jobs.add(job)
            except Exception as e:
                print 'Problem happened ', e
        
        while len(jobs) > 0:
            for job in jobs:
                if some_change != self.some_change:
                    return
                try:
                    val = self.redis.lrange(job, 0, 0)
                    if val is None or len(val) == 0:
                        stat = PROCESSED
                        self.zk.set('/jobs/' + job, PROCESSED + '=' + counts)
                        jobs.remove(job)
                        break
                    ival = int(val[0])
                    if self.redis.hmset(job + '_completed' , {ival: isprime(ival)}):
                        self.redis.lpop(job)
                except Exception as e:
                    print 'Some problem ' , e
                    sys.exit(1)

    def run(self):
        while self.keep_running:
            self.execute()
            self.condition.acquire()
            self.condition.wait(1.0)
            self.condition.release()

    def __call__(self, event):
        if event is None:
            self.run()
        if event.path == '/jobs':
            children = self.zk.get_children('/jobs', watch=self)
            self.alljobs = children
        else:
            self.executors = self.zk.get_children('/executors', watch=self)
            self.num_executors = len(self.executors)
            self.myindex = self.executors.index(self.myid)
        self.some_change += 1
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

def job_submitter_main():
    try:
        zk = init()
        cpool = ConnectionPool(host='localhost', port=6379, db=0)
        r = Redis(connection_pool=cpool)
        added = 0
        tried = 0
        max_add_try = 5000
        jobname = uuid.uuid4().hex
        added_nums = set()

        while tried < max_add_try:
            value = randint(5000, 90000000)
            tried += 1
            if value not in added_nums:
                added_nums.add(value)
            else:
                continue

            while True:
                try:
                    r.lpush(jobname, value)
                    added += 1
                    break
                except Exception as e:
                    sleep(1)
                    print "Lpush ", jobname, e
         
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.add_listener(state_listener)
        zk.start()
        value = SUBMITTED + "=" + str(added)
        zk.create('/jobs/' + jobname, value = value)
        zk.stop()

    except Exception as e:
        print 'Big problem in submitting job ', e
        sys.exit(1)
    print 'Job submitted ' + jobname
    

def watcher_main():
    x = job_watcher()

def job_executor_main():
    x = job_executor()

 
if __name__ == '__main__':
    if len(sys.argv)  < 2:
        print 'Usage: ' + sys.argv[0] + ' command'
        print 'Valid commands are : ' + ', '.join(ALLOWED_COMMANDS)
        sys.exit(1)
    
    logging.basicConfig()

    if sys.argv[1] not in ALLOWED_COMMANDS:
        print sys.argv[1] + ' not a valid command'
        sys.exit(1)
    
    if sys.argv[1] == 'watcher':
        watcher_main()
        sleep(86400)
    elif sys.argv[1] == 'jobsubmitter':
        job_submitter_main()
        sleep(2)
    elif sys.argv[1] == 'jobexecutor':
        job_executor_main()
        sleep(86400)

