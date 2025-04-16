"""
Explanation is available at:
https://docs.google.com/document/d/e/2PACX-1vTBJNbHbfnXWiMW5PsRiweleV-A8uZGPMMtLE2klBjpkXzN9h0qpX6Y2k_naoa6BVuJ_DsvKPfRAqT1/pub

"""


def min_edit_distance(source, target):
    if len(source) == 0:
        return len(target)
    if len(target) == 0:
        return len(source)

    n = len(source)
    m = len(target)

    distance = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(n + 1):
        distance[0][i] = i

    for i in range(m + 1):
        distance[m][0] = i

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if source[i - 1] == target[j - 1]:
                distance[j][i] = distance[j - 1][i - 1]
                continue
            x = distance[j - 1][i] + 1  # insert
            y = distance[j][i - 1] + 1  # delete
            z = distance[j - 1][i - 1] + 1  # substituition
            distance[j][i] = min(x, y, z)

    return distance[m][n]


print(min_edit_distance("axd", "abc"))
print(min_edit_distance("horse", "ros"))
print(min_edit_distance("intention", "execution"))
