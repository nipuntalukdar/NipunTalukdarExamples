'''
Created on Feb 18, 2013

@author: root
'''
import sys
from pycassa.types import *                                       
from pycassa.pool import ConnectionPool                           
from pycassa.system_manager import *                              
from pycassa.cassandra.ttypes import *
import uuid                            
from pycassa.columnfamily import ColumnFamily

class PlatFormTables:
    def __init__(self, keyspacename, serverport):
        self.serverport = serverport
        self.keyspace = keyspacename 
        self.sys = SystemManager(self.serverport)   
        self.cfs = self.sys.get_keyspace_column_families(self.keyspace)
        self.keyspacenames = self.cfs.keys()
        self.pool = ConnectionPool(self.keyspace, [ self.serverport ])
        self.column_family = {}
        self.createtables()
        self.reinit_column_family_map()
                                                  
    def reinit_column_family_map(self):
        self.cfs = self.sys.get_keyspace_column_families(self.keyspace)
        self.keyspacenames = self.cfs.keys()
        self.pool = ConnectionPool(self.keyspace, [ self.serverport ] )
        self.column_family = {}
        for ks in self.keyspacenames:
            self.column_family[ks] = ColumnFamily(self.pool, ks)
        self.column_family['SimpleTable']._set_key_validation_class(IntegerType())
        self.column_family['Threads']._set_key_validation_class(IntegerType())
        self.column_family['UserThreads']._set_key_validation_class(IntegerType())
        self.column_family['ThreadObjects']._set_key_validation_class(IntegerType())
        self.column_family['Objects']._set_key_validation_class(UUIDType())
        self.column_family['ThreadHolds']._set_key_validation_class(IntegerType())
        self.column_family['ObjectHistory']._set_key_validation_class(UUIDType())
                    
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
        kysps = self.keyspacenames[:]
        for cfname in kysps:                                
            ret = self.drop_cf(cfname)   
            if ret:                           
                dropcount += 1           
                dropped.append(cfname)                                    
        return dropcount                                                 

    def drop_cf(self, cfname):
        try:                  
            print("Dropping " + cfname)
            self.sys.drop_column_family(self.keyspace, cfname)
            x = self.keyspacenames.index(cfname)              
            self.keyspacenames[x: x + 1] = [] 
            del self.column_family[cfname]                
        except InvalidRequestException as e:                  
            print("ERROR "  + e.why)                          
            return False                                      
        return True
    
    def add_to_simple_table(self):
        thread_id = 1
        self.column_family['SimpleTable'].insert(thread_id, {( 1, 2) :'2'})
        print(self.column_family['SimpleTable'].get(1)) 
    def add_thread_objects(self):
        thread_id = 1
        channel_id = 2
        nw_id = 25
        date_val = time.time()
        object_id = uuid.uuid4()
        self.column_family['ThreadObjects'].insert(thread_id, {(channel_id, nw_id, date_val \
                                                                 ,object_id): '' })

    def createtables(self):
        # Create the table for User's thread row key = UserID=integer
        # Column key date, channel, network,
        # threadid is the value
        print("Creating Userthreads table")
        comparator = CompositeType(DateType(), IntegerType(), IntegerType())
        self.create_cf(comparator, 'UserThreads')
    

        #Thread table Row Key=create date, DateType
        #Column key = ChannelId, NwId, ThreadId 
        
        print("Creating Thread table")
        comparator = CompositeType(IntegerType(),IntegerType(), IntegerType())
        self.create_cf(comparator, 'Threads')
        
        # ThreadObjects table
        # ThreaObjects , row key = Thread Id, Integer 
        # create_date, object id as column key
        
        print("Creating ThreadObjects table")
        comparator = CompositeType(DateType(), UUIDType()) 
        self.create_cf(comparator, 'ThreadObjects')
    
        # Objects table will hold the object data
        # Primary key will be object id
        # channel id, networkid, createdate, body, object type, owner, parent objectid, history,
        # threads
    
        print("Creating Objects table")
        comparator = UUIDType()
        self.create_cf(comparator, 'Objects')
    
        #ThreadHolds 
        # row key = Integer
        # column key date: user id
        # value end_date
    
        print("Creating Thread Hold table")
        comparator = CompositeType(DateType(), IntegerType())
        self.create_cf(comparator, 'ThreadHolds')
        
        # Object History
        # Date is row key is object id
        # Column is date, value is the body
        
        print("Creating ObjectHistory")
        comparator = CompositeType(DateType(), IntegerType())
        self.create_cf(comparator, 'ObjectHistory')
        
        #Object History
        # Date is rowkey is object id
        # Column is date, value is the body
        
        print("Creating simple table")
        
        comparator = CompositeType(IntegerType(), IntegerType())
        self.create_cf(comparator, 'SimpleTable')            
        self.reinit_column_family_map()
        
def main():
    serverport = '127.0.0.1:9160'
    if len(sys.argv) >= 2:
        serverport = sys.argv[1]
    pf = PlatFormTables('KeySpaceCustomer1', serverport)
    pf.createtables()
    pf.add_to_simple_table()
    pf.add_thread_objects()

if __name__ == '__main__':
    main() 
