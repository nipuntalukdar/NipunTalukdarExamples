def left(r, c, grid):
    if c > 0:
        return r, c -1
    return None


def right(r, c, grid):
    if c < len(grid[0]) - 1:
        return r, c + 1
    return None

def up(r, c, grid):
    if r > 0:
        return r - 1, c
    return None

def down(r, c, grid):
    if r < len(grid) - 1:
        return r + 1, c
    return None

def max_from(i, j, dp, grid):
    if dp[i][j]:
        return
    l = left(i,j, dp)
    r = right(i,j, dp)
    u = up(i,j, dp)
    d = down(i,j, dp)
    dp[i][j] = 1
    
    max_val = 0
    for x in l, r, d, u:
        if x and grid[i][j] < grid[x[0]][x[1]]:
            if not dp[x[0]][x[1]]:
                max_from(x[0], x[1], dp, grid)
            max_val = max(max_val, dp[x[0]][x[1]])
    dp[i][j] += max_val


        
    

def longest_incr_path(grid):
    row = len(grid)
    col = len(grid[0])
    
    dp = [[0] * col for _ in range(row)]

    for i in range(row):
        for j in range(col):
            if dp[i][j]:
                continue
            max_from(i, j, dp, grid)
    mx = 1
    for r in dp:
        mx = max(mx, max(r))
    return mx

x = [[9,9,4],[6,6,8],[2,1,1]]
print(longest_incr_path(x))
x = [[3,4,5],[3,2,6],[2,2,1]]
print(longest_incr_path(x))
