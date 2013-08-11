#include <stdlib.h>
#include <bytebuffer.hpp>

GeetPutula::ByteBuffer::ByteBuffer(size_t size, Endian endian)
{
    _size = size;
    _position = 0;
    _endian = endian;
    if (size > 0)
        _data = calloc(1, size);
    else
        _data = 0;
}

GeetPutula::ByteBuffer::~ByteBuffer()
{
    if (_data)
        free(_data);
}

