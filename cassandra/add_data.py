from pycassa.cassandra.ttypes import *
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

try:
    cp = ConnectionPool("demo")
    cf = ColumnFamily(cp, "Test3")
    cf.insert('2345', 'ss')
    x = cf.get('1234')
    print(x)
except InvalidRequestException as e:
    print("ERROR " + e.why)
except NotFoundException as e:
    print("ERROR " + e.why)

