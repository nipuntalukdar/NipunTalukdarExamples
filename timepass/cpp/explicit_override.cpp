#include <iostream>

using namespace std;

class Base
{
public:
    virtual int fun()
    {
    }
};

class Derived : public Base
{
public:
    virtual int fun() override 
    {
        return 0;
    }
};

int main()
{
    Derived *d = new Derived();
    d->fun();
    delete d;
}
