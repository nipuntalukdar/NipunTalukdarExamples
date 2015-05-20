from time import sleep
from eventbus import eventbus
from event import event 
from subscriber import subscriber

if __name__ == '__main__':
    eb = eventbus()
    subscr =  subscriber('abcd') 
    subscr2 =  subscriber('pqr') 
    eb.register_consumer(subscr, 'abcd')
    subscr =  subscriber('abcd') 
    eb.register_consumer(subscr, 'abcd')
    eb.register_consumer(subscr2, 'pqr')
    ev = event('abcd' , 'a')
    ev2 = event('pqr', 'some data for pqr')
    eb.post(ev)
    eb.post(ev2)

    sleep(20)

    
