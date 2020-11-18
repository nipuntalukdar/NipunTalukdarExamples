'''
Given A, B, C, find whether C is formed by the interleaving of A and B.

Example:
1:
  A = "ab"
  B = "cd"
  C = "acdb"
  Here, C can be formed by the interleaving of A and B

2:
  A = "ab"
  B = "cd"
  C = "adbc"
  Here, C cannot be formed by the interleaving of A and B
  as 'd' and 'c' are coming out of orders in C.

2:
  A = "ab"
  B = "cd"
  C = "acd"
  Here, C cannot be formed by the interleaving of A and B
  as 'b' is missing in C

'''

def is_interleaving(first, second, interleaved):
    if len(first) + len(second) != len(interleaved):
        return False;
    if len(first) == 0:
        return second == interleaved
    if len(second) == 0:
        return first == interleaved

    # interleaved must start with 0th char of first or second string
    if not first[0] == interleaved[0]  and not second[0] == interleaved[0]:
        return False


    i = len(first) + 1
    j = len(second) + 1

    k = 0
    matrix = []
    while k < j:
        matrix.append([False] * i)
        k += 1

    # 0 char from first, 0 char from second is equal 0
    # char from interleaved
    matrix[0][0] = True


    # Now check how much of interleaved string can be formed 
    # by using 0 char from second and all others from first

    k = 1
    while k < i:
        if matrix[0][k - 1] and  (first[k - 1] == interleaved[k - 1]):
            matrix[0][k] = True
        else:
            break
        k += 1
    
    # Now check how much of interleaved string can be formed 
    # by using 0 char from first and all others from second

    k = 1
    while k < j:
        if matrix[0][0] and  (second[k - 1] == interleaved[k - 1]):
            matrix[k][0] = True
        else:
            break
        k += 1

    # Now we successively find out if interleaved[:n+m] can be formed
    # by interleaving first n chars from first and m chars from second
    # m varies from 1 to len(first)
    # n varies from 1 to len(second)
    # When we are on xth row of the matrix, we are actually trying to
    # check if (x - 1) chars from second string have been already seen,
    # and for that to happen, x - 2 chars have to be already present
    # in some prefix of interleaved. 

    k = 1
    ksecond_matched = False
    while k < j:
        #checking for a prefix of interleaved which can be formed
        #with k chars from second 
        l = 1
        ksecond_matched = matrix[k][0]
        while l < i:
            if not ksecond_matched:
                if matrix[k-1][l] and interleaved[k + l - 1] == second[k-1]:
                    matrix[k][l] = True
                    ksecond_matched = True
            else:
                # we have already matched k chars from second, check if a prefix
                # of length k + x can be obtained which is interleaved with
                # first k and x chars from second and first respectively
                if matrix[k][l - 1] and interleaved[k + l - 1] == first[l-1]:
                    matrix[k][l] = True
            l += 1
        k += 1
    
    return matrix[j - 1][i - 1]



test_data = [['a', 'b', 'ab', True],
             ['ab', '', 'ab', True],
             ['abc', 'd', 'abcd', True],
             ['ab', 'cd', 'abcd', True],
             ['ab', 'cd', 'abcde', False],
             ['ab', 'cde', 'aced', False],
             ['ab', 'cde', 'abcd' , False],
             ['ab', 'cde', 'aecdb', False],
             ['ab', 'cde', 'abcde', True]]


for row in test_data:
    if is_interleaving(row[0], row[1], row[2]) != row[3]:
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Failed for ', row
    else:
        print 'Passed for', row
