"""
For finding minimum deletion to make two strings same, we find their
longest common sequence. Then number of deletion required is:
((length of string1 - length of commn sequence) +
(length of string2 - length of commn sequence))

"""


def biggest_common(l1, l2):
    len1 = len(l1)
    len2 = len(l2)
    if len1 == 0 or len2 == 0:
        return 0

    if l1[len1 - 1] == l2[len2 - 1]:
        return 1 + biggest_common(l1[: len1 - 1], l2[: len2 - 1])

    x = biggest_common(l1, l2[: len2 - 1])
    y = biggest_common(l1[: len1 - 1], l2)
    return max(x, y)


def min_del(l1, l2):
    common = biggest_common(l1, l2)
    return len(l1) + len(l2) - 2 * common


print(min_del("abc", "abc"))
print(min_del("abc", "abcd"))
