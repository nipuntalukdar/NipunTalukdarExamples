#ifndef __EXECUTOR_FOR_API__
#define __EXECUTOR_FOR_API__

#include <string>
#include <set>

using std::string;
using std::set;

namespace ourapi
{

class Executor
{   
public:
    enum outputType {
        TYPE_JSON, TYPE_XML   
    };
    Executor();
    bool diskinfo(const set<string>& args, outputType type,  string& response);
    bool procinfo(const set<string>& args, outputType type, string& response);
    bool sysinfo(const set<string>& args, outputType type, string& response);
private:
    void _generateOutput(void *data, outputType type, string& output);

};



}  // namespace ourapi

#endif
