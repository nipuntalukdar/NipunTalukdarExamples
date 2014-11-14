from twisted.internet import defer, reactor

def getDummyData(x):
    d = defer.Deferred()
    d.addCallback(printData)
    reactor.callLater(2, d.callback, x * 3)
    return d

def printData(d):
    print "Came here"
    print d
    return 4

def printVal2(val):
    print "Printing value " , val

d = getDummyData(3)
d.addCallback(printData)
reactor.callLater(4, reactor.stop)
reactor.run()

d = defer.Deferred()
d.addCallback(printVal2)
d.callback(3)
