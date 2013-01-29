#-------------------------------------------------------------------------------
# Name:        getalluniquesubstr
# Purpose:
#
# Author:      NTalukdar
#
# Created:     29-01-2013
# Copyright:   (c) NTalukdar 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# get all the unique substrings of inputstr
def get_unique_substrings(inputstr, uniqsubstrs):
    uniqsubstrs.add(inputstr)
    i = 0
    length = len(inputstr)
    while i < length:
        substr1 = inputstr[i:]
        j  = len(substr1)
        k = j
        while k >= 1:
            substr2 = substr1[:k]
            print(substr2)
            if substr2 not in uniqsubstrs:
                uniqsubstrs.add(substr2)
            k -= 1
        i +=1

#example Run
allunique_substr = set()
get_unique_substrings("abccc", allunique_substr)
print(allunique_substr)
