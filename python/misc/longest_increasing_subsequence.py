def liss(lst):
  if len(lst) <= 1:
    return len(lst)

  longest_ss = [1] * len(lst)
  i = 1
  lcs_still = 1
  for i in range(1, len(lst)):
    for j in range(i):
      if lst[j] < lst[i]:
        longest_ss[i] = max(longest_ss[i], longest_ss[j] + 1)
        if longest_ss[i] > lcs_still:
          lcs_still = longest_ss[i]

  return lcs_still

print(liss([1,2,1,2, 1, 4, 2, 6]))
print(liss([1,2,1,1,1,1,1,3,4]))
