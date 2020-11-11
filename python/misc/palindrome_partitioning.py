'''
Given a string A, partition A such that every substring of 
the partition is a palindrome.
Return the minimum cuts needed for a palindrome partitioning of A.

Solution:
Very similar to the chain matrix multiplication problem.
A string with 1 char has no cost of partitioning, as one
char is always a palindrome.
A sring with 2 chars, may have 0 cost if it is already
a partition, otherwise 1 + 0 + 0 will be the cost as it has to be
partitioned into 2 string with 1 char each which are anyway
palindromes.
For calculting minimum partitioning cost of substring from index
i to j is:
    0 if susbtring from index i to j is already a palindrome.
    Else, find the cut at index k, which make it minimum
    for k = i to j -1.
    So,
    cost[i,j] = 1 + cost[i,k] + cost[k,j] # find k for this
    # also for all substrings with length <  j - i + 1,
    the minimum cost is already calculated.

'''


def ispalindrome(val, start, end):
    if start >= len(val) or end >= len(val):
        return False
    if start > end:
        return False

    i, j = start, end

    while i <= j:
        if val[i] != val[j]:
            return False
        i += 1
        j -= 1

    return True



BIG = 999999999999
def get_min_cut_palidrome_partitioning(inp):
    numel = len(inp)
    if numel <= 1:
        return 0
    cost = []
    i = 0
    while i < numel:
        cost.append([BIG] * numel)
        i += 1

    # single char strings are always palindromem
    # so number of cuts is zero for them
    i = 0
    while i < numel:
        cost[i][i] = 0
        i += 1

    #
    # cost[0][numel - 1] will hold the minimum cost or cuts
    #
    size = 2
    while size <= numel:
        i = 0
        while i <= numel - size:
            if ispalindrome(inp, i, i + size - 1):
                cost[i][i + size -1] = 0
            else:
                mincost = BIG
                k = i
                j = i + size -1
                while k < j:
                    tmpcost = cost[i][k] + cost[k+1][j] + 1
                    if tmpcost < mincost:
                        mincost = tmpcost
                    k += 1
                cost[i][j] = mincost
            i += 1
        size += 1
    return cost[0][numel - 1]


print(get_min_cut_palidrome_partitioning('aaaa'))
print(get_min_cut_palidrome_partitioning('aaa'))
print(get_min_cut_palidrome_partitioning('a'))
print(get_min_cut_palidrome_partitioning('xaay'))
print(get_min_cut_palidrome_partitioning('xaay'))
print(get_min_cut_palidrome_partitioning('axxayaay'))
print(get_min_cut_palidrome_partitioning('axxayyaxxa'))
