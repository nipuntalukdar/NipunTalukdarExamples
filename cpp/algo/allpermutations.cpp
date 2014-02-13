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
        _possibles = "";
        _replsize = 0;
        _current = "";
        _last = "";
        _exhausted = false;
    }
    AllPermutation(const string& given, size_t replsize) 
    {
        if (replsize < 0) {
            throw "Invalid replacement size";
        }
        _possibles = given;
        _replsize = replsize;
        _current =  string(_replsize, _possibles.at(0));
        _last =  string(_replsize, _possibles.at(_possibles.size() - 1));
        _exhausted = false;
    }

    AllPermutation(const char* given, size_t replsize) 
    {
        if (replsize < 0) {
            throw "Invalid replacement size";
        }
        _possibles = given;
        _replsize = replsize;
        _current =  string(_replsize, _possibles.at(0));
        _last =  string(_replsize, _possibles.at(_possibles.size() - 1));
        _exhausted = false;
        buildNextCharMap();
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
};

bool AllPermutation::getNext(string& out)
{
    if (_exhausted) {
        out = _last;
        return false;
    }
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
            _current.
        }
        if (pos == 0) {
            if (cur == _max)
                _exhausted = true;
            break;
        }
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

int main()
{
    AllPermutation x("helo", 4);
    return 0;
}

