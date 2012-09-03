#include <stdio.h>
#include <iostream>
#include <vector>
#include <sstream>

#include <stdint.h>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/xml_parser.hpp>

#include <executor.hpp>
#include <strutil.hpp>

using namespace ourapi;
using std::vector;
using boost::property_tree::ptree;
using std::make_pair;
using boost::lexical_cast;
using boost::bad_lexical_cast;
using boost::format;


Executor::Executor()
{
}

bool Executor::diskinfo(const set<string>& args, outputType type, 
        string& response)
{
    const char *command = "df | sed 's/ \\+/ /g'  | tail -n +2 ";
    char line[255];
    vector<string> tokens;
    int i = 0,j;
    bool spaceinfo = false;
    bool totalparts = false;
    uint64_t totalspace = 0;
    uint64_t usedspace = 0;
    int32_t partnum = 0;

    FILE *fp = popen(command, "r");
    if (!fp){
        return false;
    }
    while (fgets(line, 255, fp) != 0){
        response += string(line);
    }
    fclose(fp);

    if (args.find("spaceinfo") != args.end()) {
        spaceinfo = true;
    }
    if (args.find("totalparts") != args.end()) {
        totalparts = true;
    }


    StrUtil::splitString( response, " \t\n", tokens); 
    
    j = tokens.size();
    ptree diskinforoot ;
    ptree diskinfo;

    ptree::iterator  ptit = diskinforoot.push_back(make_pair("diskinfo", diskinfo ));
    ptree::iterator pit ;
    while (i < j) {
        {
            ptree temp;
            pit = ptit->second.push_back(make_pair("FileSystem", temp));
        }
        pit->second.push_back(make_pair("Name", tokens[i++]));
        try {
            if (spaceinfo) {
                totalspace += lexical_cast<uint64_t>(tokens[i]);
            }
            pit->second.push_back(make_pair("Size", tokens[i++]));
            usedspace += lexical_cast<uint64_t>(tokens[i]);
            pit->second.push_back(make_pair("Used", tokens[i++]));

        } catch ( bad_lexical_cast& e) {
        }
        pit->second.push_back(make_pair("Avail", tokens[i++]));
        pit->second.push_back(make_pair("PercentUse", tokens[i++]));
        pit->second.push_back(make_pair("MountedOn", tokens[i++]));
        partnum++;
    }

    if (spaceinfo) {
        ptree temp;
        format fmter("%1%");
        pit = ptit->second.push_back(make_pair("SpaceInfo", temp));
        fmter % totalspace;
        pit->second.push_back(make_pair("TotalSpace", fmter.str()));
        fmter.clear();
        fmter % usedspace;
        pit->second.push_back(make_pair("UsedSpae", fmter.str()));
        fmter.clear();

    }

    if (totalparts) {
        ptree temp;
        format fmter("%1%");
        fmter % partnum;
        ptit->second.push_back(make_pair("TotalParts", fmter.str()));
        fmter.clear();
    }

    _generateOutput(&diskinforoot, type, response);
    std::cout << response << std::endl;
    return true;
}

bool Executor::procinfo(const set<string>& args, outputType type, 
        string& response)
{
    const char *command = "ps -ef | awk ' { printf \"%s %s %s \", $1, $2, $3 ; for (i = 8; i <= NF; i++) {printf \"%s \", $i }  print \"\" }  ' ";
    char line[2048];

    ptree prcinforoot ;
    ptree prcinfo;
    ptree::iterator  ptit = prcinforoot.push_back(make_pair("prcinfo", prcinfo ));

    FILE *fp = popen(command, "r");
    while (fgets(line, 2048, fp) != 0){
        response += string(line);
    }
    fclose(fp);    
    return true;
}

bool Executor::sysinfo(const set<string>& args, outputType type, 
        string& response)
{
    const char *commandcpu = "cat /proc/cpuinfo |  sed 's/\\s\\+: /:/g'";
    const char *commandmemory = "cat /proc/meminfo |  sed 's/:\\s\\+/:/g'";
    const char *commandos = "uname -a";
    FILE *fp;
    char commandout[1048];
    string line;
    ptree sysinforoot ;
    ptree sysinfo;
    ptree::iterator  ptit = sysinforoot.push_back(make_pair("sysinfo", sysinfo ));

    while (args.empty() || args.find("cpus") != args.end()) {
        fp = popen(commandcpu, "r");
        if (!fp)
            break;
        ptree temp;
        string field;
        string value;
        size_t index;
        ptree::iterator pit;
        while (fgets(commandout, 1048, fp) != 0){
            line = commandout;
            StrUtil::eraseAllChars(line, ")( \r\n\t");
            if (strncasecmp(line.c_str(),"processor:", 10) == 0) {
                pit = ptit->second.push_back(make_pair("cpus", temp));
            }
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
    
    while (args.empty()  ||  args.find("memory") != args.end()) {
        fp = popen(commandmemory, "r");
        if (!fp)
            break;
        ptree temp;
        string field;
        string value;
        size_t index;
        ptree::iterator pit = ptit->second.push_back(make_pair("memory", temp));
        while (fgets(commandout, 1048, fp) != 0){
            line = commandout;
            StrUtil::eraseAllChars(line, ")( \n\r\t");
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
    while (args.empty() || args.find("os") != args.end()) {
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
        ptree::iterator pit = ptit->second.push_back(make_pair("os", temp));
        pit->second.push_back(make_pair("osdetails", line));
        fclose(fp);
        break;
    }

    _generateOutput(&sysinforoot, type, response);
    std::cout << response << std::endl;

    return true;
}

void Executor::_generateOutput(void *data, outputType type, string& output)
{
    std::ostringstream ostr;
    ptree *pt = (ptree *) data;
    if (TYPE_JSON == type)
        write_json(ostr, *pt);
    else if (TYPE_XML == type)
        write_xml(ostr, *pt);

    output = ostr.str();
}

