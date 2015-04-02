import sys
import signal
import time
from Queue import Queue
import logging
from lockservice import LockService
from lockservice.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from lockcontainer import Lock, LockContainer
from clients import Clients
from lockserverdiag import LockSeverDiag

handler = None

def init_logging():
    FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d  %(message)s'
    logging.basicConfig(filename='/tmp/lockserver.log', format=FORMAT, \
            level = logging.DEBUG)
    logging.debug("Logging initied")

    
class LockServiceHandler:
    def __init__(self):
        self.queue = Queue()
        self.lc = LockContainer(self.queue)
        self.lc.setDaemon(True)
        self.lc.start()
        self.lg = LockSeverDiag(self.lc)  
        self.lg.setDaemon(True)
        self.lg.start()
        self.clients = Clients(self.queue)
        self.clients.setDaemon(True)
        self.clients.start()  

    def __del__(self):
        self.clients.stop()

    def lockOp(self, clientId, lockCmd):
        if not self.clients.is_registered(clientId):
            return StatusMsg.CLIENT_NOT_REGISTERED
        return self.lc.add_lock(clientId, lockCmd.lockId, lockCmd.op) 

    def registerClient(self, clientId):
        self.clients.add_client(clientId)
        return StatusMsg.SUCCESS

    def sendHeartBeat(self, clientId):
        if not self.clients.is_registered(clientId):
            return StatusMsg.CLIENT_NOT_REGISTERED
        self.clients.heartbeat(clientId)
        return StatusMsg.SUCCESS

    def reRegisterLocks(self, clientId, locks):
        if not self.clients.is_registered(clientId):
            return StatusMsg.CLIENT_NOT_REGISTERED
        for lock in locks.locks:
            self.lc.add_lock(clientId, lock.lockId, lock.op) 
        return StatusMsg.SUCCESS

    def getLockDetails(self, lockid):
       return self.lc.getLockDetails(lockid) 

    def getLiveClients(self):
        return self.clients.getClients()

    def unRegisterClient(self, clientId):
        return self.clients.unRegisterClient(clientId)
    
    def shutDown(self):
        self.clients.stop()
        self.lc.stop()
        self.lg.stop()

def handle_sigs(signo, frame):
    handler.shutDown()
    time.sleep(20)
    sys.exit(2)

init_logging()
handler = LockServiceHandler()
signal.signal(signal.SIGTERM, handle_sigs)
signal.signal(signal.SIGINT, handle_sigs)
processor = LockService.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
print 'Starting the server...'
server.serve()
print 'done.'
