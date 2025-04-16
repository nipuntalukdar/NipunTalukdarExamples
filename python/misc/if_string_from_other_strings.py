def iffrom_otherstrings(long, strs):
  my_strs = [a for a in strs if len(a) > 0]
  my_strs = list(set(my_strs))

  lengths = set()
  l_s = {}
  for a in my_strs:
    lengths.add(len(a))
    elem = l_s.get(len(a))
    if elem:
      elem.append(a)
    else:
      l_s[len(a)] = [a]

  lengths = list(lengths)
  lengths.sort()
  max_len = lengths[len(lengths) -1]

  if len(long) < lengths[0]:
    return False

  arr = [False] * len(long)
  # Long must start with any of the strings
  indx = -1
  for l in lengths:
    for st in l_s[l]:
      if long.startswith(st):
        arr[l - 1] = True
        if indx == -1:
          indx = l - 1
  if indx == -1:
    return False
  if arr[len(arr) - 1]:
    return True
  indx += 1
  while indx < len(long):
    for l in lengths:
      if (indx - l) < 0:
        break
      if not arr[indx - l]:
        continue
      for a in l_s[l]:
        if a == long[indx - l + 1 : indx + 1]:
          arr[indx] = True
          break
      if arr[indx]:
        break
    indx += 1

  return arr[indx - 1]

def unoptimized(long, strs):
  words = [a for a in strs if a]
  words = set(words)
  if not words:
    if not long:
      return True
    return False
  if not long:
    return False
  dp = [False] * (len(long) + 1)
  dp[0] = True
  for i in range(1, len(long) + 1):
    for j in range(i):
      if dp[j] and long[j:i] in words:
        dp[i] = True
        break

  return dp[len(long)]



print(iffrom_otherstrings("abcxdepqrabcxpqr",  ["abcx", "de", "pqr"]))
print(unoptimized("abcxdepqrabcxpqr",  ["abcx", "de", "pqr"]))


