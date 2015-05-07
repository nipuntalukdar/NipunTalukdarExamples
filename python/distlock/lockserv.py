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

def main():
    init_logging('/tmp/lockserver.log')
    queue = Queue()
    clients = Clients(queue)
    clients.setDaemon(True)
    clients.start()
    lc = LockContainer(queue)
    lc.setDaemon(True)
    lc.start()
    f = Factory()
    f.protocol = DistLockComm
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
