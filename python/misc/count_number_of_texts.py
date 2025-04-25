'''
At each position i of the input string X
the substring is Y = X[:i + 1]
Now if any valid small word is suffix of Y,
then the prefix of Y removing this suffix can be formed
in n ways from the input keys, then X[:i+1] can be formed
in at least n ways from the small words. For each small word 
that is a suffix of X[:i+1] we do the checks.

'''
origin_map = {
    "2" : "abc",
    "3" : "def",
    "4" : "ghi",
    "5" : "jkl",
    "6" : "mno",
    "7" : "pqrs",
    "8" : "tuv",
    "9" : "wxyz"
}

def expand_map(orig):
    ret = {}
    for k, v in origin_map.items():
        for i in range(len(v)):
            ret[k * (i + 1)] = v[i]
    return ret

def count_string(bigword, keys):
    n = len(bigword)
    dp = [0] * n
    for i in range(n):
        for key in keys:
            k = len(key)
            if k  <= i + 1:
                tmp = bigword[i + 1 - k : i+1]
                if tmp == key:
                    prefix = bigword[:i+1 -k ]
                    if not prefix:
                        dp[i] += 1
                    else:
                        dp[i] += dp[i-k]


    print(dp)
    return dp[n-1]


exp_map = expand_map(origin_map)

number_keys = exp_map.keys()
print(count_string("222222222222222222222222222222222222", number_keys))


