import unittest
'''
Maximum capacity of the bag is W.
Items are with value v0, v1, v2, ...., vn
with weights w0, w1, w2, w3, ....., wn
what is the maximum price of items you may take in 
bag?

Assume V[i, j] is the maxium possible values with maximum total weight j,
Then,
V[i, j] is can be found as:
V[i,j] = V[i-1, j] if w[i] > j
OR
V[i,j] = max(V[i-1,j], v[i] + V[i-1, j - w[i]])

'''

def find_maximum_vals_with_given_weight(vals, weights, maxweight):
    if len(vals) != len(weights):
        raise("Error")
    maxvals = []
    i = 0
    while i < len(vals):
        maxvals.append([0] * (maxweight + 1))
        i += 1
    i = 0
    while i < len(vals):
        j = 0
        while j < (maxweight + 1):
            if weights[i] > j:
                if i > 0:
                    maxvals[i][j] = maxvals[i - 1][j]
            else:
                if i > 0:
                    maxval1 = maxvals[i-1][j]
                    maxval2 = maxvals[i-1][j - weights[i]] + vals[i]
                    maxvals[i][j] = max(maxval1, maxval2)
                else:
                    maxvals[i][j] = vals[i]
            j += 1
        i += 1
    i = 0
    while i < len(vals):
        i += 1
    return maxvals[len(vals) - 1][maxweight]

class TestKnapSack(unittest.TestCase):
    def test_all(self):
        weights = [4, 6, 12]
        values = [20, 40, 100]
        maxweight = 2
        self.assertEqual(0, find_maximum_vals_with_given_weight(values, weights,
            maxweight))
        maxweight = 6
        self.assertEqual(40,find_maximum_vals_with_given_weight(values, weights,
            maxweight))
        maxweight = 9
        self.assertEqual(40,find_maximum_vals_with_given_weight(values, weights,
            maxweight))
        maxweight = 10
        self.assertEqual(60, find_maximum_vals_with_given_weight(values,
            weights, maxweight))
        maxweight = 11
        self.assertEqual(60, find_maximum_vals_with_given_weight(values,
            weights, maxweight))
        maxweight = 13
        self.assertEqual(100, find_maximum_vals_with_given_weight(values,
            weights, maxweight))
        maxweight = 23
        self.assertEqual(160, find_maximum_vals_with_given_weight(values,
            weights, maxweight))

if __name__ == '__main__':
    unittest.main()
