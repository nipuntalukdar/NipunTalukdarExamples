#!/usr/bin/python
from time import sleep
import logging
import threading
from collections import deque
from lockmessages_pb2 import LockOperation, StatusMsg, LockDetails

lc = None
def get_lc():
    return lc

class Lock:
    def __init__(self, lock, clientId, locktype):
        self.lock = lock
        if locktype == LockOperation.WRITELOCK:
            self.writeLocker = clientId
            self.readers = []
        else:
            self.writeLocker = None
            self.readers = [clientId]
        self.write_waits = deque([])
        self.locktype = locktype

    def add_to_readers(self, clientId):
        if clientId not in self.readers:
            self.readers.append(clientId)

    def add_to_write_waits(self, clientId):
        if clientId != self.writeLocker and clientId not in self.write_waits:
            self.write_waits.append(clientId)

    def unlock_write_lock(self, clientId):
        if self.locktype != LockOperation.WRITELOCK:
            return StatusMsg.LOCK_INVALID_OP

        '''
        Write lock can only be unlocked by the owner
        '''
        if self.writeLocker != clientId:
            return StatusMsg.LOCK_NOT_OWNER
        
        '''
        if there is a write wait, allocate the lock to it
        '''
        self.writeLocker = None
        try:
            self.writeLocker = self.write_waits.popleft()
        except IndexError as e:
            logging.debug(e)
        if self.writeLocker is not None:
            # Notify the new owner TBD
            return StatusMsg.WRITE_LOCK_OWNER_CHANGED 

        ''' 
        There was no write waits. Check if there are readwaits
        '''
        if len(self.readers) != 0:
            # Notify the readers
            self.locktype = LockOperation.READLOCK
            return StatusMsg.WRITE_CHANGED_TO_READ_LOCK
        
        '''
        Nobody wants this object and hence can be removed
        '''

        return StatusMsg.LOCK_CAN_BE_REMOVED


    def unlock_read_lock(self, clientId):
        if self.locktype != LockOperation.READLOCK:
            return StatusMsg.LOCK_INVALID_OP

        self.readers.remove(clientId) 
        if len(self.readers) != 0:
            return StatusMsg.ONE_READ_LOCK_REMOVED

        '''
        if no more readers and 
        if there is a write wait, allocate the lock to it
        '''
        self.writeLocker = None
        try:
            self.writeLocker = self.write_waits.popleft()
        except IndexError as e:
            logging.debug(e.message)
        if self.writeLocker is not None:
            # Notify the new owner TBD
            self.locktype = LockOperation.WRITELOCK
            return StatusMsg.WRITE_LOCK_OWNER_CHANGED 
        
        '''
        Nobody wants this lock and hence can be removed
        '''
        return StatusMsg.LOCK_CAN_BE_REMOVED
            
    '''
    Realese the lock if the lock is "write" owned by the client. 
    Remove the client from readers if it is in readers list
    Remove the client from writewits if it is in write waute list
    '''
    def release_lock(self, clientId): 
        if self.writeLocker == clientId:
            self.writeLocker = None
            # If somebody in writewaits, grant him the write lock
            try:
                self.writeLocker = self.write_waits.popleft()
            except IndexError as e:
                logging.debug("No write waits for " + self.lock)

            if self.writeLocker is not None:
                # Announce the respected client that he got the lock TBD
                return StatusMsg.SUCCESS

            if len(self.readers) == 0:
                return StatusMsg.LOCK_CAN_BE_REMOVED
            
            # Announce all the readers that they got lock TBD 
            self.locktype = LockOperation.READLOCK
            return StatusMsg.WRITE_CHANGED_TO_READ_LOCK   
        
        '''
        If the client is in write_waits, simply remove it 
        '''
        if clientId in self.write_waits:
            self.write_waits.remove(clientId)
            return StatusMsg.SUCCESS
        '''
        if the client is in readers remove it from readers list
        '''
        if clientId in self.readers:
            self.readers.remove(clientId)
        
        '''
        If a writer is already there just return
        '''
        if self.locktype == LockOperation.WRITELOCK:
            return StatusMsg.SUCCESS
        
        '''
        it is a reader lock, if no more readers and there are some writers, 
        announce new writer lock
        '''
        if len(self.readers) != 0:
            return StatusMsg.SUCCESS

        '''
        If no readers and no writers
        The lock cane be removed
        '''
        if len(self.write_waits) == 0:
            return StatusMsg.LOCK_CAN_BE_REMOVED

        '''
        No readers, but some writers, allow writelock to one client and announce
        '''
        self.writeLocker = self.write_waits.popleft()
        self.locktype = LockOperation.WRITELOCK
        # Announce TBD 
        return StatusMsg.READ_CHANDGED_TO_WRIOTE_LOCK

    def unlock(self, clientId):
        if self.locktype == LockOperation.WRITELOCK:
            return self.unlock_write_lock(clientId)
        else:
            return self.unlock_read_lock(clientId)
            

    def __repr__(self):
        owner = self.writeLocker
        if owner is None:
            owner=''
        return 'LockId=' + self.lock + ' owner=' + owner +\
            ' WriteWaits=' + str(self.write_waits) +\
             ' ' + ' Readers=' + str(self.readers)

