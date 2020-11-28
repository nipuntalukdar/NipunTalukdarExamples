'''
Longest Substring Without Repeating Characters
'''

def longest_without_repeat(input):
    start_index = 0
    end_index = 0
    chars = {}
    i = len(input)
    max_start = 0
    max_len = 0

    j = 0
    while j < i:
        if input[j] in chars:
            indx = chars[input[j]]
            while start_index <= indx:
                del chars[input[start_index]]
                start_index += 1
            chars[input[j]] = j
        else:
            chars[input[j]] = j

        if j - start_index + 1 > max_len:
            max_len = j - start_index + 1
            max_start = start_index
        j += 1
    return input[max_start: max_start + max_len ]

print(longest_without_repeat('abcabcddcbaeffabcd'))
