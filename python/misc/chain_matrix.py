'''
Optimizing chain matrix multiplication algorihm
using dynamic programming.
Suppose we are multiplying matrices a0, a1, a2,...,an then we check
where we can parenthesize at top level. Let us say we put the bracket
at position k for that which minimizes the cost for the last multiplication.
So, a0 to ak, and ak+1 to an can be parenthesied. Then we check, where
we can put bracket for optimizing the multiplication for a0..ak and 
ak+1...an and so on. 
The process follows as:
    when there is just one matrix, the multiplication cost is 0.
    Then we get the cost for multiplying a0,a1, a1,a2, a2,a3 .... an-1,an
    then we get the cost for getting minimum cost for multiplying a0,a1,a2, a1,a2,a3,
    a2,a3,a4,...... an-2,an-1,an and for this step we can use the already computed for
    multiplying two adjacent matrix.
    Thus we reuse computation from previous stages to get the final cost.

'''

from random import randint, seed
from time import time

def gen_matrix_dimensions(max_dimension, min_dimension, num_matrix):
    '''
    Returns an array of matrix dimensions which the algorithm will 
    analyze regarding where to put parenthesis
    '''
    seed(10) 
    i = 0
    fd = randint(min_dimension, max_dimension)
    sd = randint(min_dimension, max_dimension)
    ret = []
    while i < num_matrix:
        ret.append((fd, sd))
        fd, sd = sd, randint(min_dimension, max_dimension)
        i += 1

    return ret


def get_min_cost(start, end, opt_vals, mdims):
    L = end - start + 1
    if L == 2:
        min_cost = mdims[start][0] * mdims[start][1] * mdims[end][1]
        return start, min_cost
    min_cost = -1
    split_mark = -1
    k = start 
    while k <= end - 1:
        min_c = opt_vals[start][k] + opt_vals[k+1][end] + mdims[start][0] * mdims[k][1] * mdims[end][1]
        if min_cost == -1:
            min_cost = min_c
            split_mark = k
        elif min_c < min_cost:
            min_cost = min_c
            split_mark = k
        k += 1
    return split_mark, min_cost

def print_opt_vals(opt_vals):
    for val in opt_vals:
        print val


def min_mult_cost(mdims):
    '''
    :param mdims: array of matrix dimensions
    '''
    opt_vals = []
    split_marks = []
    l = len(mdims)
    if l < 2:
        return 0

    i = 0
    while i < l:
        split_marks.append([-1] * l)
        i += 1
    i = 0
    while i < l:
        opt_vals.append([-1] * l)
        i += 1
    i = 0
    while i < l:
        opt_vals[i][i] = 0
        i += 1
    L = 2
    while L <= l:
        start = 0
        end = l - L
        while start <= end:
            split_mark, min_cost = get_min_cost(start, start + L - 1, opt_vals, mdims)
            split_marks[start][start + L - 1] = split_mark
            opt_vals[start][start + L - 1] = min_cost
            start += 1
        L += 1
    return opt_vals[0][l - 1]

x = gen_matrix_dimensions(10, 4, 4)
y = min_mult_cost(x)
print 'Minimum cost', y
