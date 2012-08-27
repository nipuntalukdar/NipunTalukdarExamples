#include <api.h>

using namespace ourapi;

struct validate_data
{
    string api;
    map<string, string>* params; 
};

api::api()
{
    set<string> params;
    string sysinfoparams[] = {"cpus", "memory", "os"}; 
    string processinfoparams[] = {"numprocessess", "totalprocess", "topmemprocesss" };
    string diskinfoparamas[] = {"totalparts", "spaceinfo" };

    _apiparams["/sysinfo"] =  set<string>(sysinfoparams, sysinfoparams + 3);
    _apiparams["/procinfo"] = set<string>(processinfoparams, processinfoparams  + 3);
    _apiparams["/diskinfo"] = set<string>(diskinfoparamas, diskinfoparamas + 2);
}

bool api::executeAPI(const string& url, const map<string, string>& argvals, string& response)
{
    validate_data vdata ;
    vdata.api = url;
    vdata.params =(map<string, string> *) &argvals;
    if ( !_validate(&vdata)) {
        _getInvalidResponse(response);
        return false;
    }

    return _executeAPI(url, argvals, response);
}

bool api::_executeAPI(const string& url, const map<string, string>& argvals, string& response)
{
    bool ret = false;
    if (url == "/sysinfo") 
        ret = _executor.sysinfo(argvals, response);
    if (url == "/diskinfo")
        ret = _executor.diskinfo(argvals, response);
    if (url == "/procinfo")
        ret = _executor.procinfo(argvals, response);

    return ret;
}

bool api::_validate(const void *data)
{
    const validate_data *vdata = static_cast<const validate_data *>(data );
    map<string, set<string> > ::iterator it =  _apiparams.find(vdata->api);

    it = _apiparams.find(vdata->api);

    if ( it == _apiparams.end()){
        return false;
    }
    map<string, string>::iterator it2 = vdata->params->begin();
    while (it2 != vdata->params->end()) {
        if (it->second.find(it2->first) == it->second.end()) 
            return false;
        ++it2;
    }

    return true;
}

void api::_getInvalidResponse(string& response)
{
    response = "Some error in your data ";
}

#if 0
int main()
{
    api a;
    map<string, string>b ;
    b["totalparts"] = "1";
    string url = "diskinfo";
    string response;
    a.executeAPI(url,b, response);

}

#endif 
