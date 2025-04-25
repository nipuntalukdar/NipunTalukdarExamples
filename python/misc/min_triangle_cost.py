def min_triangle_cost(vals):
  if len(vals) < 3:
    return 0
  if len(vals) == 3:
    return vals[0] * vals[1] * vals[2]
  
  n = len(vals)
  dp = [[0] * n for _ in range(n)]
  for lenght in range(3, n + 1):
    for i in range(n - lenght + 1):
      j = i + lenght - 1
      dp[i][j] = float('inf')
      for k in range(i + 1, j):
        dp[i][j] = min(dp[i][j],  dp[i][k] + dp[k][j] + vals[i] * vals[j] * vals[k])

  return dp[0][n-1] 

print(min_triangle_cost([1, 3, 1, 4, 1, 5]))
