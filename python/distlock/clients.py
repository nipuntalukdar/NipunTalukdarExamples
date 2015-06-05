#!/usr/bin/env python
import time
from bidict import bidict
import threading
from sets import Set
import logging
from rqrsp import RequestResponse
from geeteventbus.eventbus import eventbus
from geeteventbus.subscriber import subscriber
from geeteventbus.event import event 
import common

clientInst = None


def get_client():
    return clientInst


class Clients(threading.Thread, subscriber):

    def __init__(self, ebus):
        global clientInst
        threading.Thread.__init__(self)
        self.mutex = threading.Lock()
        self.clients = {}
        self.clientsproto = {}
        self.clientsdata = {}
        self.buckets = {}
        self.keep_running = True
        self.ebus = ebus
        self.peers = bidict()
        self.client_comms = {}
        clientInst = self
    
    def process(self, eobj):
        topic = eobj.get_topic()
        if topic != common.RESPONSE_TOPIC:
            logging.error('Invalid message recived')
        clientId, response = eobj.get_data()
        proto = None
        try:
            proto = self.clientsproto[clientId]
        except KeyError as e:
            logging.error(e)
        if proto is not None:
            proto.sendData(response)

    
    def add_client_peer(self, clientId, peer):
        self.peers[peer] = clientId
        self.add_client(clientId)

    def send_eobj(self, eobj, clientId):
        self.ebus.post(eobj)

    def send_eobjs(self, eobjs, clientId):
        for eobj in eobjs:
            self.ebus.post(eobj)
        
    def stop(self):
        self.keep_running = False

    def add_client(self, clientId, proto = None):
        self.mutex.acquire()
        curtime = int(time.time())
        expirebucket = curtime + (1023 - (1023 & curtime)) + 1024
        oldexpirebucket = -1
        if clientId in self.clients:
            oldtime = self.clients[clientId]
            oldexpirebucket = oldtime + (1023 - (1023 & oldtime)) + 1024
        self.clients[clientId] = curtime
        if oldexpirebucket != expirebucket and oldexpirebucket != -1:
            self.buckets[oldexpirebucket].remove(clientId)
        if expirebucket not in self.buckets:
            self.buckets[expirebucket] = Set()
        if clientId not in self.buckets[expirebucket]:
            self.buckets[expirebucket].add(clientId)
        if clientId not in self.clientsdata:
           self.clientsdata[clientId] = RequestResponse(clientId) 
        if proto is not None:
            self.clientsproto[clientId] = proto
        self.mutex.release()
    
    def heartbeat(self, clientId):
        self.add_client(clientId)  #Just update clients timestamp

    def is_registered(self, clientId):
        return clientId in self.clients

    def getClients(self):
        ret = []
        self.mutex.acquire()
        logging.debug('Getting client list')
        for client in self.clients:
            ret.append(client)
        self.mutex.release()
        logging.debug('Got client list')
        return ret
    
    def unRegisterClient(self, clientId):
        ret = StatusMsg.SUCCESS
        self.mutex.acquire()
        if clientId not in self.clients:
            ret = StatusMsg.CLIENT_NOT_REGISTERED
        else:
            oldtime = self.clients[clientId]
            oldexpirebucket = oldtime + (1023 - (1023 & oldtime)) + 1024
            self.buckets[oldexpirebucket].remove(clientId)
            del self.clients[clientId]
            eobj = event(common.UNREGISTER_TOPIC, clientId, clientId) 
            self.ebus.post(eobj)
        self.mutex.release()
        return ret
    
    def run(self):
        while self.keep_running:
            time.sleep(30)
            buckets = sorted(self.buckets.keys())
            curtime = int(time.time())
            curtime -= 10
            for bucket in buckets:
                if bucket > curtime: break
                logging.debug('Expiring bucket ' + str(bucket))
                for clientId in self.buckets[bucket]:
                    logging.debug('Deleting client ' + clientId)
                    del self.clients[clientId]
                    del self.clientsproto[clientId]
                    eobj_data = eobj(common.UNREGISTER_TOPIC, clientId, clientId)
                    self.ebus.post(eobj_data)
                self.buckets[bucket].clear()
                del self.buckets[bucket]
