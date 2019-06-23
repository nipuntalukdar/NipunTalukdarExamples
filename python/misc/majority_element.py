'''
In an array, if a particular element is happenning more than 
N/2 times where N is the size of the array, then that is the 
majority element.

Start with the first element and mark that is majority and
set it's count at 1. If subsequent elements equal to that element,
increment count and if not equal decrement the count. If the 
count becomes 0, then change the majority element to the current
element and set count to 0.
At the end go throgh the array again to 
check if the element is really the majority element.

'''

def find_majority_elem(array):
    if len(array) == 0:
        return False, 0
    if len(array) == 1:
        return True, array[0]
    found = True
    majority_elem = array[0]
    count = 1
    i = 1
    while i < len(array):
        if array[i] == majority_elem:
            count += 1
        else:
            count -= 1
        if count == 0:
            majority_elem = array[i]
            count = 1
        i += 1
    count = 0
    for elem in array:
        if elem == majority_elem:
            count += 1
    if count > (len(array) / 2):
        return True, majority_elem
    else:
        return False, -1

# Test run
print find_majority_elem([1,1,2,0,2,3,0,1,2,1,3,1])
print find_majority_elem([1,2,3,4,3,5,3,3,1,3,3,3,5])
