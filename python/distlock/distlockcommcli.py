#!/usr/bin/env python
import time
import threading
import uuid
from sets import Set
import Queue
import logging
from struct import pack, unpack
import threading
from time import sleep
from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory, ReconnectingClientFactory, ClientCreator
from lockmessages_pb2 import LockDetails, Exchange, StatusMsg
from logsettings_client import init_logging
import utility
from datachunk import DataChunk

lc = None

class DistLockClientProto(protocol.Protocol, DataChunk):

    def __init__(self):
        DataChunk.__init__(self)
        self.connected = True
        self.reconnect = True
        self.registered = False
        self.peerhost = None
        self.peerport = 0
        self.clientId = lc.get_client_id()
        self.register_msg_id = lc.get_next_msg_id()

    def setClientId(self, clientId):
        self.clientId = clientId
    
    def sendData(self, data):
        self.transport.write(data)
    
    def connectionMade(self):
        self.connected = True
        self.peerhost, self.peerport = self.transport.socket.getpeername()
        # Register the client
        ex = Exchange()
        ex.mid = self.register_msg_id 
        hb = ex.hb
        hb.clientId = self.clientId
        out = ex.SerializeToString()
        outlen = len(out)
        outbuf = pack('i', outlen)
        self.sendData(outbuf + out)
        lc.add_server_connection(self.peerhost, self.peerport, self)

    def handle_msg(self, response):
        ex = Exchange()
        try:
            ex.ParseFromString(response)
        except Exception as e:
            logging.error(e)
            logging.error('Diconnecting')
            self.transport.loseConnection()
            return
        if ex.HasField('sm'):
            mid = ex.mid
            sm = ex.sm
            logging.debug('Response message id ' +  str(mid) +  ' status ' + str(sm.sv))
            if mid == self.register_msg_id and sm == StatusMsg.SUCCESS:
                self.registered = True
                lc.add_server_registered(self.peerhost, self.peerport)
        elif ex.HasField('ld'):
           utility.print_lock_details(ex.ld)
        else:
            print 'Other  message'

    def dataReceived(self, data):
        self.process_chunk(data)
    
    def unregister(self):
        logging.debug('Unregistering ' + self.clientId)
        self.registered = False
        msg = utility.get_unRegister_msg(lc.get_next_msg_id(), self.clientId) 
        self.reconnect = False
        self.sendData(msg) 

    def get_lock_details(self, lockname):
        msg = utility.get_lockDetail_msg(lc.get_next_msg_id(), lockname)
        logging.debug('Getting lock details for ' + lockname)
        print 'Hi'
        print utility.unpack_protocol_msg(msg)
        self.sendData(msg)
    
    def unlock(self, lockname):
        msg = utility.get_unLock_msg(lc.get_next_msg_id(), self.clientId, lockname) 
        logging.debug('Sending unlock lock request for '+  lockname)
        self.sendData(msg)
    
    def read_lock(self, lockname):
        msg = utility.get_readLock_msg(lc.get_next_msg_id(), self.clientId, lockname) 
        logging.debug('Sending read lock request for '+  lockname)
        self.sendData(msg)

    def write_lock(self, lockname):
        msg = utility.get_writeLock_msg(lc.get_next_msg_id(), self.clientId, lockname) 
        print 'Sending write lock request for', lockname
        self.sendData(msg)

    def connectionLost(self, reason):
        lc.remove_server(self.peerhost, self.peerport)
        self.connected = False
        self.registered = False
        if self.reconnect:
            pass
        logging.debug('Disconnected')


class DistLockClientFactory(ReconnectingClientFactory):
    protocol = DistLockClientProto
    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        logging.error('connection failed:'+ reason.getErrorMessage())
        self.resetDelay()
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        logging.debug('Connection lost, will try reconnection')
        self.resetDelay()
        self.retry(connector)


class LockClient(threading.Thread):
    
    def __init__(self, clientId, initialHostPorts):
        global lc
        lc = self
        threading.Thread.__init__(self)
        self.clientId = clientId
        self.hostPorts = {}
        self.clientComms = {}
        self.serverNextSeq = 1
        self.server_connections = {}
        self.serverNextSeqLock = threading.Lock()
        self.server_regd_to = {}
        for pair in initialHostPorts:
            if pair[0] not in self.hostPorts:
                self.hostPorts[pair[0]] = Set()
            self.hostPorts[pair[0]].add(pair[1])
        self.clientCreator = ClientCreator(reactor, DistLockClientProto)
        d = None
        try:
            d = self.clientCreator.connectTCP('127.0.0.1', 8000)
        except Exception as e:
            logging.debug(e)
        if d is not None:
            d.addErrback(self.failed)
            d.addCallback(self.passed)
    
 
    def get_next_msg_id(self):
        ret = 1
        self.serverNextSeqLock.acquire()
        ret = self.serverNextSeq
        self.serverNextSeq += 1
        self.serverNextSeqLock.release()
        return ret
        
    def get_lock_op(self, lock, locktype):
        pass
    
    def get_lock_server(self, lock):
        for server in self.server_connections:
            return self.server_connections[server]

    def perform_lock_op(self, lock, locktype):
        lockopbin = self.get_lock_op(lock, locktype)
    
    def add_server_connection(self, host, port, proto):
        self.server_connections[(host, port)] = proto
        self.server_regd_to[(host, port)] = False
        print self.server_regd_to

    def add_server_registered(self, host, port):
        self.server_regd_to[(host, port)] = True

    def remove_server(self, host, port):
        if (host, port) in self.server_connections:
            clientId = self.server_connections[(host, port)]
            del self.server_connections[(host, port)]
            del self.server_regd_to[(host, port)]

    def enque_req(self, partId, data):
        if partId not in self.clientReqs:
            self.clientReqs[partId] = Queue(1000)
        self.clientReqs[partId].append(data)

    def passed(self, proto):
        if proto is not None:
            logging.debug('Success ' + proto.peerhost + ':' + str(proto.peerport))
            self.server_connections[(proto.peerhost, proto.peerport)] = proto  
            proto.setClientId(self.clientId)
        
    def failed(self, failure):
        logging.error('Failure')
        return None

    def get_client_locks(self, clId):
        ex = Exchange()
        clocks = ex.clock

    def get_client_id(self):
        return self.clientId

    def get_lock_details(self, lockname):
        # get appropriate server connection
        proto = self.get_lock_server(lockname)
        proto.get_lock_details(lockname)
    
    def unlock(self, lockname):
        proto = self.get_lock_server(lockname) 
        proto.unlock(lockname)

    def read_lock(self, lockname):
        proto = self.get_lock_server(lockname) 
        proto.read_lock(lockname)

    def write_lock(self, lockname):
        proto = self.get_lock_server(lockname) 
        proto.write_lock(lockname)

    def unregister(self):
        for server in self.server_connections:
            proto = self.server_connections[server]
            proto.unregister()

class test_runner(threading.Thread):
    def __init__(self, lc):
        threading.Thread.__init__(self)
        self.lc =lc

    def run(self):
        print 'Started'
        sleep(1)
        lc.read_lock('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.get_lock_details('MyLock2')
        lc.unlock('MyLock')

def main():
    init_logging()
    LockClient(uuid.uuid1().hex, [('localhost', 8000)])
    t = test_runner(lc)
    t.start()
    reactor.run()

if __name__ == '__main__':
    main()
