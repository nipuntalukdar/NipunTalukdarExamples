#-------------------------------------------------------------------------------
# Name:        quicksort
# Purpose:
#
# Author:      NTalukdar
#
# Created:     27-01-2014
# Copyright:   (c) NTalukdar 2014
#-------------------------------------------------------------------------------
def quicksort(array, start, end):
    if len(array) <= 1:
        return
    pivotindex = start + int((end - start + 1) / 2)
    pivotel = array[pivotindex]
    temp = array[end]
    array[end] = pivotel
    array[pivotindex] = temp
    i = start
    pivotindex = start
    while i < end:
        if array[i] <= pivotel:
            temp = array[i]
            array[i] = array[pivotindex]
            array[pivotindex] = temp
            pivotindex = pivotindex + 1
        i = i + 1
    temp = array[end]
    array[end] = array[pivotindex]
    array[pivotindex] = temp
    if pivotindex - start > 1:
        quicksort(array, start, pivotindex - 1)
    if end -pivotindex > 1:
        quicksort(array , pivotindex + 1, end)

#example run of the quicksort
def main():
    array = [100, 34, 3,1,3,4,0,67,78]
    quicksort(array, 0, len(array) - 1)
    print(array)

if __name__ == '__main__':
    main()
