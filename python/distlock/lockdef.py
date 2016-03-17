from time import sleep
import logging
import threading
from collections import deque
from lockmessages_pb2 import LockOperation, StatusMsg, LockDetails
from geeteventbus.subscriber import subscriber

def synced(func):
    def lockingfunc(self, *args, **kwargs):
        with self.lock:
            func(self, *args, **kwargs)
    return lockingfunc

class LockDef:
    def __init__(self, lock, clientId, locktype, ebus):
        self.lock = lock
        self.ebus = ebus
        if locktype == LockOperation.WRITELOCK:
            self.writeLocker = clientId
            self.readers = []
        else:
            self.writeLocker = None
            self.readers = [clientId]
        self.write_waits = deque([])
        self.locktype = locktype

    @synced
    def add_to_readers(self, clientId):
        if clientId not in self.readers:
            self.readers.append(clientId)

    @synced
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
            eobj = event(common.RESPONSE_TOPIC, (clientId, -1))
            self.ebus.post(eobj)
            return StatusMsg.WRITE_LOCK_OWNER_CHANGED

        ''' 
        There was no write waits. Check if there are readwaits
        '''
        if len(self.readers) != 0:
            # Notify the readers
            self.locktype = LockOperation.READLOCK
            for clientId in self.readers:
                eobj = event(common.RESPONSE_TOPIC, (clientId, -1))
                self.ebus.post(eobj)
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
