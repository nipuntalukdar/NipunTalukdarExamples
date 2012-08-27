#ifndef __EXECUTOR_FOR_API__
#define __EXECUTOR_FOR_API__

#include <string>
#include <map>

using std::string;
using std::map;

namespace ourapi
{

class Executor
{   
public:
    Executor();
    bool diskinfo(const map<string, string>& args, string& response);
    bool procinfo(const map<string, string>& args, string& response);
    bool sysinfo(const map<string, string>& args, string& response);
private:
    void _eraseWhiteSpace(string& input);

};



}  // namespace ourapi

#endif
