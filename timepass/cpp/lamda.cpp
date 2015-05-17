#include <iostream>
#include <algorithm>
#include <vector>

int main()
{
    std::vector <int> x = {1,2,3};
    std::for_each(x.begin(), x.end(), [](int x) { std::cout << x << std::endl; });
}
