from pycassa.types import *
from pycassa.pool import ConnectionPool
from pycassa.system_manager import *
from pycassa.cassandra.ttypes import *

mysys = SystemManager()
try: 
    comparator = CompositeType(LongType(reversed=True), AsciiType())
    mysys.create_column_family("demo", "Test3", comparator_type=AsciiType())
    mysys.create_column_family("demo", "MyTest", comparator_type=comparator)

    # Create the table for User's thread
    comparator = CompositeType(LongType(reversed=True), AsciiType())

except InvalidRequestException as e:
    print("ERROR "  + e.why)
