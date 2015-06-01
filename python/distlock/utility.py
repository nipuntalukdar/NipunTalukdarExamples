#!/usr/bin/env python
from struct import pack, unpack
from zlib import crc32
from lockmessages_pb2 import Exchange, LockOperation, LockCommandClient, StatusMsg


allowed_lock_mode = [ LockOperation.READLOCK, LockOperation.WRITELOCK, LockOperation.WRITELOCKIMMD, 
        LockOperation.READLOCKIMMD, LockOperation.UNLOCK ]

def get_unRegister_msg(msgid, clientId):
    ex = Exchange()
    ex.mid = msgid 
    ur = ex.ur
    ur.clientId = clientId
    out = ex.SerializeToString()
    outlen = len(out)
    outbuf = pack('i', outlen)
    return outbuf + out

def get_lockDetail_msg(msgid, lockName):
    ex = Exchange()
    ex.mid = msgid 
    ld = ex.ld
    ld.sm.sv = StatusMsg.SUCCESS
    ld.lockName = lockName
    out = ex.SerializeToString()
    outlen = len(out)
    outbuf = pack('i', outlen)
    return outbuf + out

def get_lockDetail_resp_msg(msgid, ldin):
    ex = Exchange()
    ex.mid = msgid 
    ld = ex.ld
    ld.sm.sv = ldin.sm.sv
    ld.currentWriter = ldin.currentWriter
    ld.lockName = ldin.lockName
    ld.lockType = ldin.lockType
    ld.currentWriteWaits.extend(ldin.currentWriteWaits)
    ld.currentReaders.extend(ldin.currentReaders)
    out = ex.SerializeToString()
    outlen = len(out)
    outbuf = pack('i', outlen)
    return outbuf + out


def get_lockOp_msg(msgId, clientId, lockName, op):
    ex = Exchange()
    ex.mid = msgId
    lc = ex.lc
    lc.clientId  = clientId
    lc.cmd.op.opval = op
    lc.cmd.lockId = lockName
    lc.cmd.expireTime = 0 
    out = ex.SerializeToString()
    outlen = len(out)
    outbuf = pack('i', outlen)
    
    return outbuf + out

def get_Response_msg(msgId, status):
    ex = Exchange()
    ex.mid = msgId
    ex.sm.sv = status
    out = ex.SerializeToString()
    outlen = len(out)
    outbuf = pack('i', outlen)
    
    return outbuf + out

def get_readLock_msg(msgId, clientId, lockName):
    return get_lockOp_msg(msgId, clientId, lockName, LockOperation.READLOCK)


def get_writeLock_msg(msgId, clientId, lockName):
    return get_lockOp_msg(msgId, clientId, lockName, LockOperation.WRITELOCK)


def get_unLock_msg(msgId, clientId, lockName):
    return get_lockOp_msg(msgId, clientId, lockName, LockOperation.UNLOCK)


def get_StatusMsg_bin(msgId, status):
    ex = Exchange()
    ex.mid = msgId
    ex.sm.sv = status
    out = ex.SerializeToString()
    outlen = len(out)
    outbuf = pack('i', outlen)
    
    return outbuf + out

def print_lock_details(ld):
    if ld.sm.sv != StatusMsg.SUCCESS:
        print 'Lock details not found for ', ld.locName
        return
    print 'Lock details for ', ld.lockName
    print 'Lock type ', ld.lockType
    if ld.lockType == 'WRITE':
        print 'Writer:', ld.currentWriter
    print 'Readers:' 
    for r in ld.currentReaders:
        print '\t', r
    print 'Write waits:'
    for w in ld.currentWriteWaits:
        print '\t', w

def unpack_protocol_msg(data):
    datalen = unpack('i', data[0:4])
    command = data[4:]
    ex = Exchange()
    try:
        ex.ParseFromString(command)
    except Exception as e:
        print 'Failure in unpacking data'
        return None
    return ex


def get_hash_index(key, max_index, bitwiseand):
    if max_index <= 0:
        return 0
    return abs((crc32(str(key))) & bitwiseand) % max_index
    

if __name__ == '__main__':
    data = get_unLock_msg(1, 'abcdefgh' , 'MyLock2')
    datalen = unpack('i', data[0:4])
    print datalen
    command = data[4:]
    ex = Exchange()
    try:
        ex.ParseFromString(command)
    except Exception as e:
        print e
    print ex

