class event:
    
    def __init__(self, topic, data):
        self.topic = topic
        self.data = data

    def get_topic(self):
        return self.topic

    def get_data(self):
        return self.data

