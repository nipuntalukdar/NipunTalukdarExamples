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
        
print(find_max_hist_area([100,2,1,1, 40,50,40]))
