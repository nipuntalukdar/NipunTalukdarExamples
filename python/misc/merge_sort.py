'''
merge_sort alogoritm
'''

import random

def correct_pos(arr, start, pos_to_correct):
    i = start
    while i <= pos_to_correct:
        if arr[i] <= arr[pos_to_correct]:
            i += 1
        else:
            break
    if i >= pos_to_correct:
        return
    tmp = arr[pos_to_correct]
    while pos_to_correct > i:
        arr[pos_to_correct] = arr[pos_to_correct - 1]
        pos_to_correct -= 1
    arr[i] = tmp
    

def merge_sort(arr, start, end):
    if end - start < 1:
        return
    if end - start == 1:
        if arr[end] < arr[start]:
            arr[end], arr[start] = arr[start], arr[end]
        return
    middle = (end - start) / 2 + start
    merge_sort(arr, start, middle)
    merge_sort(arr, middle + 1, end)

    i = start + 1
    while i <= end:
        if arr[i] < arr[i - 1]:
            correct_pos(arr, start, i)
        i += 1


if __name__ == '__main__':
    random.seed(1)
    arr = []
    i = 0
    while i < 10:
        arr.append(random.randint(0, 1000))
        i += 1

    print 'Unsorted: ', arr
    merge_sort(arr, 0, len(arr) - 1)
    print 'Sorted: ', arr
