def min_cut_palindrome(lst):
    if len(lst) <= 1:
        return len(lst)
    if len(lst) < 3:
        if lst[0] == lst[1]:
            return 0
        return 1
    n = len(lst)
    isp = [[False] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1):
            start = j
            end = i
            isp[j][i] = True
            while start <= end:
                if lst[start] != lst[end]:
                    isp[i][j] = False
                    break
    if isp[0][n-1]:
        return 0

    min_cuts = [0] * n
    for i in range(1, n):
        min_cuts[i] = i
        for j in range(i):
            if isp[j[i]:
                min_cuts[i] = min(min_cuts[i], 1 + min_cuts[j-1])

    return min_cuts[n -1]

            
                

