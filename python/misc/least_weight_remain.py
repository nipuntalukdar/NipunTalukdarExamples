from copy import copy
from typing import List

'''
You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. 
On each turn, we choose any two stones and smash them together. 
Suppose the stones have weights x and y with x <= y. The result of this smash is:

    If x == y, both stones are destroyed, and
    If x != y, the stone of weight x is destroyed, and the stone of weight y 
    has new weight y - x.

At the end of the game, there is at most one stone left.

Return the smallest possible weight of the left stone. If there are no stones left, return 0.

---
Always smash the two heaviest stones together

'''

def list_wt(arr : List[int]) -> int:
  if len(arr) == 0:
    return 0
  if len(arr) == 1:
    return arr[0]
  if len(arr) == 2:
    return abs(arr[1] - arr[2])

  arr.sort()
  while True:
    if not arr:
      return 0
    position = len(arr) -1
    if position == 0:
      return arr[0]
    if position == 1:
      return abs(arr[1] - arr[0])
    if arr[position] == arr[position - 1]:
      arr.pop()
      arr.pop()
    else:
      arr[position - 1] = arr[position] - arr[position -1]
      arr.pop()
      arr.sort()
a1 = [1,2,3]
a2 = [4,1,1,1]
a3 = [4,1,1,2]
a4 = [4,1,1,1,1]

for a in [a1, a2, a3, a4]:
  print(a, list_wt(copy(a)))


