#!/usr/bin/env python

from Queue import Queue
from threading import Lock, Thread
from zlib import crc32

MAX_TOPIC_INDEX = 16 # Must be power of 2

class eventbus(Thread):
    def __init__(self, max_queued_event = 10000):
        Thread.__init__(self)
        self.event_queue = Queue(max_queued_event)
        self.event_queue_size = max_queued_event
        self.topics = MAX_TOPIC_INDEX * [{}]
        self.index_locks = []
        self.consumers = {}
        self.consumers_lock = Lock()
        i = 0
        while i < MAX_TOPIC_INDEX:
            self.index_locks.append(Lock())
            i += 1
        self.setDaemon(True)
        self.start()
    
    def post(self, event):
        self.event_queue.put(event)

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
            elif topic not in self.consumers[consumer]:
                self.consumers[consumer].append(topic)        
    
    def unregister_consumer(self, consumer):
        with self.consumers_lock:
            subscribed_topics = None
            if consumer in self.consumers:
                subscribed_topics = self.consumers[consumer]
                del self.consumers[consumer]
            
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
            

    def run(self):
        print 'started'
        while True:
            event = self.event_queue.get()
            topic = event.get_topic()
            subscribers = self.get_subscribers(topic)
            if subscribers is not None:
                for subscr in subscribers:
                    subscr.process(event)
            self.event_queue.task_done()
