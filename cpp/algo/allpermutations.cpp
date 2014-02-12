#include <iostream>
#include <string>

using std::string;
using std::cout;
using std::endl;

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
    AllPermutation(const string& given) 
    {
        _possibles = given;
        _replsize = given.size();
        _current =  string(_replsize, _possibles.at(0));
        _last =  string(_replsize, _possibles.at(_possibles.size() - 1));
        _exhausted = false;
    }

    AllPermutation(const char* given) 
    {
        _possibles = given;
        _replsize = _possibles.size();
        _current =  string(_replsize, _possibles.at(0));
        _last =  string(_replsize, _possibles.at(_possibles.size() - 1));
        _exhausted = false;
    }
    bool getNext(string& next);
    void reset();
    void mutate_current();

private:
    string _possibles;
    size_t _replsize;
    string _current;
    string _last;
    bool _exhausted ;
};

bool AllPermutation::getNext(string& out)
{
    if (_exhausted) {
        out = _last;
    }
    mutate_current();
    return false;

}

void AllPermutation::mutate_current()
{
    if (_current == _last) {
        _exhausted = true;
        return;
    }
    size_t pos = _replsize - 1;
    while (true) {
    }
}

int main()
{
    AllPermutation x("helo");
    return 0;
}

