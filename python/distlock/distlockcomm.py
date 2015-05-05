#!/usr/bin/env python
import sys
import re
from io import BytesIO
from struct import pack, unpack
from io import BytesIO
from clients import get_client
import math
from time import sleep
import traceback
import logging
from twisted.internet import protocol, defer, interfaces, error
from lockmessages_pb2 import StatusMsg
from lockmessages_pb2 import LockDetails, Exchange
from lockcontainer import get_lc
import utility

class DistLockComm(protocol.Protocol):
    def __init__(self):
        self.times = 0
        self.expect_new = True
        self.current_msg_len = 0
        self.current_buffer = BytesIO()
        self.clientId = None
        self.allclients = get_client()
        self.registered = False
        self.peer = None

    def connectionMade(self):
        self.peer = self.transport.socket.getpeername()
        logging.debug('Connection from ' + str(self.peer))

    def handle_msg(self, command):
        self.times += 1
        print len(command)
    
    def handle_chunk(self, command):
        ex = Exchange()
        try:
            ex.ParseFromString(command)
        except Exception as e:
            logging.error(e)
            self.transport.loseConnection()
            return
        exr = Exchange()
        if not self.registered:
            if not ex.HasField('hb'):
                exr.mid = ex.mid
                ex.sm.sv = StatusMsg.FAIL
                resp = exr.SerializeToString()
                outlen = len(resp)
                outbuf = pack('i', outlen)
                self.sendData(outbuf + resp)
                return
            else:
                self.registered = True
                hb = ex.hb
                self.clientId = hb.clientId
                print 'Registered ' , self.clientId
                statusdata = utility.get_StatusMsg_bin(ex.mid, StatusMsg.SUCCESS)
                self.sendData(statusdata)
                self.allclients.add_client(self.clientId)
        else:
            if ex.HasField('ur'):
                print 'Unregistering client ', self.clientId
                self.allclients.unRegisterClient(self.clientId)
                self.transport.loseConnection()
                return
            self.allclients.add_client(self.clientId)
            if ex.HasField('clocks'):
                # details about locks is wanted
                c_locks = ex.clocks
                clientId = c_locks.clientId 
                if not get_client().is_registered(clientId):
                    exr.sm = CLIENT_NOT_REGISTERED
                    resp = exr.SerializeToString()
                    outlen = len(resp)
                    outbuf(pack('i', outlen))
                    self.sendData(outbuf + resp)
                else:
                    clocks = get_lc().getClientLocks(clientId) 
            elif ex.HasField('ld'):
                logging.debug('Getting lock dettails  ' + ex.ld.lockName) 
                ld = get_lc().getLockDetails(ex.ld.lockName)
                lddata = utility.get_lockDetail_resp_msg(ex.mid, ld) 
                self.sendData(lddata)

            elif ex.HasField('lc'):
                lcl = ex.lc 
                logging.debug('Received lock request ' + ' ' +
                               lcl.clientId + ' ' + lcl.cmd.lockId + ' ' +
                               str(lcl.cmd.op.opval))
                status = get_lc().add_lock(lcl.clientId, lcl.cmd.lockId, lcl.cmd.op.opval)
                statusdata = utility.get_StatusMsg_bin(ex.mid, status)
                self.sendData(statusdata)

    def dataReceived(self, data):
        datalen = len(data)
        if self.expect_new:
            if datalen >= 4:
                self.current_msg_len = unpack('i', data[0:4])[0]
                if (self.current_msg_len + 4) == datalen:
                    # We got the entire packet 
                    self.handle_msg(data[4:])
                    return
                elif (self.current_msg_len + 4) > datalen:
                    # We need some more bytes
                    self.current_buffer.write(data[4:])
                    self.expect_new = False
                else:
                    # We may have got more than one message
                    start = 4
                    while True:
                        self.handle_msg(data[start : start + self.current_msg_len])
                        start = start + self.current_msg_len
                        if start == datalen:
                            # We finished all the bytes and there is no incomplete messages
                            # in the bytes
                            self.expect_new = True
                            self.current_msg_len = -1
                            self.current_buffer = BytesIO()
                            break
                        if 4 <= (datalen - start):
                            self.current_msg_len = unpack('i', data[start : start + 4])[0]
                            start += 4
                            if (datalen - start) >= self.current_msg_len:
                                # we have this message also in this buffer
                                continue
                            else:
                                # This message is incomplete, wait for the next chunk
                                self.expect_new = False
                                self.current_buffer = BytesIO()
                                self.current_buffer.write(data[start:])
                                break
                        else:
                            # we don't even know the size of the current buffer
                            self.current_msg_len = -1
                            self.current_buffer = BytesIO()
                            self.current_buffer.write(data[start:])
                            self.expect_new = False
                            break
            else:
                # We haven't even received 4 bytes of data for this brand new 
                # packet
                self.expect_new = False
                self.current_buffer = BytesIO()
                self.current_buffer.write(data)
                self.current_msg_len = -1
        else:
            # Not a new message
            start = 0
            if self.current_msg_len == -1:
                # try to get the message len
                if datalen >= (4 - self.current_buffer.tell()):
                    #get the length of the data
                    start = 4 - self.current_buffer.tell()
                    self.current_buffer.write(data[0: start])
                    self.current_buffer.seek(0)
                    self.current_msg_len = unpack('i', self.current_buffer.read())[0]
                    self.current_buffer = BytesIO()
                else:
                    # Till now even the size of the data is not known
                    self.current_buffer.write(data)
                    return
            while start < datalen:
                if self.current_buffer is None:
                    self.current_buffer = BytesIO()
                if self.current_msg_len == -1:
                    if (datalen - start) < 4:
                        self.current_buffer.write(data[start:])
                        break
                    elif (datalen - start) == 4:
                        self.current_msg_len = unpack('i', data[start:])[0]
                        break
                    else:
                        self.current_msg_len = unpack('i', data[start: start + 4])[0]
                        start += 4
                if (datalen - start) >= (self.current_msg_len - self.current_buffer.tell()):
                    consume = self.current_msg_len -  self.current_buffer.tell()
                    self.current_buffer.write(data[start: start + consume])
                    start += consume
                    self.current_msg_len = - 1
                    self.current_buffer.seek(0)
                    self.handle_msg(self.current_buffer.read())
                    self.current_buffer = BytesIO()
                    if start == datalen:
                        self.expect_new = True
                else:
                    self.current_buffer.write(data[start:])
                    break

    def sendData(self, data):
        return self.transport.write(data)

    def connectionLost(self, reason):
        print 'Lost connection '
        self.registered = False

if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit(1)
    datareadlen = int(sys.argv[1])
    if datareadlen <= 0:
        datareadlen = 10000000
    p = DistLockComm()
    fin = open('out.dump', 'rb')
    byte = None
    while True:
        byte = fin.read(datareadlen)
        if byte == '':
            break
        p.dataReceived(byte)
