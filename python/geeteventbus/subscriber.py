from event import event

class subscriber:
    def __init__(self, topics):
        self.topics = topics
    
    def process(self, event):
        print 'processing', event.get_topic(), event.get_data()

