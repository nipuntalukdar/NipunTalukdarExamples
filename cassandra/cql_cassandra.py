import sys
from cqlshlib import tfactory
import cql

class CassandraOperations:
    def __init__(self, host, port, keyspace):
        try:
            self.host = host
            self.port = port
            self.keyspace = keyspace
            self.transport = tfactory.regular_transport_factory('127.0.0.1', 9160, None, None)
            self.con = cql.connect('127.0.0.1', 9160,  cql_version='3', transport=self.transport) 
            self.cursor = self.con.cursor()
            self.cursor.execute('USE ' + self.keyspace + ' ;');
        except cql.ProgrammingError as e:
            print e.args 
            sys.exit(1)
    
    def table_exists(self, keyspacename, tablename):
        try:
           statement = 'select columnfamily_name from system.schema_columnfamilies ' + \
                'where keyspace_name=\'' + keyspacename + '\';'
           self.cursor.execute(statement)
           result = self.cursor.fetchmany(2)
           if (len(result) < 1) or (tablename not in result[0]):
               return False
           return True
        except cql.ProgrammingError as e:
            print e.args
            raise
    def __del__(self):
        self.cursor.close()
        self.con.close()
        self.transport.close()
    
    def create_table(self, tablename, statement):
        try:
            if self.table_exists(self.keyspace, tablename):
                print 'Already exists'
                return False
            self.cursor.execute(statement)
        except cql.ProgrammingError as e:
            print e.args
            return False
        return True

def readfile(filename):
    result = None
    try:
        f = open(filename, 'r')
        result = f.read()
        f.close()
    except IOError as e:
        print e.args
    return result
def main():
    cass = CassandraOperations('127.0.0.1', 9160, 'mykeyspace')
    if cass.table_exists('mykeyspace', 'mytable'):
        print 'Exists'
    tablecreate = readfile('createtables.txt')
    if tablecreate is not None:
        cass.create_table('mytable2', tablecreate)
    else:
        print 'Some problem in creating table'
    
     
main()
