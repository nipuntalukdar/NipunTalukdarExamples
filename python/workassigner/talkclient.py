import os
import socket
from twisted.internet import reactor, protocol
'''
Below are our imports
'''

import constants


class talkclient(protocol.Protocol):
    def connectionMade(self):
        workerid = socket.gethostname()
        myid = os.getenv('MY_ID')
        if myid is not None:
            workerid += "-" + myid
        self.transport.write(constants.JOINING + constants.SEPARATOR + workerid) 
        
    def dataReceived(self, data):
        print data
        pass
print constants.SEPARATOR
