'''
Demonstrates the algorithm to find the longest common subsequence between two
substrings.
The algorithm works by starting at the last elements of both sequences.
Let us assume that last elements matches. Then, the last two elements will
be in the longest common sequence, and then the LCS will be, 1 + lcs(seq1[:length(seq1) -1],
seq2[:length(seq2) -1)

Else, the LCS will be:
    max(lcs(seq1, seq2[:length(seq2) -1]), lcs(seq1[:length(seq1)-1], seq2))

The above approach gives the length of the LCS, but we can easily extract the sequence itself,
as showon in the below program
'''

def lcs(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    if l1 == 0 or l2 == 0:
        return 0, []
    if s1[l1 -1] == s2[l2 -1]:
        len1, c1 = lcs(s1[:l1 - 1], s2[:l2 -1])
        return len1 + 1, c1 +  [s1[l1-1]]
    else: 
        len1, c1 = lcs(s1, s2[:l2 -1])
        len2, c2 = lcs(s1[:l1 -1], s2)
        if len1 > len2:
            return len1, c1
        else:
            return len2, c2

print(lcs('aghjbjklcghh', 'gdannbc'))
