class event:
    
    def __init__(self, topic, data, ordered = None):
        self.topic = topic
        self.data = data
        self.ordered = ordered
        if self.ordered is not None:
            if not type(self.ordered) is str:
                raise ValueError('Ordered field must be a string')

    def get_topic(self):
        return self.topic

    def get_data(self):
        return self.data

    def get_ordered(self):
        return self.ordered

