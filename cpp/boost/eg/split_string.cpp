#include <vector>
#include <iostream>
#include <boost/algorithm/string/regex.hpp>
#include <boost/regex.hpp>

using std::endl;
using std::cout;
using std::string;
using std::vector;
using boost::algorithm::split_regex;

int main()
{
    vector<string> out;
    string sep = "(\r\n)+";
    string input = "aabcdabc\r\n\r\ndhhh\r\ndabcpqrshhsshabc";
    split_regex(out, input, boost::regex("(\r\n)+"));
    for (auto &x : out) {
        std::cout << "Split: " << x << std::endl;
    }
    return 0;
}
