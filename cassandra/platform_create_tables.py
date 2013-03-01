from pycassa.types import *
from pycassa.pool import ConnectionPool
from pycassa.system_manager import *
from pycassa.cassandra.ttypes import *

mysys = SystemManager()

class PlatFormTables:
    def __init__(self, keyspacename):
        self.keyspace = keyspacename
        self.sys = SystemManager()
        self.cfs = self.sys.get_keyspace_column_families(self.keyspace)
        self.keyspacenames = self.cfs.keys()
    def create_cf(self, comparator, cfname):
        try: 
            if cfname in self.keyspacenames:
                print("CF " + cfname +  " is already there")
                return True
            self.sys.create_column_family(self.keyspace, cfname, comparator_type = comparator)
            self.keyspacenames.append(cfname)
        except InvalidRequestException as e:
            print("ERROR "  + e.why)
            return False
        except NameError as e:
            print("ERROR "  + e.why)
            return False
        print("CF " + cfname + " created")
        self.keyspacenames.append(cfname)
        return True

    def drop_all_cfs(self):
        dropcount = 0
        dropped = []
        print (self.keyspacenames)
        for cfname in self.keyspacenames:
            print (cfname)
            continue
            ret = self.drop_cf(cfname)
            if ret:
                print("I am here")
                dropcount += 1
                dropped.append(cfname)
        remaining = [ x for x in self.keyspacenames if x not in dropped ]
        self.keyspacenames = remaining 
        return dropcount

    def drop_cf(self, cfname):
        try:
            print("Dropping " + cfname)
            self.sys.drop_column_family(self.keyspace, cfname)
            x = self.keyspacenames.index(cfname)
            self.keyspacenames[x: x + 1] = []
        except InvalidRequestException as e:
            print("ERROR "  + e.why)
            return False
        return True

def main():
    pf = PlatFormTables('KeySpaceCustomer1')
    pf.drop_all_cfs()
    exit(1)
    # Create the table for User's thread
    # Userid, date, channel, network is the key, 
    # threadid is the value
    print("Creating Userthreads table")
    comparator = CompositeType(IntegerType(), DateType(), IntegerType(), IntegerType())
    pf.create_cf(comparator, 'UserThreads')
    
    #Thread table will have channelid,networkid, createdate, threadid,
    #as the primary key
    print("Creating Thread table")
    comparator = CompositeType(IntegerType(), IntegerType(), IntegerType(), DateType(), UUIDType())
    pf.create_cf(comparator, 'Threads')

    # ThreadObjects table will contain Threadid, channelid, networkid, object
    # create date as the primary key
    #
    print("Creating ThreadObjects table")
    comparator = CompositeType(IntegerType(), IntegerType(), \
            IntegerType(),DateType(),UUIDType())
    pf.create_cf(comparator, 'Objects')
     

    #Objects table will hold the object data
    # Primary key will be object id, channel id, networkid, createdate, values are object
    # creator, body data, lastmode date, delete date, parent object id etc

    print("Creating Objects table")
    comparator = CompositeType(UUIDType(), IntegerType(), IntegerType(), DateType())
    pf.create_cf(comparator, 'Objects')

    # Threadhold table will have data for thread holds
    # Primary key will be thread id, channel id, networkid, values are 
    # object hold date range and correponding users holding it
    # Primary Key is Threadid, channelId, Network Id, 

    print("Creating Thread Hold table")
    comparator = CompositeType(IntegerType(), IntegerType(), IntegerType(), DateType(), DateType())
    pf.create_cf(comparator, 'ThreadHolds')
     

main()
