from copy import copy

def find_max_hist_area(arr):
    cur_max = arr[0]
    arreas = {arr[0] :  arr[0]}
    currents = [arr[0]]
    i = 1
    current_height = arr[0]

    while i < len(arr):
        removes = []
        rem_count = 0
        for k in arreas:
            if k > arr[i]:
                removes.append(k)
        for k in removes:
            rem_count += int(arreas[k] / k)
            del arreas[k]

        for k in arreas:
            arreas[k] += k
            if arreas[k] > cur_max:
                cur_max = arreas[k]
        if arr[i] not in arreas:
            arreas[arr[i]] = arr[i] + rem_count * arr[i]
            if arreas[arr[i]] > cur_max:
                cur_max = arreas[arr[i]]
        i += 1

    return cur_max

'''
Get the maximum histogram area with all 1s,
starting with first row
if a column in a row is 1, then histogram 
will add the prvious 1s from that column,
basically histograms height increase on that
column. If the element is 0, then the height
on that column of the histogram becomes 0.
'''
def max_rec_all_ones(rects):
    cur_max = 0
    cur_row = None
    for r in rects:
        if not cur_row:
            cur_row = copy(r)
        else:
            i = 0
            while i < len(r):
                if r[i] == 1:
                    cur_row[i] += 1
                else:
                    cur_row[i] = 0
                i += 1
        cur_max_tmp = find_max_hist_area(cur_row)
        if cur_max_tmp > cur_max:
            cur_max = cur_max_tmp
    return cur_max

 
print(max_rec_all_ones([[1, 1], [0,0], [1,1]]))
