#include <iostream>
#include <vector>

using namespace std;

class A
{
    public:
        A(){
        }
        A(initializer_list<int>& a) {
            x = a;
        }
        void show()
        {
            for (auto &i : x) {
                cout << i << endl;
            }
        }

    private:
        vector<int> x = {1,2,3};
    
};

int main()
{
    A a;
    a.show();
    initializer_list<int> x = {10,20,30};
    A b(x);
    b.show();
}
