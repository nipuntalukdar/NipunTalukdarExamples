from random import randint

def merge_sort(array,  start, end):
    if start >= end or (end - start) < 1:
        return
    if end - start == 1:
        if array[end] < array[start]:
            array[start], array[end] = array[end], array[start]
        return
    middle = start + ( end - start) / 2

    merge_sort(array, start, middle)
    merge_sort(array, middle + 1, end)

    # insert sort the entire array

    i = middle + 1
    while i <= end:
        if array[i] < array[ i - 1]:
            j = i - 1
            while j >= start:
                if array[j] > array[i]:
                    j -= 1
                else:
                    break
            j += 1
            tmp = array[i]
            k = i
            while k > j:
                array[k] = array[k - 1]
                k -= 1
            array[j] = tmp
        i += 1

                

if __name__ == '__main__':
    x = []
    for i in range(20):
        x.append(randint(1,100))
    merge_sort(x, 0, len(x) - 1)
    print x
