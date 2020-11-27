'''
genrate valid combination of parentheses
E.g. for 1 pair,
we get the below:
()

for 2 pairs, we get
()()
(())

For 3 pairs, we get:
()()()
()(())
(())()
(()())
((()))

etc.

'''


def gen_p(depth, rt, lt, lst, maxcount, paircount):
    depth += 1
    if rt < lt:
        lst.append(')')
        if depth != maxcount:
            gen_p(depth, rt + 1, lt, lst, maxcount, paircount)
        else:
            print(''.join(lst))
        lst.pop()
    if lt != paircount:
        lst.append('(')
        if depth != maxcount:
            gen_p(depth, rt, lt + 1, lst, maxcount, paircount)
        lst.pop()

   
gen_p(0, 0, 0, [], 10, 5)
