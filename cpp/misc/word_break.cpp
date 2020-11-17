#include <string>
#include <iostream>
#include <unordered_set>
#include <algorithm>
#include <vector>

using std::cout;
using std::string;
using std::vector;
using std::unordered_set;
using std::cout;
using std::endl;

class word_break
{
private:
    unordered_set<string> words;
    word_break& operator=(const word_break&) = delete;
    word_break(const word_break&) = delete;
    word_break() = delete;

public:
    word_break(const unordered_set<string>& words);
    bool can_break(const string& input);
};

word_break::word_break(const unordered_set<string>& words)
{
    unordered_set<string>::iterator it = words.begin();
    while (it != words.end()) {
        this->words.insert(*it);
        it++;
    }
}



bool word_break::can_break(const string& input)
{
    if (any_of(words.begin(), words.end(), [&input ](const string& inp) {return inp == input; })){
        return true;
    }
    vector<vector<bool>> vals;
    int i = input.size();
    int j = 0;
    while ( j++ < i ) {
       vals.push_back(vector<bool>(i, false));
    }

    // Now fill check for words with just one chars
    j = 0;
    while (j < i) {
        string a = input.substr(j, 1);
        if (any_of(words.begin(), words.end(), [&a ](const string& inp) {return a == inp; })){
            vals[j][j] = true;
        }
        j++;
    }

    // Now check from length 2 onwards to length of the input string
    int k = 2;
    while (k <= i) {
        j = 0; 
        while ((j + k) <= i) {
            if (k == i) {
                // complete input string
                while (j <= i - 2) {
                    if  (vals[0][j] && vals[j+1][i-1])
                        return true;
                    j++;
                }
            } else {
                string tmp = input.substr(j, k);
                if (any_of(words.begin(), words.end(), [&tmp ](const string& inp) {return tmp == inp; })){
                    vals[j][j + k -1] = true;
                } else {
                   int m = j;
                   while (m <= j + k - 2) {
                       if (vals[j][m] && vals[m+1][j+k-1]){
                           vals[j][j+k-1] = true;
                           break;
                       }
                       m++;
                   }
                }
            }
            j++;
        }
        k++;
    }

    return false;
}



int main()
{
    unordered_set<string> words({"xx", "x", "am", "i", "ok", "you", "are", "fine"});
    word_break wb(words);
    vector<string> input = {"a", "fineare", "x", "ami", "xxx", 
                "iamfineokok", "no", "arefin", "", "aaaa"};
    for_each(input.begin(), input.end(), [&wb](string& inp) {
            if (wb.can_break(inp))
                    cout << "Can break " << inp << endl;
             else
                     cout << "Cannot break " << inp << endl;
            }); 
    return 0;
}
