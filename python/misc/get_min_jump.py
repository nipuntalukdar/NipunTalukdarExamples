'''
Given an array of non-negative integers, A, of length N,
you are initially positioned at the first index of the array.
Each element in the array represents your maximum jump length at 
that position.

Return the minimum number of jumps required to reach the last index.
If it is not possible to reach the last index, return -1.

Soultion:
Start with min cost of moving to just to next position from any position,
then check min cost for going to 'current + 2' position for each 'current'
positon.

Continue checking for each 'current to 'current + j' minimum cost

When we are checking for 'current' to 'current+j' minimum cost, already the
minimum cost for 'current' to 'current+k'  for all current and all k < j
are calculated and they can be used for minumum cost of 
'current' to 'current+j' position.


'''



BIG=999999999999999999999
def get_min_jump(positions):
    pos = len(positions)
    a = []
    i = 0
    while i < pos:
       a.append([BIG] * pos)
       i += 1

    i = 0
    while i < pos:
        a[i][i] = 0
        i += 1


    #start with jump that covers just one step

    jumpto = 1
    i = 0
    end = pos - 2
    while jumpto <= pos  -1:
        i = 0
        while i < pos - jumpto:
            if jumpto == 1:
                if positions[i] >= 1:
                    a[i][i+jumpto] = 1
            else:
                if positions[i] >= jumpto:
                    a[i][i + jumpto] = 1
                else:
                    k = i + 1
                    j = i + jumpto
                    minjump = BIG
                    while k < j:
                        if a[i][k] + a[k][j] < minjump:
                            minjump = a[i][k] + a[k][j]
                        k += 1
                    a[i][j] = minjump
            i += 1
        jumpto += 1
    
    '''
    a[0]pos-1] has the minimum jumps needed to reach the last element

    '''
    if a[0][pos - 1] == BIG:
        return -1
    return a[0][pos - 1]

print(get_min_jump([1,1,0,1]))
print(get_min_jump([1,1,2,1,1]))

