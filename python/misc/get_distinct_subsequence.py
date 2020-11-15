'''
Let us assume the source string is S='aabaab' and target string is
T='ab'. Index of the first char is 0 and last char is 5 in S.
Now, till index 1, we have 2 occurences of 'a', but no occurrence of
'b'. So, till index 1, there cannot be any occurrences of 'ab'.  At
index 1, we have the first occurrence of 'b' and it can be combined
with the previous 2 occurrences of b (we have 2 occurrences of b till
index 2) and hence we get 2 'ab' till index 2. 

Now we get 2nd  occurrence of b at index 5 
and before index 5 there are 4 occurrences of 'a', 
that means the 'b' at index 5 can be combined with 4 'a's and hence,
this 'b' can result in 4 selection of 'ab'. 
Remember, the 'b' at index 2 can also result in 2 different selections
of 'ab',
and hence the total disting subsequences of 'ab' will be 2 + 4 = 6.

'''


def get_distinct_subsequence(source, target):
    if source is None:
        return 0
    if len(target) > len(source):
        return 0
    if len(target) == len(source):
        if target != source:
            return 0
        return 1

    matches = []
    i = 0
    while i < len(target):
        matches.append([0] *len(source))
        i += 1

    j = 0

    while j < len(target):
        row = matches[j]
        i = 0
        while i < len(source):
            if target[j] ==  source[i]:
                if j == 0:
                    if i > 0:
                        row[i] = row[i - 1 ] + 1
                    else:
                        row[i] = 1
                else:
                    if i > 0:
                        row[i] = matches[j - 1][i - 1] + row[i-1]
                    else:
                        row[i] = 0
            else:
                if i > 0:
                    row[i] = row[i - 1]
                else:
                    row[i] = 0

            i +=1

        j += 1
    
    return matches[j - 1][i-1]


print(get_distinct_subsequence('aababb', 'aab'))
print(get_distinct_subsequence('aabaab', 'ab'))
