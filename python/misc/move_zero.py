'''
Move the zeros to the end,
If zeros to move to the start,
we should start from the end of the
array for efficiency

'''

def move_zero(arr):
    if len(arr) < 2:
        return

    i = len(arr)
    j = 0
    start_zero = -1
    while j < i:
        if arr[j] != 0:
            if start_zero != -1:
                arr[start_zero] = arr[j]
                arr[j] = 0
                start_zero += 1
        else:
            if start_zero == -1:
                start_zero = j
        j += 1

def move_zero_first(arr):
    if len(arr) < 2:
        return

    i = len(arr)
    j = i - 1
    start_zero = -1
    while j > -1:
        if arr[j] != 0:
            if start_zero != -1:
                arr[start_zero] = arr[j]
                arr[j] = 0
                start_zero -= 1
        else:
            if start_zero == -1:
                start_zero = j
        j -= 1

x = [0,0,1,2, 0, 4, 5, 0, 6, 7, 0]
y = [0,0,1,2, 0, 4, 5, 0, 6, 7, 0]
move_zero(x)
print(x)
move_zero_first(y)
print(y)


