def parent(i):
    return (i - 1)/2

def sibling(i, max):
    if i == 0:
        return None
    if i % 2 == 0:
        return i - 1
    if i + 1 > max:
        return None
    return i + 1

def lchild(x, mx):
    ret = 2 * x + 1
    if ret > mx:
        return None
    return ret

def rchild(x, mx):
    ret = 2 * x + 2
    if ret > mx:
        return None
    return ret

def correct_sub_heap(pos, mx, arr):
    lch = lchild(pos, mx)
    rch = rchild(pos, mx)
    if not lch:
        return
    mvl = pos
    if lch and arr[mvl] < arr[lch]:
        mvl = lch 
    if rch and arr[mvl] < arr[rch]:
        mvl = rch
    if mvl != pos:
        arr[mvl], arr[pos] = arr[pos], arr[mvl]
        correct_sub_heap(mvl, mx, arr)

def correct_sub_min_heap(pos, mx, arr):
    lch = lchild(pos, mx)
    rch = rchild(pos, mx)
    if not lch:
        return
    mvl = pos
    if lch and arr[mvl] > arr[lch]:
        mvl = lch 
    if rch and arr[mvl] > arr[rch]:
        mvl = rch
    if mvl != pos:
        arr[mvl], arr[pos] = arr[pos], arr[mvl]
        correct_sub_min_heap(mvl, mx, arr)

def max_heapify(arr):
    if len(arr) <= 1:
        return
    mx = len(arr) - 1
    i = mx
    while i  > 1:
        p = parent(i)
        correct_sub_heap(p, mx, arr)
        i -= 1

def min_heapify(arr):
    if len(arr) <= 1:
        return
    mx = len(arr) - 1
    i = mx
    while i  > 1:
        p = parent(i)
        correct_sub_min_heap(p, mx, arr)
        i -= 1

def is_max_heap(arr):
    i = 0
    while i < len(arr):
        lch = lchild(i, len(arr) - 1)
        if not lch:
            i += 1
            continue
        if arr[i] < arr[lch]:
            return False
        rch = rchild(i, len(arr) - 1)
        if not rch:
            i += 1
            continue
        if arr[i] < arr[lch]:
            return False
        i += 1
    return True

def is_min_heap(arr):
    i = 0
    while i < len(arr):
        lch = lchild(i, len(arr) - 1)
        if not lch:
            i += 1
            continue
        if arr[i] > arr[lch]:
            return False
        rch = rchild(i,len(arr) - 1)
        if not rch:
            i += 1
            continue
        if arr[i] > arr[lch]:
            return False
        i += 1
    return True

def heapsort(arr):
    max_heapify(arr)
    pos = len(arr) - 1
    while pos > 0:
        arr[0], arr[pos] = arr[pos], arr[0]
        pos -= 1
        if pos == 0:
            break
        correct_sub_heap(0, pos, arr)


x = [100,200, 50, 30, 20, 210, 60, 80, 90, 70, 40, 400, 1]
print x, 'is min heap? ', is_min_heap(x)
max_heapify(x)
if is_max_heap(x):
    print 'Below is a max heap'
print x
min_heapify(x)
if is_min_heap(x):
    print 'Below is a min heap'
print x
heapsort(x)
print 'Sorted', x
max_heapify(x)
if is_max_heap(x):
    print 'Below is a max heap'
print x
heapsort(x)
print 'Sorted', x
