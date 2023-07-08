import asyncio
import time

from tornado.ioloop import PeriodicCallback


async def main() -> None:
    await asyncio.sleep(1, '1')


async def say_hello(t, what) -> None:
    await asyncio.sleep(t)
    print(t)

def fun() -> None:
    print(1)

class A:
    def __init__(self):
        self.__val__ = 1
    def show(self):
        print(self.__val__)
        self.__val__ += 1

async def main() -> None:
    print(time.time())
    t1 = asyncio.create_task(say_hello(1, 'hi'))
    t2 = asyncio.create_task(say_hello(30, 'world'))
    await t1
    print(time.time())
    pc = PeriodicCallback(A().show, 2000)
    pc.start()
    await t2


if __name__ == '__main__':
    asyncio.run(main(), debug=True)

