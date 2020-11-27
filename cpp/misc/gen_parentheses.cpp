#include <iostream>
#include <vector>
#include <algorithm>

/*
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

*/

using namespace std;

void gen_p(size_t depth, size_t rt, size_t lt, vector<char>& lst,
    size_t maxcount, size_t paircount)
{
    depth += 1;
    if (rt < lt) {
        lst.push_back(')');
        if (depth != maxcount)
            gen_p(depth, rt + 1, lt, lst, maxcount, paircount);
        else {
            for_each(lst.begin(), lst.end(), [](char c) {cout << c;});
            cout << endl;
        }
        lst.pop_back();
    }
    if (lt != paircount) {
        lst.push_back('(');
        gen_p(depth, rt, lt + 1, lst, maxcount, paircount);
        lst.pop_back();
    }

}

void gen_parantheses(size_t paircount) 
{
    vector<char> lst;
    gen_p(0, 0, 0, lst, paircount * 2, paircount);    
}

int main()
{
    gen_parantheses(6);
    return 0;
}
