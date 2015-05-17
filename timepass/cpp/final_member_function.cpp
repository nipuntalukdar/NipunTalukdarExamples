#include <iostream>

using namespace std;

class Base
{
public:
    virtual int fun() final
    {
    }
};

class Derived : public Base
{
public:
    // Compiler will throw error
    virtual int fun() override
    {
        return 0;
    }
};

int main()
{
}
