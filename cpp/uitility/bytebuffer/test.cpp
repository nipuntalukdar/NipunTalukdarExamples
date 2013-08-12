#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <bytebuffer.hpp>
#include <stdio.h>

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
    position = buffer.currentPosition();
    buffer.putInt16(45);
    buffer.position(position);
    cout << buffer.getInt16() << endl;
    cout << "Current position " << buffer.currentPosition() << endl;
    position = buffer.currentPosition();
    buffer.putInt64(-123456789123400);
    buffer.position(position);
    cout << buffer.getInt64() << endl;
    position = buffer.currentPosition() ;
    cout << "Current position " << position << endl;
    buffer.putFloat(-1223.3233);
    buffer.position(position);
    float f  = buffer.getFloat() ;
    printf("%f floattttt\n", f);
    
    position = buffer.currentPosition() ;
    cout << "Current position " << position << endl;
    buffer.putDouble(-1223879967.3233129);
    buffer.position(position);
    cout << buffer.getDouble() << endl;
    buffer.position(position);
    double x = buffer.getDouble();
    printf("%lf \n", x);
    return 0;
}