class LockContainer(threading.Thread):
    def __init__(self, qexpcl):
        global lc
        threading.Thread.__init__(self) 
        self.mutex = threading.Lock()
        self.keep_running = True
        self.alllocks = {}
        self.clientlocks = {}
        self.expire_client_queue = qexpcl
        logging.info('Lock container initialized')
        lc = self
    
    def __del__(self):
        pass
    
    def getLockDetails(self, lock):
        logging.debug('Trying to get LockDetails for ' + lock)
        retval = LockDetails()
        retval.lockName = lock
        self.mutex.acquire()
        if lock in self.alllocks:
            lck = self.alllocks[lock]
            if lck.writeLocker is not None:
                retval.currentWriter = lck.writeLocker
            retval.currentReaders.extend(lck.readers)
            retval.currentWriteWaits.extend(lck.write_waits)
            if lck.locktype == LockOperation.WRITELOCK:
                retval.lockType = 'WRITE'
            else:
                retval.lockType = 'READ'
        self.mutex.release()
        if retval is None:
            logging.debug('Lock details not found' + lock)
            retval.sm.sv = StatusMsg.FAIL
        else:
            retval.sm.sv = StatusMsg.SUCCESS
            logging.debug('Lock details ' + str(retval))
        return retval

    def print_diagnostics(self):
        self.mutex.acquire()
        for lock in self.alllocks:
            print lock, self.alllocks[lock]
        for clientId in self.clientlocks:
            print clientId
            for lock in self.clientlocks[clientId]:
                print '\t', lock, self.clientlocks[clientId][lock] 
        self.mutex.release()

    '''
    This method is called when a write lock exists on the requested lock
    '''
    def check_existing_writelock(self, lck, client, locktype):
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
                return StatusMsg.YOU_WRITELOCKKED
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
                return StatusMsg.YOU_WRITELOCKKED
            logging.debug('Enquing client ' + client + ' as readers for lock ' + lck.lock)
            lck.add_to_readers(client)
            return StatusMsg.READ_LOCK_QUEUED

    def check_existing_lock(self, lck, client, locktype):
        if lck.locktype == LockOperation.WRITELOCK:
            return self.check_existing_writelock(lck, client, locktype)
        else:
            return self.check_existing_readlock(lck, client, locktype)

    def add_lock(self, clientId, lock, locktype):
        '''
        First check if the lock already exists
        '''
        if lock in self.alllocks:
            lck = self.alllocks[lock]
            ret = self.check_existing_lock(lck, clientId, locktype)
            if ret == StatusMsg.WRITE_LOCK_QUEUED or ret == StatusMsg.READ_LOCK_QUEUED:
                if clientId not in self.clientlocks:
                    self.clientlocks[clientId] = {}
                self.clientlocks[clientId][lock] = lck
            return ret
        '''
        Lock doesn't exist, get the new lock
        '''
        logging.debug('Client ' + clientId + ' taking the new lock ' + lock + ' ' + str(locktype))
        lck = Lock(lock, clientId, locktype)
        self.alllocks[lock] = lck
        if clientId not in self.clientlocks:
            self.clientlocks[clientId] =  {}
        self.clientlocks[clientId][lock] = lck
        return StatusMsg.SUCCESS
   
    def getClientLocks(self, clientId):
        ret = None
        logging.debug('Getting locks for client ' + clientId)
        self.mutex.acquire()
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
        self.mutex.release()
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
        self.mutex.acquire()
        if clientId in self.clientlocks:
            clilocks = self.clientlocks[clientId]
            for lock in clilocks:
                lck = clilocks[lock]
                ret = lck.release_lock(clientId)
                if ret == StatusMsg.LOCK_CAN_BE_REMOVED:
                    del self.alllocks[lock]
                logging.debug('Released the lock ' + str(lck))
            del self.clientlocks[clientId]
        self.mutex.release()

    def stop(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            clientId = self.expire_client_queue.get()
            logging.debug('Expiring the client ' + clientId)
            self.expire_client(clientId)
            self.expire_client_queue.task_done()
