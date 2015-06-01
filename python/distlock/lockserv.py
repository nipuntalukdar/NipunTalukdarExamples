#!/usr/bin/env python

import logging
from Queue import Queue 
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from geeteventbus.eventbus import eventbus
from distlockcomm import DistLockComm
from threading import Thread
from clients import Clients
from lockcontainer import LockContainer
from logsettings_client import init_logging
from distcomfactory import DistComFactory
import common

def main():
    init_logging('/tmp/lockserver.log')
    ebus = eventbus()
    clients = Clients(ebus)
    clients.setDaemon(True)
    clients.start()
    lc = LockContainer(ebus)
    ebus.register_consumer(lc, common.LOCKOP_TOPIC)
    ebus.register_consumer(lc, common.UNREGISTER_TOPIC)
    ebus.register_consumer(clients, common.RESPONSE_TOPIC)
    f = DistComFactory(ebus)
    f.protocol = DistLockComm
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
