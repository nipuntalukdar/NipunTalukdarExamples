'''
There is a robot on an m x n grid. 
The robot is initially located at the top-left corner 
(i.e., grid[0][0]). The robot tries to move to the bottom-right corner 
(i.e., grid[m - 1][n - 1]). The robot can only move either down or right at 
any point in time.
Given the two integers m and n, return the number of possible unique paths 
that the robot can take to reach the bottom-right corner.

'''
def unique_ways(row, col):
  unq = [[0] *col for _ in range(row)]
  for i in range(col):
    unq[0][i] =1
  for i in range(row):
    unq[i][0] =1

  for i in range(1, row):
    for j in range(1, col):
      unq[i][j] = unq[i-1][j] + unq[i][j-1]
  return unq[row-1][col-1]

print(unique_ways(3,3))
print(unique_ways(3,7))

