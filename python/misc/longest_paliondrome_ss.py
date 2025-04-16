'''
let us take a substring, if the first and last char of the substring are equal, then they will be
part of the longest paliondrome of the substring between them.
I.e.
let us take the string a[i:j+1]
if a[i] == a[j],
then a[i] and a[j] will be part of max paliondrome which can be formed
from a[i+1:j]
and the lenght of the paliondrome will be
2 + lengh_of_max_paliondrome_of (a[i:1:j]
,
if they are not equal, then  max paliondrom of a[i:j + 1] is 
equal to max paliondrome of a[i: j]
'''


def lps(inp):
  n = len(inp)
  if n < 2:
    return n
  psl = [[0] * n for _ in range(n)]

  for i in range(n):
    psl[i][i] = 1

  max_ps = 1

  for i in range(1, n):
    for j in range(i):
      if inp[j] == inp[i]:
        if i == j + 1 and psl[i][j] < 2:
          psl[i][j] = 2
        else:
          psl[i][j] = psl[i-1][j+1] + 2
      else:
        psl[i][j] = psl[i-1][j] 
      max_ps =  max(psl[i][j], max_ps)
  return max_ps
  


print(lps("aba"))
print(lps("bbbabcdcba"))

          

