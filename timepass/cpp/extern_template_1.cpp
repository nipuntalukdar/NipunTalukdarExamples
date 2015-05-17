#include <iostream>
#include <vector>

using namespace std;
extern template class vector<int>;


int main()
{
    vector<int> x = {1,2, 3};
}
