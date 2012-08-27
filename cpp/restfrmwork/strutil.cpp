#include <boost/algorithm/string.hpp>

#include <strutil.hpp>
using namespace ourapi;


void StrUtil::eraseWhiteSpace(string& val)
{
    boost::erase_all(val," ");
    boost::erase_all(val,"\n");
    boost::erase_all(val,"\t");
    boost::erase_all(val,"\r");
}

void StrUtil::splitString(const string& input, const char* delims,
        vector <string>& tokens)
{
    
    boost::split( tokens, input, boost::is_any_of(delims), boost::token_compress_on ); 

}

