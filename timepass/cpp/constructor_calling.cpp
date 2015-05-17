#include <iostream>

using namespace std;

class A 
{
public:
    A() : A(0,0) {}
    A(int a, int b) : x(a), y(b) {}
private:
    int x, y;
};

class B
{   

public:
    auto show() -> int 
    {
        cout << x << "  " << y << endl;
        return 0;
    }
private:
    int x = 1;
    int y = 2;

};

int main()
{
    A a;
    B b;
    b.show();
    return 0;
}
