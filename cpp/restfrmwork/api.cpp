#include <boost/foreach.hpp>
#include <api.hpp>
#include <strutil.hpp>

using namespace ourapi;

struct validate_data
{
    string api;
    set <string>* params; 
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
    // Ignore all the args except the "fields" param 
    validate_data vdata ;
    vdata.api = url;
    vector<string> params;
    set<string> uniqueparams;
    map<string,string>::const_iterator it1 = argvals.find("fields");

    if (it1 != argvals.end()) {
        StrUtil::splitString(it1->second, ",", params);   
    }
    BOOST_FOREACH( string pr, params ) {
        uniqueparams.insert(pr);
    }
    vdata.params = &uniqueparams;

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
    set<string>::iterator it2 = vdata->params->begin();
    while (it2 != vdata->params->end()) {
        if (it->second.find(*it2) == it->second.end()) 
            return false;
        ++it2;
    }

    return true;
}

void api::_getInvalidResponse(string& response)
{
    response = "Some error in your data ";
}

