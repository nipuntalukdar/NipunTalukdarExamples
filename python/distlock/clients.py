#!/usr/bin/env python
import time
from bidict import bidict
import threading
from sets import Set
import logging
import rqrsp impor RequestResponse

clientInst = None

def get_client():
    return clientInst

class Clients(threading.Thread):

    def __init__(self, queue):
        global clientInst
        threading.Thread.__init__(self)
        self.mutex = threading.Lock()
        self.clients = {}
        self.clientsdata = {}
        self.buckets = {}
        self.keep_running = True
        self.queue = queue
        self.peers = bidict()
        self.client_comms = {}
        clientInst = self
    
    def add_client_peer(self, clientId, peer):
        self.peers[peer] = clientId
        self.add_client(clientId)

    def send_event(self, event, clientId):
        pass

    def send_events(self, events, clientId):
        pass
        
    def stop(self):
        self.keep_running = False

    def add_client(self, clientId):
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
           self.clientsdata[clientId] = RequestResponse() 
        self.mutex.release()
    
    def heartbeat(self, clientId):
        self.add_client(clientId)

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
            self.queue.put(clientId)
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
                    self.queue.put(clientId)
                self.buckets[bucket].clear()
                del self.buckets[bucket]
