from random import randint

dividends = []
divisors = ['2', '3', '4', '6', '12', '-2', '-3', '-4', '-12']

for i in range(20):
    x = 0
    while True:
        x = randint(-15, 15)
        if x == 0:
            continue
        break
    x = x * 12
    if x < 0:
        dividends.append('({})'.format(x))
    else:
        dividends.append(str(x))
x = 1
print '***************************************'
print ''
while x < 11:
    x += 1
    print '   {} divided by {}'.format(dividends[randint(0, len(dividends) -1)], 
        divisors[randint(0,len(divisors) -1)])
    print ''
