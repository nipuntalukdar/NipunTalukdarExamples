'''
Take an element, "include" the element and check if there
is combination of some other elements with this that
adds up to the sum. If it is there, return true
Then "exclude" the element and then check if there are
other elements without the excluded elements add up to 
the sum. If it is there, then return true

Do that recursively
'''

def find_subset_sum(array, n, sumval):
    if n == 0:
        return sumval == 0

    # Include the element
    included_sum = sumval - array[n - 1]
    if included_sum == 0:
        return True
    if included_sum > 0:
        sum_matched = find_subset_sum(array, n - 1, included_sum)
        if sum_matched:
            return True
    # Now try excluding the current element
    return find_subset_sum(array, n - 1, sumval)

# The below implementation also returns the first list of
# elements making up the sum
def find_subset_sum_and_set(array, n, sumval, array_taken):
    if n == 0:
        return sumval == 0, array_taken
    # Include the element
    included_sum = sumval - array[n - 1]
    if included_sum == 0:
        return True, array_taken.append(array[n-1])
    if included_sum > 0:
        array_taken.append(array[n-1])
        sum_matched = find_subset_sum_and_set(array, n - 1, included_sum, array_taken)
        if sum_matched:
            return True, array_taken
        # Remove the taken element as it cannot be in array making up the sum
        array_taken.pop()
    # Now try excluding the current element
    return find_subset_sum_and_set(array, n - 1, sumval, array_taken)

# Test run
arraynum = [1,4,8,7, 9, 9, 19]
print find_subset_sum(arraynum, len(arraynum), 29)
print find_subset_sum(arraynum, len(arraynum), 33)

print find_subset_sum_and_set(arraynum, len(arraynum), 29, [])
print find_subset_sum_and_set(arraynum, len(arraynum), 33, [])
