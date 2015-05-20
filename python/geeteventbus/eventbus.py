#!/usr/bin/env python

from time import time
from threading import Lock, Thread, current_thread
import logging
from Queue import Queue, Empty
from zlib import crc32

MAX_TOPIC_INDEX = 16 # Must be power of 2
DEFAULT_EXECUTOR_COUNT = 8
MAX_EXECUTOR_COUNT = 1024
MIN_EXECUTOR_COUNT = 1
MAX_EXECUTOR_COUNT = 128
MAXIMUM_QUEUE_LENGTH = 25600
MINIMUM_QUEUE_LENGTH = 16


class eventbus:
    def __init__(self, max_queued_event = 10000, executor_count = DEFAULT_EXECUTOR_COUNT,
            synchronus = False, subscribers_thread_safe = True):
        self.synchronus = synchronus
        self.subscribers_thread_safe = subscribers_thread_safe
        self.topics = MAX_TOPIC_INDEX * [{}]
        self.index_locks = []
        self.consumers = {}
        self.consumers_lock = Lock()
        self.subscriber_locks = {}
        self.keep_running = True
        self.stop_time = 0
        i = 0
        while i < MAX_TOPIC_INDEX:
            self.index_locks.append(Lock())
            i += 1
        
        if not self.synchronus:
            self.event_queue = Queue(max_queued_event)
            self.event_queue_size = MAXIMUM_QUEUE_LENGTH
            if max_queued_event >= MINIMUM_QUEUE_LENGTH and max_queued_event <= \
                MAXIMUM_QUEUE_LENGTH:
                self.event_queue_size = max_queued_event
            self.executor_count = executor_count
            if executor_count < MIN_EXECUTOR_COUNT or executor_count > MAX_EXECUTOR_COUNT:
                self.executor_count = DEFAULT_EXECUTOR_COUNT
            self.executors = []
            i = 0
            while i < self.executor_count:
                thrd = Thread(target = self)
                thrd.setDaemon(True)
                self.executors.append(thrd)
                i += 1
            for thrd in self.executors:
                thrd.start()
        else:
            def __post_synchronous(event):
                topic = event.get_topic()
                data = event.get_data()
                subscribers = self.get_subscribers(topic)
                if subscribers is not None:
                    for subscr in subscribers:
                        if not subscr.is_registered():
                            continue
                        try:
                            subscr.process(event)
                        except Exception as e:
                            logging.error(e)
            self.post_synchronous = __post_synchronous

    
    def post(self, event):
        if not self.keep_running:
            return False
        if not self.synchronus:
            self.event_queue.put(event)
        else:
            self.post_synchronous(event)
        return True


    def register_consumer(self, consumer, topic):
        indexval = crc32(topic) & (MAX_TOPIC_INDEX - 1)
        with self.consumers_lock:
            with self.index_locks[indexval]:
                if topic not in  self.topics[indexval]:
                    self.topics[indexval][topic] = [ consumer ]
                elif consumer not in self.topics[indexval][topic]:
                    self.topics[indexval][topic].append(consumer)
            if consumer not in self.consumers:
                self.consumers[consumer] = [ topic ]
                consumer.set_registered()
            elif topic not in self.consumers[consumer]:
                self.consumers[consumer].append(topic)        
            if not self.subscribers_thread_safe:
                if consumer not in self.subscriber_locks:
                    self.subscriber_locks[consumer] = Lock()
    
    
    def unregister_consumer(self, consumer):
        with self.consumers_lock:
            consumer.set_registered(False)
            subscribed_topics = None
            if consumer in self.consumers:
                subscribed_topics = self.consumers[consumer]
                del self.consumers[consumer]
            if self.subscribers_thread_safe and (consumer in self.subscriber_locks):
                del self.subscriber_locks[consumer]
            
            if subscribed_topics is None:
                return
            for topic in subscribed_topics:
                indexval = crc32(topic) & (MAX_TOPIC_INDEX - 1)
                with self.index_locks[indexval]:
                    if (topic in self.topics[indexval]) and (consumer in\
                            self.topics[indexval][topic]):
                        self.topics[indexval][topic].remove(consumer)
                        if len(self.topics[indexval][topic]) == 0:
                            del self.topics[indexval][topic]
   
    
    def get_subscribers(self, topic):
        indexval = crc32(topic) & (MAX_TOPIC_INDEX - 1)
        with self.index_locks[indexval]:
            if topic not in self.topics[indexval]:
                return None
            return self.topics[indexval][topic]
            
    
    def __call__(self):
        while True:
            if self.stop_time > 0:
                if time() < self.stop_time: break
            event = None
            try:
                event = self.event_queue.get(timeout = 0.1)
            except Empty as e:
                continue
            topic = event.get_topic()
            subscribers = self.get_subscribers(topic)
            if subscribers is not None:
                for subscr in subscribers:
                    lock = None
                    if not subscr.is_registered():
                        continue
                    if not self.subscribers_thread_safe:
                        try:
                            lock = self.subscriber_locks[subscr]
                        except KeyError as e:
                            logging.error(e)
                            continue
                    if lock is not None:
                        lock.acquire()
                    try:
                        subscr.process(event)
                    except Exception as e:
                        logging.error(e)
                    if lock is not None:
                        lock.release()
            self.event_queue.task_done()


    def shutdown(self):
        self.keep_running = False
        self.stop_time = time() + 2
        if not self.synchronus:
            for thrd in self.executors:
                thrd.join()
