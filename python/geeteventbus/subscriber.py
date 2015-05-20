from event import event
from threading import current_thread

class subscriber:
    def __init__(self, topics):
        self.topics = topics
        self.registered = False
    
    def process(self, event):
        if not self.registered:
            return
        print current_thread(), 'processing', event.get_topic(), event.get_data()

    def set_registered(self, registered = True):
        self.registered = True
    
    def is_registered(self):
        return self.registered
