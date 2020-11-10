def get_distinct_subsequence(source, target):
    if source is None:
        return 0
    if len(target) > len(source):
        return 0
    if len(target) == len(source):
        if target != source:
            return 0
        return 1

    matches = []
    i = 0
    while i < len(target):
        matches.append([0] *len(source))
        i += 1

    j = 0

    while j < len(target):
        row = matches[j]
        i = 0
        while i < len(source):
            if target[j] ==  source[i]:
                if j == 0:
                    if i > 0:
                        row[i] = row[i - 1 ] + 1
                    else:
                        row[i] = 1
                else:
                    if i > 0:
                        row[i] = matches[j - 1][i - 1] + row[i-1]
                    else:
                        row[i] = 0
            else:
                if i > 0:
                    row[i] = row[i - 1]
                else:
                    row[i] = 0

            i +=1

        j += 1
    print matches
    return matches[j - 1][i-1]


print get_distinct_subsequence('aababb', 'aab')
