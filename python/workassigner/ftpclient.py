from twisted.protocols.ftp import FTPClient
from twisted.internet.protocol import Protocol, ClientCreator
from twisted.internet import reactor
import string
import signal
from cStringIO import StringIO


class BufferingProtocol(Protocol):
    def __init__(self):
        self.buffer = StringIO()

    def dataReceived(self, data):
        self.buffer.write(data)


def success(response):
    print 'Success!  Got response:'
    print '---'
    if response is None:
        print None
    else:
        print string.join(response, '\n')
    print '---'


def fail(error):
    print 'Failed.  Error was:'
    print error


def showBuffer(result, bufferProtocol):
    print 'Got data:'
    print bufferProtocol.buffer.getvalue()
    print "*******************************"
    print "*******************************"


def get_file(filename):
    print "Here"
    creator = ClientCreator(reactor, FTPClient, 'anonymous', 'passwd', 1)
    creator.connectTCP('localhost', 2021).addCallback(connectionMade, filename)
           .addErrback(connectionFailed)


def connectionFailed(f):
    print "Connection Failed:", f

def connectionMade(ftpClient, filename):
    print "Connection made"
    proto = BufferingProtocol()
    d = ftpClient.retr(filename , proto)
    d.addCallbacks(showBuffer, fail, callbackArgs=(proto,))
    ftpClient.quit().addCallbacks(success,fail)

def start_reactor():
    reactor.run(installSignalHandlers=0)

def term(signum, frame):
    print "Stoping"
    reactor.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, term)
    signal.signal(signal.SIGINT, term)
    #t = Thread(target = start_reactor)
    #t.start()
    signal.signal(signal.SIGTERM, term)
    signal.signal(signal.SIGINT, term)
    get_file('ftpserver.py')
    get_file('ftpserver.py')
    get_file('ftpserver.py')
    reactor.run(installSignalHandlers=0)
