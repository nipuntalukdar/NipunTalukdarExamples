import time
import threading
import logging
from lockservice import LockService
from lockservice.ttypes import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def init_logging():
    FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d  %(message)s'
    logging.basicConfig(filename='/tmp/lockclient.log', format=FORMAT, \
            level = logging.DEBUG)
    logging.debug("Logging initied")

class LockClient(threading.Thread):
    def __init__(self, host, port, clientid):
        threading.Thread.__init__(self)
        init_logging()
        self.clientid = clientid
        self.host = host
        self.port = port
        self.keep_running = True
        self.mutex = threading.Lock()
        transport = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = LockService.Client(self.protocol)
        try:
            self.transport.open()
            ret = self.register_client(clientid)
            if ret == StatusMsg.SUCCESS:
                logging.info('Successfully registered client ' + self.clientid)
        except Exception as e:
            logging.warn(e)
            print e

    def register_client(self, clientid):
        ret = StatusMsg.FAIL
        self.mutex.acquire()
        try:
            ret =  self.client.registerClient(clientid)
        except Exception as e:
            logging.error(e)
            print e
        self.mutex.release()
        return ret
    
    def un_register_client(self, clientid):
        ret = StatusMsg.FAIL
        self.mutex.acquire()
        try:
            ret = self.client.unRegisterClient(clientid)
        except Exception as e:
            logging.error(e)
            return StatusMsg.FAIL
        self.mutex.release()
        return ret

    def lock(self, lockname, mode, clientid):
        ret = StatusMsg.FAIL
        self.mutex.acquire()
        try:
            lockmode = LockOperation.WRITELOCK
            if mode == 'read':
                lockmode = LockOperation.READLOCK
            lck = LockCommand(lockmode, lockname)
            ret = self.client.lockOp(clientid, lck)
        except Exception as e:
            logging.error(e)
        self.mutex.release()
        return ret

    def unlock(self, lockname, clientid):
        ret = StatusMsg.FAIL
        self.mutex.acquire()
        try:
            lck = LockCommand(LockOperation.UNLOCK, lockname)
            ret =  self.client.lockOp(clientid, lck)
        except Exception as e:
            logging.error(e)
        self.mutex.release()
        logging.debug('Try to unlock ' + lockname +  ' by ' + clientid + ' ret=' + str(ret))
        return ret

    def sendHeartBeat(self, clientid):
        ret = StatusMsg.FAIL
        self.mutex.acquire()
        try:
            if clientid is None:
                ret = self.client.sendHeartBeat(self.clientid)
            else:
                ret = self.client.sendHeartBeat(clientid)
        except Exception as e:
            logging.error(e)
        self.mutex.release()
        return ret

    def getLockDetails(self, lockname):
        self.mutex.acquire()
        try:
           ret = self.client.getLockDetails(lockname) 
        except Exception as e:
            logging.error(e)
            ret =  None
        self.mutex.release()
        return ret

    def getClients(self):
        clients = None
        self.mutex.acquire()
        try:
            clients = self.client.getLiveClients()
        except Exception as e:
            logging.error(e)
        self.mutex.release()
        return clients

    def getClientLocks(self, clientId):
        clientLocks = None
        self.mutex.acquire()
        try:
            logging.debug('Getting lock details for client ' + clientId)
            clientLocks = self.client.getClientLocks(clientId)
        except Exception as e:
            logging.error(e)
        self.mutex.release()
        return clientLocks

    def run(self):
        while self.keep_running:
            logging.debug('Sending heartbeat for ' + self.clientid)
            time.sleep(10)
            self.sendHeartBeat(None)

    def stop(self):
        self.keep_running = False
