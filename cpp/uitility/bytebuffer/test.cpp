#include <iostream>
#include <bytebuffer.hpp>

using namespace GeetPutula;
using namespace std;

int main()
{
    ByteBuffer buffer(256, ByteBuffer::LITTLE);
    buffer.putInt32(102);
    buffer.rewind();
    int32_t val = buffer.getInt32();
    cout << val << endl;
    val = buffer.getInt32();
    return 0;
}
