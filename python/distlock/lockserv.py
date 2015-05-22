#!/usr/bin/env python

import logging
from Queue import Queue 
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from distlockcomm import DistLockComm
from threading import Thread
from clients import Clients
from lockcontainer import LockContainer
from logsettings_client import init_logging
from geeteventbus.eventbus import eventbus

def main():
    init_logging('/tmp/lockserver.log')
    ebus = eventbus()
    clients = Clients(ebus)
    clients.setDaemon(True)
    clients.start()
    lc = LockContainer(ebus)
    lc.setDaemon(True)
    lc.start()
    f = Factory()
    f.protocol = DistLockComm
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
