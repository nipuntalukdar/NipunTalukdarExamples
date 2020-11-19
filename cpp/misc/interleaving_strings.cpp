#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>

using std::string;
using std::vector;
using std::cout;
using std::endl;
using std::tuple;
using std::make_tuple;
using std::get;


bool is_interleaving(const string& first, const string& second, 
    const string& interleaved)
{
    if (first.size() + second.size() != interleaved.size()) {
        return false;
    }
    if (first.size() == 0) {
        return second == interleaved;

    }
    if (second.size() == 0) {
        return first == interleaved;
    }
    
    if (second[0] != interleaved[0] && first[0] != interleaved[0]) {
        return false;
    }

    int i = first.size() + 1;
    int j = second.size() + 1;

    int k = 0;
    vector<vector<bool> > matrix;
    while (k++ < j) {
        matrix.push_back(vector<bool>(false,i));
    }

    // 0 char from first, 0 char from second is equal 0
    // char from interleaved
    matrix[0][0] = true;

    // Now check how much of interleaved string can be formed 
    // by using 0 char from second and all others from first

    k = 1;
    while (k < i) {
        if (matrix[0][k - 1] &&  (first[k - 1] == interleaved[k - 1]))
            matrix[0][k] = true;
        else
            break;
        k++;
    }
    
    // Now check how much of interleaved string can be formed 
    // by using 0 char from first and all others from second

    k = 1; 
    while (k < j) {
        if (matrix[0][0] &&  (second[k - 1] == interleaved[k - 1]))
            matrix[k][0] = true;
        else
            break;
        k++;
    }

    // Now we successively find out if interleaved[:n+m] can be formed
    // by interleaving first n chars from first and m chars from second
    // m varies from 1 to len(first)
    // n varies from 1 to len(second)
    // When we are on xth row of the matrix, we are actually trying to
    // check if (x - 1) chars from second string have been already seen,
    // and for that to happen, x - 2 chars have to be already present
    // in some prefix of interleaved. 

    k = 1;
    int l = 0;
    bool ksecond_matched = false;
    while (k < j) {
        //checking for a prefix of interleaved which can be formed
        //with k chars from second 
        l = 1;
        ksecond_matched = matrix[k][0];
        while (l < i) {
            if (!ksecond_matched) {
                if (matrix[k-1][l] && interleaved[k + l - 1] == second[k-1]) {
                    matrix[k][l] = true;
                    ksecond_matched = true;
                }
            } else {  
                // we have already matched k chars from second, check if a prefix
                // of length k + x can be obtained which is interleaved with
                // first k and x chars from second and first respectively
                if (matrix[k][l - 1] && interleaved[k + l - 1] == first[l-1])
                    matrix[k][l] = true;
            }
            l++;
        }
        k++;
    }
    return matrix[j - 1][i - 1];

}


// test run

int main() {
    cout << "Running some tests for the implementation" << endl;
    vector<tuple<string, string, string, bool> > inputs;
    inputs.push_back(make_tuple("a", "b", "ab", true));
    inputs.push_back(make_tuple("ab", "", "ab", true));
    inputs.push_back(make_tuple("abc", "d", "abcd", true));
    inputs.push_back(make_tuple("abc", "d", "acbd", false));
    inputs.push_back(make_tuple("a", "bc", "ab", false));
    inputs.push_back(make_tuple("ab", "bc", "abbc", true));
    inputs.push_back(make_tuple("ab", "bc", "acbb", false));
    inputs.push_back(make_tuple("ac", "bc", "abbc", false));

    for_each(inputs.begin(), inputs.end(), [](tuple<string, string, string, bool>& data) {
            cout << "Cheking for str1 = " << get<0>(data) << "  str2 = " << get<1>(data) 
                << "    interleaved = " << get<2>(data) 
                << "  expected=" << std::boolalpha << get<3>(data); 
            if (is_interleaving(get<0>(data), get<1>(data), get<2>(data)) != get<3>(data)){
                cout << " --> Failed " << endl;
            } else {
                cout << " --> Success " << endl;
            }
    });    
}
