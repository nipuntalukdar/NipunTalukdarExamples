#include <string.h>
#include <stdlib.h>
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
    cout << val << endl;
    size_t position = buffer.currentPosition();
    cout << buffer.position(1024) << endl;
    cout << buffer.position(1024) << endl;
    if (buffer.putInt32(100) == false) {
        cout << "Worked as expected \n";
    }
    buffer.position(position);
    buffer.putBytes((void *)"this is my string", strlen("this is my string") + 1);
    void *buf = malloc(strlen("this is my string") + 1);
    buffer.position(position);
    buffer.readBytes(buf, strlen("this is my string") + 1);
    cout << (char *) buf << endl;
    free(buf);
    return 0;
}
