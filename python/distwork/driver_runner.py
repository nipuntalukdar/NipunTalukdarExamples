from distwork.redis_stream import RedisStream
from distwork.dumpload import DumpLoad
from random import randint


def my_fun(x:int =1 , y:int =2):
  print("Hello", x, y)
  return f"{ x + y }"

rs = RedisStream()
for i in range(2):
  work = DumpLoad.dumpfn(my_fun, *(randint(1,100), randint(2,300)), **{})
  rs.enqueue_work({'work' : work})
