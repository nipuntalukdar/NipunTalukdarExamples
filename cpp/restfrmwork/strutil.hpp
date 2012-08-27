#ifndef __OUR_STRUTILS__
#define __OUR_STRUTILS__ 

#include <string>
#include <vector>

using std::vector;
using std::string;

namespace ourapi
{

class StrUtil
{
public:
    static void eraseWhiteSpace(string& input);
    static void splitString(const string& input, const char* delims, 
            vector<string>& tokens);
};

}
#endif
