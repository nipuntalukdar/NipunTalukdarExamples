#include <stdio.h>
#include <iostream>
#include <vector>
#include <sstream>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

#include <executor.h>
#include <strutil.h>

using namespace ourapi;
using std::vector;
using boost::property_tree::ptree;
using std::make_pair;


Executor::Executor()
{
}

bool Executor::diskinfo(const map<string, string>& args, string& response)
{
    const char *command = "df | sed 's/ \\+/ /g'  | tail -n +2 ";
    char line[255];
    vector<string> tokens;

    FILE *fp = popen(command, "r");
    while (fgets(line, 255, fp) != 0){
        response += string(line);
    }
    StrUtil::splitString( response, " \t\n", tokens); 
    std::cout << response ;
    vector <string> :: iterator it = tokens.begin();
    while (it != tokens.end()) {
        std::cout << *it << std::endl;
        ++it;
    }
    fclose(fp);    
    return true;
}

bool Executor::procinfo(const map<string, string>& args, string& response)
{
    const char *command = "ps -ef";
    char line[1048];
    vector<string> tokens;

    FILE *fp = popen(command, "r");
    while (fgets(line, 1048, fp) != 0){
        response += string(line);
    }
    fclose(fp);    
    return true;
}

bool Executor::sysinfo(const map<string, string>& args, string& response)
{
    const char *commandcpu = "cat /proc/cpuinfo |  sed 's/\\s\\+: /:/g'";
    const char *commandmemory = "cat /proc/meminfo |  sed 's/:\\s\\+/:/g'";
    const char *commandos = "uname -a";
    FILE *fp;
    char commandout[1048];
    string line;

    ptree sysinfo;


    while (args.find("cpus") != args.end()) {
        fp = popen(commandcpu, "r");
        if (!fp)
            break;
        ptree temp;
        string field;
        string value;
        size_t index;
        ptree::iterator pit = sysinfo.push_back(make_pair("cpus", temp));
        while (fgets(commandout, 1048, fp) != 0){
            line = commandout;
            StrUtil::eraseWhiteSpace(line);
            index = line.find(":");
            if (string::npos == index)
                continue;
            field = line.substr(0, index);
            value = line.substr(index + 1);
            pit->second.push_back(make_pair(field, value));
        }
        fclose(fp);
        break;
    }
    
    while (args.find("memory") != args.end()) {
        fp = popen(commandmemory, "r");
        if (!fp)
            break;
        ptree temp;
        string field;
        string value;
        size_t index;
        ptree::iterator pit = sysinfo.push_back(make_pair("memory", temp));
        while (fgets(commandout, 1048, fp) != 0){
            line = commandout;
            StrUtil::eraseWhiteSpace(line);
            index = line.find(":");
            if (string::npos == index)
                continue;
            field = line.substr(0, index );
            value = line.substr(index + 1);
            pit->second.push_back(make_pair(field, value));
        }
        fclose(fp);
        break;
    }
    while (args.find("os") != args.end()) {
        fp = popen(commandos, "r");
        if (!fp)
            break;
        if (fgets(commandout, 1048, fp) == 0) {
            fclose(fp);
            break;
        }
        line = commandout;
        ptree temp;
        string field;
        string value;
        size_t index;
        ptree::iterator pit = sysinfo.push_back(make_pair("os", temp));
        pit->second.push_back(make_pair("osdetails", line));
        fclose(fp);
        break;
    }

    std::ostringstream ostr;
    write_json(ostr, sysinfo);
    response = ostr.str();
    std::cout << response << std::endl;

    return true;
}

