'''
Given two strings word1 and word2, return the minimum number 
of steps required to make word1 and word2 the same.

In one step, you can delete exactly one character in either string.

find the longest common sequence of the two strings and minimum deletion will
be :
   len(l1) - lcs  + len(2) -lcs
'''

def lcs(l1, l2):
  if len(l1) == 0 or len(l2) == 0:
    return 0
  if len(l1) ==1:
    if l2.find(l1[0]) != -1:
      return 1
    return 0
  if len(l2) ==1:
    if l1.find(l2[0]) != -1:
      return 1
    return 0

  m = len(l2)
  n = len(l1)
  long = [[0] * (m + 1) for _ in range(n + 1)]

  for i in range(1, n+1):
    for j in range(1, m + 1):
      if l1[i - 1] == l2[j - 1]:
        long[i][j] = long[i-1][j-1] + 1
      else:
        long[i][j] = max(long[i-1][j], long[i][j-1])
  return long[n][m]


def min_delete(l1, l2):
  return len(l1) + len(l2) - 2 * lcs(l1,l2)

print(min_delete("sea", "eat"))
print(min_delete("leetcode", "etco"))
