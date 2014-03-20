#include <string.h>
#include <iostream>
#include <string>
#include <vector>
#include <map>

using std::string;
using std::cout;
using std::endl;
using std::map;
using std::vector;

class AllPermutation
{
public:
    AllPermutation()
    {   
        initForBlankStr();
    }
    AllPermutation(const string& given, size_t replsize) 
    {
        initForStr(given.c_str(), replsize);

    }

    AllPermutation(const char* given, size_t replsize) 
    {
        initForStr(given, replsize);
    }
    bool getNext(string& next);
    void reset();


private:
    string _possibles;
    size_t _replsize;
    string _current;
    string _last;
    vector<char> _uniquechars;
    map<char, char> _nextchars;
    bool _exhausted ;
    char _max;
    char _min;
    void mutateCurrent();
    void buildNextCharMap();
    void initForBlankStr();
    void initForStr(const char* str, size_t replsize);
};

void AllPermutation::initForBlankStr()
{
    _possibles = "";
    _replsize = 0;
    _current = "";
    _last = "";
    _exhausted = true;
}

void AllPermutation::initForStr(const char* str, size_t replsize)
{
    if (replsize <= 0 || str == NULL || strlen(str) == 0) {
        throw "Invalid replacement ";
    }
    _possibles = str;
    _replsize = replsize;
    buildNextCharMap();
    _current =  string(_replsize, _uniquechars[0]);
    _last =  string(_replsize, _uniquechars[_uniquechars.size() -1 ]);
    _exhausted = false;
    if (_current == _last)
        _exhausted = false;
}

bool AllPermutation::getNext(string& out)
{
    if (_exhausted) {
        out = _last;
        return false;
    }
    out = _current;
    mutateCurrent();
    return true;

}

void AllPermutation::mutateCurrent()
{
    size_t pos = _replsize - 1;
    char cur ;
    while (true) {
        cur = _current.at(pos);
        if (cur == _max) {
            if (pos == 0) {
                // cannot increment anymore
                _exhausted = true;
                break;
            }
            _current.replace(pos,1,1, _min);
        } else {
            _current.replace(pos,1,1, _nextchars[cur]);
            break;
        }
        pos--;
    }
}

void AllPermutation::buildNextCharMap()
{
    size_t givenSize = _possibles.size();
    size_t i = 0;
    char next ;
    char cur;
    while (i < givenSize) {
        if (_nextchars.find(_possibles.at(i)) != _nextchars.end()) {
            i++;
            continue;
        }
        _nextchars[_possibles.at(i)] = _possibles.at(i);
        _uniquechars.push_back(_possibles.at(i));
        i++;
    }

    // Now set the next uniq char in map correctly
   givenSize = _uniquechars.size();
   _max = _uniquechars[givenSize - 1] ;
   _min = _uniquechars[0];
   if (givenSize < 2)
       return;
   i = 0;
   while (i < givenSize) {
       _nextchars[_uniquechars[i]] = _uniquechars[(i + 1) % givenSize];
       i++;
   }

   map<char, char>:: iterator it = _nextchars.begin();
   while (it != _nextchars.end()){
       cout << it->first << "=> " << it->second << endl;
       ++it;
   }

}

// Below is an example run
int main()
{
    int i = 0;
    try {
        AllPermutation x("abcxYABCNc", 4);
        string nextcomb;
        while (x.getNext(nextcomb)) {
            i++;
            cout << nextcomb << endl;
        }
        cout << i << " " <<  " replacements \n";
    } catch (const char *what) {
        cout << what << endl;
    }
    return 0;
}

