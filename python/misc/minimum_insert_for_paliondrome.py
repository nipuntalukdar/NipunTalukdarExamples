def max_paliondrome_len(st):
  n = len(st)
  if n == 1:
    return 0
  if n == 2:
    if st[0] == st[1]:
      return 0
    return 1
  
  pd = [[False] * n  for _ in range(n)]

  max_p = 1
  for i in range(n):
    pd[i][i] = 1
    if i <= n -2 and st[i] == st[i + 1]:
      pd[i][i+1] = 2
      max_p = 2

  for i in range(2,n):
    for j in range(i):
      if st[j] == st[i]:
        pd[j][i] = pd[j+1][i-1] + 2
      else:
        pd[j][i] = pd[j+1][i-1]
      max_p = max(max_p, pd[j][i])

  return n - max_p



print(max_paliondrome_len("zzazz"))
print(max_paliondrome_len("mbadm"))
print(max_paliondrome_len("leetcode"))
      
