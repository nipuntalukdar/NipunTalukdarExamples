from random import randint

class Schedule(object):
    def __init__(self, start, end):
        self.__start__ = start
        self.__end__ = end
    @property
    def start(self):
        return self.__start__

    @property
    def end(self):
        return self.__end__

    def __repr__(self):
        return '[{} {}]'.format(self.__start__, self.__end__)

def compare(schedule1, schedule2):
   if schedule1.end != schedule2.end:
       return schedule1.end - schedule2.end
   if schedule1.start != schedule2.start:
       return schedule1.start - schedule2.start
   return 0

def optimal_schedules(unsorted_schedules):
    # Sort the schedule by their finish time
    schedules = sorted(unsorted_schedules, cmp=compare)
    ret = []
    last = None
    # Now progressively select schedules with lowest end time,
    # which has a start time greater than the end time of the 
    # previously selected schedule
    for a in schedules:
        if not ret:
            ret.append(a)
            last = a
        elif last.end < a.start :
            last = a
            ret.append(a)
    return ret

if __name__ == '__main__':
    i = 1
    schedules = []
    while i < 11:
        start = randint(1,20)
        schedules.append(Schedule(start, start + randint(1,15)))
        i += 1
    print 'Proposed schedules', schedules
    print 'Schedules alloted', optimal_schedules(schedules)

