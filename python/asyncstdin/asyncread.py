import sys
import math
from concurrent.futures import ProcessPoolExecutor
import asyncio

async def connect_stdin_stdout():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader
def is_prime(res):
    try:
        inp = abs(int(res))
        num = int(math.sqrt(inp))
        if inp == 1:
            return False, False
        if inp & 1 == 0:
            return False, False
        i = 3
        while i <= num:
            if inp % i == 0:
                return False, False
            i += 2
        return True, False
    except ValueError:
        return None, True


async def process_in(thenumber, pool):
    loop = asyncio.get_running_loop()
    res, error = await loop.run_in_executor(pool, is_prime, thenumber)
    if error:
        print("Error in input")
        return False
    elif res:
        print(f"Prime {thenumber}", )
        return True
    else:
        print(f"Not prime {thenumber}")
        return False

async def main(pool):
    reader = await connect_stdin_stdout()
    while True:
        res = await reader.read(100)
        res1 = await process_in(res, pool)



if __name__ == '__main__':
    pool = ProcessPoolExecutor()
    asyncio.run(main(pool))


