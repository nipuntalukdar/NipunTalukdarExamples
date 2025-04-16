def lcs(l1, l2):
    len1 = len(l1)
    len2 = len(l2)
    if len1 == 0 or len2 == 0:
        return 0, []

    if l1[len1 - 1] == l2[len2 - 1]:
        a, cs = lcs(l1[: len1 - 1], l2[: len2 - 1])
        return a + 1, cs + [l1[len1 - 1]]

    x, seq1 = lcs(l1, l2[: len2 - 1])
    y, seq2 = lcs(l1[: len1 - 1], l2)
    if x > y:
        return x, seq1
    return y, seq2


def superseq(l1, l2):
    if len(l1) == 0:
        return l2
    if len(l2) == 0:
        return l1

    cl, cs = lcs(l1, l2)
    if cl == 0:
        return l1 + l2

    l2_s = list(l2)
    insert_index = []
    ind = 0
    for c in cs:
        ind = l2_s.index(c, ind)
        insert_index.append(ind)
        ind += 1

    j = 0
    i = 0
    for c in cs:
        ind = insert_index.pop(0)
        i = 0
        while True:
            j += 1
            if l1[j - 1] != c:
                l2_s.insert(ind + i, l1[j - 1])
                i += 1
            else:
                break
        insert_index = [a + i for a in insert_index]
    while j < len(l1):
        l2_s.append(l1[j])
        j += 1
    return "".join(l2_s)


print(superseq("abac", "ac"))
print(superseq("abac", "cab"))
print(superseq("same", "same"))
print(superseq("abc", "def"))
