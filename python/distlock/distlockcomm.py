#!/usr/bin/env python

import re
from struct import pack, unpack
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
import common
from datachunk import DataChunk
from geeteventbus.subscriber import subscriber
from geeteventbus.event import event

class DistLockComm(protocol.Protocol, DataChunk, subscriber):
    def __init__(self, ebus):
        DataChunk.__init__(self)
        subscriber.__init__(self)
        self.ebus = ebus
        self.clientId = None
        self.allclients = get_client()
        self.registered = False
        self.peer = None

    def process(self, eobj):
        '''
        Events are generally will come from the real lock container
        '''
        data = eobj.get_data()

    def connectionMade(self):
        self.peer = self.transport.socket.getpeername()
        logging.debug('Connection from ' + str(self.peer))


    def handle_msg(self, command):
        ex = Exchange()
        try:
            ex.ParseFromString(command)
        except Exception as e:
            print 'Exception received ', e
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
                statusdata = utility.get_StatusMsg_bin(ex.mid, StatusMsg.SUCCESS)
                self.sendData(statusdata)
                self.allclients.add_client(self.clientId, self)
        else:
            if ex.HasField('ur'):
                logging.debug('Unregistering client ' + self.clientId)
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
                eobj = event(common.LOCKOP_TOPIC, ex, str(lcl.cmd.lockId))
                self.ebus.post(eobj)

    def dataReceived(self, data):
        self.process_chunk(data)

    def sendData(self, data):
        self.transport.write(data)

    def connectionLost(self, reason):
        print 'Lost connection '
        self.registered = False
