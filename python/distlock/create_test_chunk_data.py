#/usr/bin/env python

from struct import pack
import random
from io import BytesIO

x = open('out.dump', 'wb')
i = 0
random.seed(10000)
while i < 100:
    i += 1
    cur = random.randint(1, 10000)
    buf = pack('i', cur)
    x.write(buf)
    bio = BytesIO()
    j = 0
    while j < cur:
        j += 1
        bio.write('a')
    bio.seek(0)
    buf = bio.read()
    print cur
    x.write(buf)
x.close()

