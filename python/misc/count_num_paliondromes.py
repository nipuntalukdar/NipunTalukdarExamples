def count_num_pd(st):
  n = len(st)
  if n <= 1:
    return n
  if n == 2:
    if st[1] == st[0]:
      return 3
    return 2

  pd = [[False] * n for _ in range(n)]
  count = n
  for i in range(n):
    pd[i][i] = True
    if  i <= n -2 and st[i] == st[i+1]:
      pd[i][i+1] = True
      count += 1

  for length in range(3, n+1):
    for i in range(n - length + 1):
      j = i + length - 1
      if st[i] == st[j] and pd[i+1][j - 1]:
        pd[i][j] = True
        count += 1
  return count


print(count_num_pd("abc"))
print(count_num_pd("abcc"))
print(count_num_pd("aaa"))
print(count_num_pd("aaaa"))
print(count_num_pd("abcba"))




