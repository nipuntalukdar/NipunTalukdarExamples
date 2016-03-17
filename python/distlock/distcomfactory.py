from twisted.internet.protocol import Factory
from distlockcomm import DistLockComm

class DistComFactory(Factory):
    
    def __init__(self, ebus):
        self.ebus = ebus

    def buildProtocol(self, addr):
        return DistLockComm(self.ebus) 

