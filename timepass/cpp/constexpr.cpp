#include <iostream>

using namespace std;

constexpr int get_five() { return 5; }
constexpr int x = 2;
int main()
{
    int a[get_five()];
}
