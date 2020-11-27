from functools import cmp_to_key

class Act(object):
    def __init__(self, start, end):
        self.__start__ = start
        self.__end__ = end

    @property
    def start(self):
        return self.__start__

    @property
    def end(self):
        return self.__end__

    def __str__(self):
        return '({},{})'.format(self.__start__, self.__end__)

    def __repr__(self):
        return '({},{})'.format(self.__start__, self.__end__)

def myfunc(k1, k2):
    if k1.end != k2.end:
        return k1.end - k2.end
    return k1.start - k2.start

def activity_select(acts):
    # sort by end time
    acts.sort(key=cmp_to_key(myfunc))
    selected = []
    last_selected = None
    for a in acts:
        if not last_selected:
            last_selected = a
            selected.append(a)
            continue
        # take the activity if its start time is 
        # greater than or equal last selected task's end time
        if a.start >= last_selected.end:
            selected.append(a)
            last_selected = a

    return selected


acts = [Act(100,102), Act(101, 102), Act(102, 104), Act(105, 108), Act(106,
                109), Act(109, 110), Act(108, 109)]

print(activity_select(acts))

    
