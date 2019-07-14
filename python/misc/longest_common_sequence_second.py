def lcs(a1, a2):
    if type(a1) != list or type(a2) != list:
        raise("Non list passed")
    if len(a1) == 0 or len(a2) == 0:
        return 0, None

    x = len(a1)
    y = len(a2)
    longest = []
    j = 0
    while j <= x:
        longest.append([0] * ( y + 1))
        j += 1
    # all longest[0, j] = 0
    # all longest[i, 0] = 0
    i = 1
    j = 1
    lcmsofar = []
    while i <= x:
        while j <= y:
            if a1[i - 1] == a2[j - 1]:
                longest[i][j] = 1 + longest[i-1][j-1]
            else:
                longest[i][j] = max(longest[i-1][j], longest[i][j-1])
            j +=1 
        j = 1
        i += 1
    i = x
    j = y
    while i >= 1 and j >= 1:
        if longest[i][j] == longest[i -1][j]:
            i -= 1
        elif longest[i][j] == longest[i][j -1]:
            j -= 1
        else:
            #here a1[i-1] belongs to LCS as 
            # longest[i][j] == longest[i-1][j-1] + 1
            lcmsofar = [a1[i-1]] + lcmsofar
            i -= 1
            j -= 1

    return longest[x][y], lcmsofar

first = [1, 2,3,3,3,4]
second = [1,2,3, 4]
lengthcs, cs = lcs(first, second)
print 'First', first
print 'Second', second
print 'LCS lenghth', lengthcs
print 'LCS', cs

