'''
Replace every element with the smallest element on its left side
'''

def replace_in_array(array):
    if len(array) < 1: 
        return
    smallest_so_far = array[0]
    i = 1
    while i < len(array):
        if array[i] < smallest_so_far:
            array[i], smallest_so_far = smallest_so_far, array[i]
        else:
            array[i] = smallest_so_far
        i += 1

x = [10, 3, 2, 5, 4, 10, 100]
print x
replace_in_array(x)
print x
   
