from random import randint


def onethreetwo(lst):
    if len(lst) < 3:
        return False

    n = len(lst)
    mins = [float("inf")] * n
    mins[0] = lst[0]
    for i in range(1, n):
        mins[i] = min(mins[i - 1], lst[i])
    stack = []
    for j in range(n - 1, 0, -1):
        while stack and stack[-1] < lst[j]:
            k = stack.pop()
            if k > mins[j - 1]:
                return True
        stack.append(lst[j])
    return False


def brute_check(lst):
    if len(lst) < 3:
        return False
    for i in range(1, len(lst) - 1):
        small = min(lst[:i])
        if small >= lst[i]:
            continue
        if any(x < lst[i] and x > small for x in lst[i + 1 :]):
            return True
    return False


x = [1, 2, 3, 4, 2]
assert onethreetwo(x) == brute_check(x)
x = [randint(1, 200) for _ in range(20)]
assert onethreetwo(x) == brute_check(x)
assert not onethreetwo([x for x in range(200)])
assert onethreetwo([1, 3, 2])
