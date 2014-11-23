from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess
from twisted.internet import reactor


def start_ftp_server(rootdir):
    p = Portal(FTPRealm(rootdir), [AllowAnonymousAccess()])
    f = FTPFactory(p)
    reactor.listenTCP(2022, f)

if __name__ == '__main__':
    start_ftp_server('/tmp')
    reactor.run()
