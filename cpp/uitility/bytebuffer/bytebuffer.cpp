#include <stdlib.h>
#include <string.h>
#include <bytebuffer.hpp>

using GeetPutula::ByteBufferException;
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

void GeetPutula::ByteBuffer::resize(size_t size) 
{
    void *temp = calloc(1, size);
    memcpy(temp, _data, _size > size ? size : _size);
    free(_data);
    _data = temp;
    _size = size;
}

bool GeetPutula::ByteBuffer::putInt32(int32_t val)
{
    int32_t converted = 0;

    if ((4 + _position) > _size)
        return false;
    if (_endian == BIG) 
        converted = htobe32(val);
    else
        converted = htole32(val);
    memcpy((char *)_data + _position , (void *)&converted, 4);
    _position += 4;

    return true;
}

int32_t GeetPutula::ByteBuffer::getInt32()
{
    int32_t val = 0;
    if ((4 + _position) > _size)
        throw ByteBufferException("Invalid position for reading int32_t");
    memcpy((void *)&val, (char *)_data + _position , 4);
    if (_endian == BIG) 
        val = be32toh(val);
    else
        val = le32toh(val);
    _position += 4;

    return val;
}

GeetPutula::ByteBuffer::~ByteBuffer()
{
    if (_data)
        free(_data);
}

void GeetPutula::ByteBuffer::rewind()
{
    _position = 0;
}

void GeetPutula::ByteBuffer::proceed(size_t steps)
{
    if ((_position + steps) > _size )
        throw ByteBufferException("Overflow error");
    _position += steps;
}


