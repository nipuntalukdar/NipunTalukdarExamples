from time import sleep
from eventbus import eventbus
from event import event 
from subscriber import subscriber

def asynchronus_eventbus_test():
    eb = eventbus(subscribers_thread_safe = False)
    subscr =  subscriber('abcd') 
    subscr2 =  subscriber('pqr') 
    eb.register_consumer(subscr, 'abcd')
    subscr =  subscriber('abcd') 
    eb.register_consumer(subscr, 'abcd')
    eb.register_consumer(subscr2, 'pqr')
    ev = event('abcd' , 'a')
    ev2 = event('pqr', 'some data for pqr')
    i = 1
    while i < 100:
        eb.post(ev)
        eb.post(ev2)
        i += 1
    sleep(1)
    eb.shutdown()

def synchronus_eventbus_test():
    eb = eventbus(synchronus = True)
    subscr =  subscriber('abcd') 
    subscr2 =  subscriber('pqr') 
    eb.register_consumer(subscr, 'abcd')
    subscr =  subscriber('abcd') 
    eb.register_consumer(subscr, 'abcd')
    eb.register_consumer(subscr2, 'pqr')
    ev = event('abcd' , 'a')
    ev2 = event('pqr', 'some data for pqr')
    i = 0
    while i < 100:
        eb.post(ev)
        eb.post(ev2)
        sleep(0.1)
        i += 1
    eb.shutdown()

if __name__ == '__main__':
    #synchronus_eventbus_test()
    asynchronus_eventbus_test()
    sleep(2)
