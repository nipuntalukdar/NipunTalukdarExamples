import cmd
import re
import uuid
from lockservice.ttypes import *
from lockclient import LockClient

default_client = uuid.uuid1().hex 

class LockServiceSehell(cmd.Cmd):
    MODE_W = 'write'
    MODE_R = 'read'

    def __init__(self, host, port):
        cmd.Cmd.__init__(self)
        self.host = host
        self.port = port
        self.lclient = LockClient(self.host, self.port, default_client)  
        self.lclient.setDaemon(True)
        self.lclient.start()

    def do_lock(self, line):
        '''
        cretes a lock. Example is:
        lock locname write/read [clientid]
        '''
        els = re.split('\s+', line) 
        if len(els) < 2:
            print 'Lock expects minimum 3 args'
            return
        lockname = els[0]
        lockmode = els[1].lower()
        client = default_client
        if len(els) > 2:
            client = els[2]
        if lockmode != LockServiceSehell.MODE_R and LockServiceSehell.MODE_W != lockmode:
            print 'Invalid lockmode'
        else:
            print self.lclient.lock(lockname, lockmode, client)

    def do_unlock(self, line):
        '''
        Unlocks a lock. Example below:
        unlock lockname [clentid]
        '''
        els = re.split('\s+', line) 
        if len(els) < 1:
            print 'Unlock expects minimum 1 args'
            return
        lockname = els[0]
        client = default_client
        if len(els) > 1:
            client = els[1]
        print self.lclient.unlock(lockname, client) 

    def do_lockdetails(self, line):
        '''
        Get the details of a lock. Example below:
        lockdetails lockname
        '''
        els = re.split('\s+', line) 
        if len(els) < 1:
            print 'lockdetails expects minimum 1 arg'
            return
        lockname = els[0]
        ld = self.lclient.getLockDetails(lockname)
        if ld is not None:
            print ld
        else:
            print 'Some problem in getting details for ' + lockname

    def do_dumplocks(self, line):
        '''
        Dumps the all lock details. Example below:
        dumplocks
        '''
        pass

    def do_register(self, line):
        '''
        Registers a client. Example below:
        register clientid
        '''
        els = re.split('\s+', line) 
        if len(els) < 1:
            print 'register expects minimum 1 arg'
            return
        clientid = els[0]
        ret = self.lclient.register_client(clientid)
        print 'Returned ' + str(ret)

    def do_unregister(self, line):
        '''
        De-registers a client. Example below:
        unregister clientid
        '''
        els = re.split('\s+', line) 
        if len(els) < 1:
            print 'unregister expects minimum 1 arg'
            return
        clientid = els[0]
        ret = self.lclient.un_register_client(clientid)
        if ret != StatusMsg.SUCCESS:
            print "Some problem. Error code " + str(ret)
        else:
            print 'Successfully unregisterd ' + clientid

    def do_exit(self, line):
        '''
        Exit the lock servuce shell. Example below:
        exit
        '''
        return self.do_quit(line)

    def do_quit(self, line):
        '''
        Exit the lock servuce shell. Example below:
        quit
        '''
        print "Exiting...."
        return True

    def do_getclients(self, line):
        '''
        Prints the list of current registered client. Example below:
        getclients
        '''
        clients = self.lclient.getClients()
        for client in clients:
            print 'Client:', client

    def do_getclientlocks(self, line):
        '''
        Prints the list of locks hold by the client . Example below:
        getclientlocks <client-id>
        '''
        clientId = default_client
        els = re.split('\s+', line) 
        if len(els) >= 1:
            clientId = els[0]
        if clientId == '':
            clientId = default_client
        print clientId
        clientLocks = self.lclient.getClientLocks(clientId)
        print clientLocks

    def emptyline(self):
        pass

    def default(self, line):
        out = ''
        if line is not None:
            outs = re.split('\s+', line)
            out = outs[0]
        print 'Unrecognized command ' + out

if __name__ == '__main__':
    cmd.Cmd.prompt = 'distlockcli> '
    LockServiceSehell('127.0.0.1', 9090).cmdloop()
