#!/usr/bin/python
from time import sleep
import logging
from threading import Thread, Lock
from lockmessages_pb2 import LockOperation, StatusMsg, LockDetails
from geeteventbus.subscriber import subscriber
from geeteventbus.subscriber import event
import common
from utility import get_hash_index, get_Response_msg
from lockdef import LockDef

MAX_PARTITIONS = 16
BITWISEAND = 1023

lc = None
def get_lc():
    return lc


class LockContainer(subscriber):
    def __init__(self, ebus):
        global lc
        subscriber.__init__(self)
        self.biglock = Lock()
        self.keep_running = True
        self.alllocks = {}
        self.partitionlock = {}
        self.clientlocks = {}
        self.ebus = ebus
        self.ebus.register_consumer(self, 'unreg')
        logging.info('Lock container initialized')
        self.partions = []
        self.__init__partitions()
        lc = self
    
    def __del__(self):
        pass

    def __init__partitions(self):
        '''
        Initialize the partition list for the containers. It is a dummy method for 
        the time being. TBD
        '''
        i = 0
        while i < MAX_PARTITIONS:
            self.partions.append(i)
            self.alllocks[i] = {}
            self.partitionlock[i] = Lock()
            i += 1
    
    def getLockDetails(self, lock):
        '''
        Returns the details of the lock with the name 'lock'
        it will return FAIL status message if the lock is not found
        in this lock container
        '''

        logging.debug('Trying to get LockDetails for ' + lock)
        retval = LockDetails()
        retval.lockName = lock
        indx = get_hash_index(lock, MAX_PARTITIONS, BITWISEAND)
        partlock = None
        partallocks = None
        self.biglock.acquire()
        with self.biglock:
            if indx  not in self.alllocks:
                retval.sm.sv = StatusMsg.FAIL
                return retval
            partlock = self.partitionlock[indx]
            partallocks = self.alllocks[indx]
            partlock.acquire()
                
        if lock in partallocks:
            lck = partallocks[lock]
            if lck.writeLocker is not None:
                retval.currentWriter = lck.writeLocker
            retval.currentReaders.extend(lck.readers)
            retval.currentWriteWaits.extend(lck.write_waits)
            if lck.locktype == LockOperation.WRITELOCK:
                retval.lockType = 'WRITE'
            else:
                retval.lockType = 'READ'
        partlock.release()
        if retval is None:
            logging.debug('Lock details not found' + lock)
            retval.sm.sv = StatusMsg.FAIL
        else:
            retval.sm.sv = StatusMsg.SUCCESS
            logging.debug('Lock details ' + str(retval))
        return retval

    def print_diagnostics(self):
        partitions = []
        with self.biglock:
            for part in self.alllocks:
                partitions.append(part)
        if not partitions:
            return
        
        for part in partitions:
            partlock = None
            with self.biglock:
                if part not in self.alllocks:
                    continue
                partlock = self.partitionlock[part]
                partlock.acquire()
            for lock in  self.alllocks[part]:
                print lock, self.alllocks[lock]
            
            partlock.release()
    
    def check_existing_writelock(self, lck, client, locktype):
        '''
        This method is called when a write lock exists on the requested lock
        '''
        if locktype == LockOperation.WRITELOCK:
            if lck.writeLocker == client:
                logging.debug('Lock ' + lck.lock + ' ' + ' is ' + ' already owned by ' + client) 
                return StatusMsg.LOCK_ALREADY_TAKEN
            else:
                if client not in lck.readers:
                    logging.debug('Write lock queued for Lock=' + lck.lock + ' for client ' +\
                            client)
                    lck.add_to_write_waits(client)
                    return StatusMsg.WRITE_LOCK_QUEUED
                else:
                    return StatusMsg.READ_LOCK_ALREADY_QUEUED
        if locktype == LockOperation.READLOCK:
            if lck.writeLocker == client:
                logging.debug('Write lock already by client ' + client + ' for lock ' + lck.lock)
                return StatusMsg.YOU_WRITELOCKED_ALREADY
            else:
                if client not in lck.write_waits:
                    lck.add_to_readers(client)
                    return StatusMsg.READ_LOCK_QUEUED
                else:
                   logging.debug('Already have a write lock request from ' + client + ' on ' +\
                           lck.lock)
                   return StatusMsg.WRITE_LOCK_ALREADY_QUEUED
            
    '''
    This method is called when a read lock exists on the requested lock
    '''
    def check_existing_readlock(self, lck, client, locktype):
        if locktype == LockOperation.WRITELOCK:
            if client not in lck.readers:
                lck.add_to_write_waits(client)
                return StatusMsg.WRITE_LOCK_QUEUED
            else:
                return StatusMsg.READ_LOCK_ALREADY_TAKEN
        else:
            if client in lck.write_waits:
                logging.debug('Client in write waits ' + client + ' for ' + lck.lock)
                return StatusMsg.WRITE_LOCK_ALREADY_QUEUED 
            if client == lck.writeLocker:
                logging.debug('Client ' + client + ' already writelocked ' + lck.lock)
                return StatusMsg.YOU_WRITELOCKED_ALREADY
            logging.debug('Enquing client ' + client + ' as readers for lock ' + lck.lock)
            lck.add_to_readers(client)
            return StatusMsg.READ_LOCK_QUEUED

    
    def check_existing_lock(self, lck, client, locktype):
        if lck.locktype == LockOperation.WRITELOCK:
            return self.check_existing_writelock(lck, client, locktype)
        else:
            return self.check_existing_readlock(lck, client, locktype)

    
    def add_lock(self, clientId, lock, locktype, mid):
        '''
        First check if the lock already exists
        '''
        indx = get_hash_index(lock, MAX_PARTITIONS, BITWISEAND)
        alllocks = self.alllocks[indx]
        partlock = self.partitionlock[indx]
        with partlock:
            if lock in alllocks:
                lck = alllocks[lock]
                ret = self.check_existing_lock(lck, clientId, locktype)
                if ret == StatusMsg.WRITE_LOCK_QUEUED or ret == StatusMsg.READ_LOCK_QUEUED:
                    if clientId not in self.clientlocks:
                        self.clientlocks[clientId] = {}
                    self.clientlocks[clientId][lock] = (lck, mid)
                return ret
            '''
            Lock doesn't exist, get the new lock
            '''
            logging.debug('Client ' + clientId + ' taking the new lock ' + lock + ' ' + str(locktype))
            lck = LockDef(lock, clientId, locktype)
            alllocks[lock] = lck
            if clientId not in self.clientlocks:
                self.clientlocks[clientId] =  {}
            self.clientlocks[clientId][lock] = (lck , mid)
            response = get_Response_msg(mid, StatusMsg.LOCK_GRANTED)
            eobj = event(common.RESPONSE_TOPIC, (clientId, response))
            self.ebus.post(eobj)
            return StatusMsg.SUCCESS
   
    
    def getClientLocks(self, clientId):
        ret = None
        logging.debug('Getting locks for client ' + clientId)
        self.biglock.acquire()
        if clientId in self.clientlocks:
            ret = ClientLocks()
            for lock in self.clientlocks[clientId]:
                lck = self.clientlocks[clientId][lock]
                if lck.writeLocker is not None:
                    if clientId == lck.writeLocker:
                        if ret.writes is None:
                            ret.writes = []
                        ret.writes.append(lock)
                    elif clientId in lck.write_waits:
                        if ret.writeWaits is None:
                            ret.writeWaits = []
                        ret.writeWaits.append(lock)
                    elif clientId in lck.readers:
                        if ret.reads is None:
                            ret.reads = []
                        ret.reads.append(lock)
                else:
                    # Readers locked it
                    if clientId in lck.write_waits:
                        if ret.writeWaits is None:
                            ret.writeWaits = []
                        ret.writeWaits.append(lock)
                    elif clientId in lck.readers:
                        if ret.reads is None:
                            ret.reads = []
                        ret.reads.append(lock)
        self.biglock.release()
        logging.debug('Returned client lock info for client ' + clientId)
        return ret
    
    def unlock(self, clientId, lock):
        logging.debug('Try unlock of ' + lock + ' by ' + clientId)
        if clientId not in self.clientlocks:
            return StatusMsg.CLIENT_NOT_REGISTERED 
        if lock not in self.clientlocks[clientId]:
            return StatusMsg.LOCK_NOT_GRANTED
        
        lck = self.clientlocks[clientId][lock]
        ret = lck.unlock(clientId)
        logging.debug('Unlock returned ' + str(ret))
        del self.clientlocks[clientId][lock]
        if ret == StatusMsg.LOCK_CAN_BE_REMOVED:
            del self.alllocks[lock]
        return StatusMsg.SUCCESS

    def expire_client(self, clientId):
        '''
        Unlock the locks owned by the client
        '''
        self.biglock.acquire()
        if clientId in self.clientlocks:
            clilocks = self.clientlocks[clientId]
            for lock in clilocks:
                lck = clilocks[lock]
                ret = lck.release_lock(clientId)
                if ret == StatusMsg.LOCK_CAN_BE_REMOVED:
                    del self.alllocks[lock]
                logging.debug('Released the lock ' + str(lck))
            del self.clientlocks[clientId]
        self.biglock.release()

    def stop(self):
        self.keep_running = False

    def process(self, eobj):
        try:
            topic = eobj.get_topic()
            ex = eobj.get_data()
            lcl = ex.lc
            mid = ex.mid
            clientId = lcl.clientId
            if topic == common.LOCKOP_TOPIC:
                logging.debug('Received a lock request ')
                #if lcl.cmd.op.opval == lockmessages_pb2.LockOperation.WRITELOCK:
                if lcl.cmd.op.opval == 0:
                    self.add_lock(clientId, lcl.cmd.lockId, lcl.cmd.op.opval, mid)
            else:
                clientId = eobj.get_data()
                logging.debug('Expiring the client ' + clientId)
                self.expire_client(clientId)
        except Exception as e:
            logging.error(e)

