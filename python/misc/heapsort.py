#-------------------------------------------------------------------------------
# Name:        heapsort
# Purpose:
#
# Author:      NTalukdar
#
# Created:     28-01-2014
# Copyright:   (c) NTalukdar 2014
#-------------------------------------------------------------------------------

def rchildi(arr, relpos, i):
    newi = i - relpos
    rindex = 2 * newi + 2 + relpos
    if rindex <= len(arr) - 1:
        return rindex
    return -1

def lchildi(arr, relpos, i):
    newi = i - relpos
    lindex = 2 * newi + 1 + relpos
    if lindex <= len(arr) -1:
        return lindex
    return -1

def max_heapify(arr, relpos, startpos):
    child = lchildi(arr, relpos, startpos)
    if child == -1:
        return
    largest = startpos
    if arr[child] > arr[largest]:
        largest = child
    child = rchildi(arr, relpos, startpos)
    if child != -1 and arr[child] > arr[largest]:
        largest = child
    if largest != startpos:
        arr[largest], arr[startpos] = arr[startpos], arr[largest]
        max_heapify(arr, relpos, largest)

def min_heapify(arr, relpos, startpos):
    child = lchildi(arr, relpos, startpos)
    if child == -1:
        return
    smallest = startpos
    if arr[child] < arr[smallest]:
        smallest = child
    child = rchildi(arr, relpos, startpos)
    if child != -1 and arr[child] < arr[smallest]:
        smallest = child
    if smallest != startpos:
        arr[smallest], arr[startpos] = arr[startpos], arr[smallest]
        min_heapify(arr, relpos, smallest)

def heapsort(arr, relpos, maxheap=True):
    if relpos >= len(arr) - 1:
        return
    sortlen = len(arr) - relpos
    startindex = relpos + int(sortlen / 2)
    while startindex >= relpos:
        if maxheap == True:
            max_heapify(arr, relpos, startindex)
        else:
            min_heapify(arr, relpos, startindex)
        startindex = startindex -1
    relpos = relpos + 1
    heapsort(arr, relpos, maxheap)

#Example run
def main():
    array=[3,2,4,100, -1, 34,56,19,188888,55666,2782]
    sorted = []
    heapsort(array, 0, False)
    print(array)
if __name__ == '__main__':
    main()
