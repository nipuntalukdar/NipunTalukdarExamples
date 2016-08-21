# Below function demonstrates how we can print the permutations of the letters
# in a word

###############################################################################
# HOW it works?
# it starts with the "smallest" possible word and successively prints the next
# bigger word. For example, the smallest possible word from the chars in 
# word 'axprq' is 'apqrx' and then the next bigger word is 'apqxr' and so on.
# It stops after printing the "biggest" word which is 'xrqpa'.
#
# The advantage of this algorithm is that we don't print any duplicate words.
#
#
# Given a word(current permutation), how do we find the next permutation?
# ------------------------------ 
# Start from last char and successively compare a char to the character in its
# left. If the left character is smaller than the current character (say the 
# position of the left character is exchange position), exchange the left 
# charecter with a charecter to its right which is bigger than it and
# nearest to it. When the exchange happens, sort the character array to the 
# right of the exchange position.
# Repeat the above process until the iteration when no exchange of characters
# happens (i.e. it reaches the "biggest" word)

def print_permute(word):
    a = sorted(word)
    l = len(word)
    exchanged = True
    while exchanged:
        print ''.join(a)
        i = l - 1
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
print('.............................')
print('.............................')
print ('Printing permutations of axprq')
print_permute('axprq')
