#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

/*
    Move the zeros to the end,
    If zeros to move to the start,
    we should start from the end of the
    array for efficiency
*/


void move_zero(vector<int>& nums)
{
    size_t n = nums.size();
    if (n < 2) {
        return;
    }
    
    int pos = 0, start_zero = -1;
    while (pos < n) {
        if (nums[pos] > 0 && start_zero != -1) {
            nums[start_zero] = nums[pos]; 
            nums[pos] = 0;
            start_zero++;
        } else {
            if (start_zero == -1) {
                start_zero = pos;
            }
        }
        pos++;
    }
}

int main() {
    vector<int> x = {0, 1, 2,0, 0, 3,0,4};
    move_zero(x);
    for_each(x.begin(), x.end(), [](int a) { cout << a << " "; });
    cout << endl;
}
