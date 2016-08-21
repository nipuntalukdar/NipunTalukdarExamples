# Below function demonstrates how we can print the permutations of the letters
# in a word

def print_permute(word):
    a = sorted(word)
    l = len(word)
    exchanged = True
    while exchanged:
        print ''.join(a)
        i = l - 1
        smallest = i
        exchanged = False
        while i != 0:
            if a[i] <= a[i - 1]:
                i -= 1
            else:
                exchanged = True
                j = i + 1
                while j < l:
                    if a[i - 1] < a[j]:
                        j += 1 
                    else:
                        break
                j -= 1
                a[i-1], a[j] = a[j], a[i-1]
                a[i:] = sorted(a[i:])
                break

#Example Run
print ('Printing permutations of xyz')
print_permute('xyz')
print('.............................')
print('.............................')
print ('Printing permutations of abcdd')
print_permute('abcdd')
