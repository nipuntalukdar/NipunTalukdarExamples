from copy import copy

def min_grid_path(grids):
    row  = len(grids)
    col = len(grids[0])

    cost_grid = copy(grids)

    for i in range(1,col):
        cost_grid[0][i] += cost_grid[0][i-1]
    for i in range(1,row):
        cost_grid[i][0] += cost_grid[i-1][0]

    for i in range(1, row):
        for j in range(1, col):
            cost_grid[i][j] += min(cost_grid[i-1][j], cost_grid[i][j-1])

    return cost_grid[row-1][col-1]

print(min_grid_path([[1,3,1],[1,5,1],[4,2,1]]))
print(min_grid_path([[1,2,3],[4,5,6]]))



