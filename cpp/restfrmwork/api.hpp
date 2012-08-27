#ifndef __API_FOR_REST_OR_WHATEVER__
#define __API_FOR_REST_OR_WHATEVER__

#include <map>
#include <string>
#include <set>
#include <executor.h>

using std::map;
using std::string;
using std::set;

namespace  ourapi
{

class api
{
public:
    api();
    bool executeAPI(const string& url, const map<string, string>& argvals, string& response);
private:
    Executor _executor;
    bool _validate(const void*  data);
    bool _executeAPI(const string& url, const map<string, string>& argvals, string& response);
    void _getInvalidResponse(string& response);
    map<string, set<string> > _apiparams;

};

} // namespace ourapi ends

#endif
