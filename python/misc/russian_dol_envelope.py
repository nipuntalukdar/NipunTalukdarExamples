def bigr_env(l1, b1, l2, b2):
    return l1 > l2 and b1 > b2


def get_max_env(envs):
    envs.sort()
    mx = [1] * len(envs)
    print(mx)
    for i in range(1, len(envs)):
        for j in range(i):
            if bigr_env(envs[i][0], envs[i][1], envs[j][0], envs[j][1]):
                mx[i] = max(mx[i], mx[j] + 1)

    print(mx)
    return mx[len(mx) - 1]


print(get_max_env([[5,4],[6,4],[6,7],[2,3]]))
