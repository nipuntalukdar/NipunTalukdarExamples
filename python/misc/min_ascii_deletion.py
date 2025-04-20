def min_ascii_delete(l1, l2):
    min_ascii = 0
    if len(l1) == 0:
        for c in l2:
            min_ascii += ord
        return min_ascii
    if len(l2) == 0:
        for c in l1:
            min_ascii += ord
        return min_ascii

    n = len(l1)
    m = len(l2)
    cost = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, n + 1):
        cost[0][i] = ord(l1[i - 1]) + cost[0][i - 1]
    for i in range(1, m + 1):
        cost[i][0] = ord(l2[i - 1]) + cost[i - 1][0]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if l1[i - 1] == l2[j - 1]:
                cost[j][i] = cost[j - 1][i - 1]
                continue
            cost1 = cost[j][i - 1] + ord(l1[i - 1])
            cost2 = cost[j - 1][i] + ord(l2[j - 1])
            cost[j][i] = min(cost1, cost2)

    return cost[m][n]


print(min_ascii_delete("delete", "leet"))
