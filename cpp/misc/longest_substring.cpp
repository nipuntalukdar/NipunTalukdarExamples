#include <iostream>
#include <string>
#include <unordered_map>
/*
Longest Substring Without Repeating Characters
*/

using namespace std;

string longest_substr_without_repeat(const string& input)
{
    if (input.size() < 2)
        return input;
    size_t start_index = 0, max_len = 0, max_start = 0;
    size_t j = 0;
    unordered_map<char, size_t> chars;
    while (j < input.size()) {
        if (chars.find(input[j]) != chars.end()){
            size_t index = chars[input[j]];
            while (start_index <= index){
                chars.erase(input[start_index]);
                start_index++;
            }
        }
        chars[input[j]] = j;
        if (j - start_index + 1 > max_len) {
            max_len = j - start_index + 1;
            max_start = start_index;
        }
        j++;
    }
    return input.substr(max_start, max_len);

}


int main()
{
    string input("abcabcddddbcaxyabcdefghiiiklmnopqrstuvabcdeddae");
    cout << longest_substr_without_repeat(input) << endl;
}
