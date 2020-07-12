from random import randint

x = 1
while x < 11:
    x += 1
    j = randint(2, 3)
    k = 0
    array = []
    while k < j:
        k += 1
        l = randint(-3, 3)
        if l < 0:
            array.append('({})'.format(l))
        else:
            array.append(str(l))
    print '{} ='.format(' x '.join(array))
    print ''
        
    

