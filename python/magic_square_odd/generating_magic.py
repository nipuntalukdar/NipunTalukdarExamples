from copy import deepcopy

def get_magic(order):
    if order == 1:
        return [1]
    if order % 2 != 1:
        return None
    i = 0
    out = []
    while i < order:
        out.append([None] * order)
        i += 1

    i , j =  0, order/2
    current = 1
    laste = order * order
    while current != laste + 1:
        out[i][j] = current
        current += 1
        nextj = (j + 1) % order
        nexti = i - 1
        if nexti == -1:
            nexti = order - 1
        if out[nexti][nextj] == None:
            i, j = nexti, nextj
        else:
            i = i + 1
    return out

def verify_magic(magic):
    val = None
    order = len(magic)
    for a in magic:
        newval = sum(a)
        if val is None:
            print 'Value is', newval
            val = newval
        elif newval != val:
            return 'Invalid'
    
    i, j = 0, 0
    while j < order:
        newval = 0
        while i < order:
            newval += magic[i][j]
            i += 1
        if newval != val:
            return 'Invalid'
        j += 1
        i = 0
    i, j = 0, 0
    newval = 0
    while i < order:
        newval += magic[i][j]
        i += 1
        j += 1
    if newval != val:
        return 'Invalid'
    i, j = 0,  order - 1
    newval = 0
    while i < order:
        newval += magic[i][j]
        i += 1
        j -= 1
    if newval != val:
        return 'Invalid'

    return 'Valid'


def get_path(start_col, end_col, start_row, end_row):
    path = []
    i = start_col
    row = start_row
    while i <= end_col:
        path.append((row, i))
        i += 1

    col = end_col
    i = start_row + 1
    while i <= end_row:
        path.append((i, col))
        i += 1
    
    i = end_col - 1
    while i >= start_col:
        path.append((end_row, i))
        i -= 1

    col = start_col
    i = end_row - 1
    while i >= start_row + 1:
        path.append((i, col))
        i -= 1
    return path

def printmagic(magic):
    print 'Magic'
    for a in  magic:
        a = ['{:4d}'.format(x)  for x in a ]
        print ' '.join(a)

def rotate_place(magic, start_col, end_col, start_row, end_row, howmany_places):
    paths = get_path(start_col, end_col, start_row, end_row)
    
    tmp1, tmp2, tmp3 = None, None, None
    i = 0

    tmps = []
    i = 0
    while i < howmany_places:
        tmps.append(magic[paths[i][0]][paths[i][1]])
        i += 1
    i = 0
    while i <= len(paths) - 1:
        dest = (i + howmany_places) % len(paths)
        tmps.append(magic[paths[dest][0]][paths[dest][1]])
        magic[paths[dest][0]][paths[dest][1]] = tmps.pop(0)
        i += 1

def reflect_magic(magic, num_rows):
    i = 0
    j = num_rows - 1
    while i < j:
        k = 0
        while k < len(magic[i]):
            magic[i][k], magic[j][k] = magic[j][k], magic[i][k]
            k += 1
        i += 1
        j -= 1

magic = get_magic(3)

magics = [magic]
rplaces = [2, 4, 6]
for rplace in rplaces:
    newmagic = deepcopy(magic)
    rotate_place(newmagic, 0, 2, 0, 2, rplace)
    magics.append(newmagic)

reflected_magics = []
for newmagic in magics:
    newmagic = deepcopy(newmagic)
    reflect_magic(newmagic,3)
    reflected_magics.append(newmagic)

for m in reflected_magics:
    magics.append(m)
    
def get_min_cost(given_matrix, magics):
    min_cost = None
    row = len(given_matrix)
    col = len(given_matrix[0])
    for tmp_m in magics:
        i = 0
        j = 0
        this_cost = 0
        while i < row:
            j = 0
            while j < col:
                this_cost += abs(tmp_m[i][j] - given_matrix[i][j])
                j += 1
            i += 1
        if this_cost == 0:
            return 0
        if min_cost is None:
            min_cost = this_cost
        if this_cost < min_cost:
            min_cost = this_cost
    return min_cost
