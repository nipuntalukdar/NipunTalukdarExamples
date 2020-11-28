from copy import copy

def print_permute(input, lst, printed):
    if len(input) == 1:
        lst.append(input[0])
        word = ''.join(lst)
        if word not in printed:
            printed.add(word)
            print(word)
        lst.pop()
    else:
        i = 0
        while i < len(input):
            newinput = copy(input)
            x = newinput.pop(i)
            lst.append(x)
            print_permute(newinput, lst, printed)
            lst.pop()
            i += 1
string = 'abcda'
print_permute(list(string), [], set())
        
