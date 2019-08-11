from random import randint
import sys

def find_in_sorted(sorted_array, elem):
    start = 0
    end = len(sorted_array) -1 
    while True:
        if sorted_array[start] == elem:
            return start
        if sorted_array[start] > elem:
            return -1
        if sorted_array[end] < elem:
            return -1
        if start == end:
            return -1
        nend = start + ((end - start) / 2)
        if sorted_array[nend] == elem:
            return nend
        elif sorted_array[nend] > elem:
            end = nend - 1
        else:
            start = nend + 1

count = 2
if len(sys.argv) > 1:
    count = int(sys.argv[1])

x = [randint(100, 10000) for a in range(count)]
x.sort()
print x
print 'Below should print from 0 to {}'.format(count -1)
i = 0
while i < count:
    print find_in_sorted(x, x[i])
    i +=1 

