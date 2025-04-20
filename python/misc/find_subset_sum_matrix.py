"""
Let us say we want to check if set of n elements N has a combination that
adds up to sum S.
Have a 2-dimensional matrix of (1+n) * (1+S) size and initialize all
elements to False.
Sort N.
Now check if there is a combination that adds upto 0,
then check if there is a combination that adds upto 1,
...
....
then check if there is a combination that adds upto S.

When we check the number x, to check if it can be added to a set which adds
upto sum y, we check if there is a previous combination which adds up to (y -x).
if that is true, then x can be combined with that previous combination to have
the subset that adds up to y.

We store the results in the array to finally arrive at the conclusion, if there
is a combination that adds upto S.
THIS IS DYNAMIC PROGRAMMING....

"""


def find_subset_sum(inputarray, targetsum):
    if len(inputarray) <= 1:
        return sum(inputarray) == targetsum
    matrix = []
    cols = targetsum + 1
    rows = len(inputarray)
    i = 0
    while i < rows:
        matrix.append([False] * cols)
        i += 1
    sortedarray = sorted(inputarray)
    i = 0
    found_on_row = -1
    while i < rows:
        j = 0
        while j < cols:
            if sortedarray[i] == j:
                matrix[i][j] = True
            else:
                # find in all previous rows on column 'j - sortedarray[j]'
                # if there a True value
                prevcol = j - sortedarray[i]
                if prevcol >= 0:
                    prev_row = i - 1
                    while prev_row >= 0:
                        if matrix[prev_row][prevcol]:
                            matrix[i][j] = True
                            break
                        prev_row -= 1
            j += 1
        if matrix[i][cols - 1]:
            # Already found the subset
            found_on_row = i
            break
        i += 1

    if found_on_row != -1:
        # find the elements adding upto the sum
        start_col = targetsum
        ret_elems = [sortedarray[found_on_row]]
        while found_on_row >= 0:
            start_col = start_col - sortedarray[found_on_row]
            found_on_row -= 1
            while found_on_row >= 0:
                if matrix[found_on_row][start_col]:
                    ret_elems.append(sortedarray[found_on_row])
                    break
                found_on_row -= 1
        return True, ret_elems
    else:
        return False, None


def second_version_find_subset_sum(nums, target):
    if len(nums) == 0:
        return target == 0
    if len(nums) == 1:
        return nums[0] == target

    n = len(nums)

    total = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        total[i][0] = True
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            if j < nums[i - 1]:
                total[i][j] = total[i - 1][j]
                continue
            total[i][j] = total[i - 1][j] or total[i - 1][j - nums[i - 1]]
    return total[n][target]


print(find_subset_sum([3, 3, 5, 4, 100], 112))
print(find_subset_sum([3, 3, 5, 4, 100], 4))
print(find_subset_sum([3, 3, 5, 4, 100], 14))
print(find_subset_sum([1, 2, 3, 5, 6, 7, 8], 13))
print(second_version_find_subset_sum([1, 2, 3, 5, 6, 7, 8], 13))
