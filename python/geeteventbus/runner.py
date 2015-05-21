import sys
from time import sleep
from eventbus import eventbus
from event import event 
from subscriber import subscriber
from signal import signal, SIGTERM, SIGINT

ebus = None


def asynchronus_eventbus_test():
    global ebus
    ebus = eventbus(subscribers_thread_safe = False)
    subscr =  subscriber('abcd') 
    subscr2 =  subscriber('pqr') 
    ebus.register_consumer(subscr, 'abcd')
    subscr =  subscriber('abcd') 
    ebus.register_consumer(subscr, 'abcd')
    ebus.register_consumer(subscr2, 'pqr')
    ev = event('abcd' , 'a')
    i = 1
    while i < 100:
        ebus.post(ev)
        i += 1
    sleep(1)
    ebus.shutdown()


def asynchronus_eventbus_test_ordered_event():
    global ebus
    ebus = eventbus(subscribers_thread_safe = True)
    subscr =  subscriber('abcd') 
    subscr2 =  subscriber('pqr') 
    ebus.register_consumer(subscr, 'abcd')
    subscr =  subscriber('abcd') 
    ebus.register_consumer(subscr, 'abcd')
    ebus.register_consumer(subscr2, 'pqr')
    ev = event('abcd' , 'Your data here', 'orderkey')
    i = 1
    while i < 100:
        ebus.post(ev)
        i += 1
    sleep(1)
    ebus.shutdown()


def synchronus_eventbus_test():
    global ebus
    ebus = eventbus(synchronus = True)
    subscr =  subscriber('abcd') 
    subscr2 =  subscriber('pqr') 
    ebus.register_consumer(subscr, 'abcd')
    subscr =  subscriber('abcd') 
    ebus.register_consumer(subscr, 'abcd')
    ebus.register_consumer(subscr2, 'pqr')
    ev = event('abcd' , 'a')
    ev2 = event('pqr', 'some data for pqr')
    i = 0
    while i < 100:
        ebus.post(ev)
        ebus.post(ev2)
        sleep(0.1)
        i += 1
    ebus.shutdown()
    sleep(4)


def interuppt_handler(signo, statck):
    if ebus is not None:
        ebus.shutdown()
    sys.exit(1)


if __name__ == '__main__':
    signal(SIGTERM, interuppt_handler)
    signal(SIGINT, interuppt_handler)
    synchronus_eventbus_test()
    asynchronus_eventbus_test()
    asynchronus_eventbus_test_ordered_event()
    sleep(2)
