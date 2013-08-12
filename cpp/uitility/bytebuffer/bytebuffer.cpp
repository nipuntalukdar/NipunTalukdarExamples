#include <stdlib.h>
#include <string.h>
#ifndef __USE_BSD
#define __USE_BSD
#endif
#include <endian.h>
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

GeetPutula::ByteBuffer::ByteBuffer(const ByteBuffer& buffer)
{
    _size = buffer._size;
    _position = buffer._position;
    _endian = buffer._endian;
    if (_size > 0) {
        _data = malloc(_size);
        memcpy(_data, buffer._data, _size);
    } else {
        _data = 0;
    }
}

GeetPutula::ByteBuffer& GeetPutula::ByteBuffer::operator=(const ByteBuffer& buffer)
{
    if (this != &buffer) {
        _size = buffer._size;
        _position = buffer._position;
        _endian = buffer._endian;
        if (_data)
            free(_data);
        if (_size > 0) {
            _data = malloc(_size);
            memcpy(_data, buffer._data, _size);
        } else {
            _data = 0;
        }
    }
    return *this;
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
    if (_endian == BIG) 
        converted = htobe32(val);
    else
        converted = htole32(val);
    putBytes((void *)&converted, 4);
    return true;
}

int32_t GeetPutula::ByteBuffer::getInt32()
{
    int32_t val = 0;
    readBytes((void *)&val, 4);
    if (_endian == BIG) 
        return be32toh(val);
    return le32toh(val);
}

bool GeetPutula::ByteBuffer::putInt16(int16_t val)
{
    int16_t converted = 0;
    if (_endian == BIG) 
        converted = htobe16(val);
    else
        converted = htole16(val);
    putBytes((void *)&converted, 2);
    return true;
}

int16_t GeetPutula::ByteBuffer::getInt16()
{
    int16_t val = 0;
    readBytes((void *)&val, 2);
    if (_endian == BIG) 
        return be16toh(val);
    return le16toh(val);
}

bool GeetPutula::ByteBuffer::putInt64(int64_t val)
{
    int64_t converted = 0;
    if (_endian == BIG) 
        converted = htobe64(val);
    else
        converted = htole64(val);
    putBytes((void *)&converted, 8);
    return true;
}

int64_t GeetPutula::ByteBuffer::getInt64()
{
    int64_t val = 0;
    readBytes((void *)&val, 8);
    if (_endian == BIG) 
        return be64toh(val);
    return le64toh(val);
}

bool GeetPutula::ByteBuffer::putUInt32(uint32_t val)
{
    return putInt32((int32_t)val);
}

uint32_t GeetPutula::ByteBuffer::getUInt32()
{
    return (uint32_t) getInt32();
}

bool GeetPutula::ByteBuffer::putUInt16(uint16_t val)
{
    return putInt64((int16_t)val);
}

uint16_t GeetPutula::ByteBuffer::getUInt16()
{
    return (uint16_t) getInt16();
}

bool GeetPutula::ByteBuffer::putUInt64(uint64_t val)
{
    return putInt64((int64_t)val);
}

uint64_t GeetPutula::ByteBuffer::getUInt64()
{
    return (uint64_t)getInt64();
}

bool GeetPutula::ByteBuffer::putDouble(double val)
{
    if ((_position + sizeof(double)) > _size)
        return false;
    if (((_endian == BIG) && littleEndianHost()) ||
            ((_endian == LITTLE) && !littleEndianHost())) {
        // swap needed
        val = __bswap_64(val);
    }
    memcpy((char *)_data + _position, (void *)&val, sizeof(double));
    _position += sizeof(double);
}

double GeetPutula::ByteBuffer::getDouble()
{
    double val = 0.0;

    if ((_position + sizeof(double)) > _size)
        throw ByteBufferException("Cannot get a double from current position");
    memcpy((void *)&val, (char *)_data + _position, sizeof(double));
    if (((_endian == BIG) && littleEndianHost()) ||
            ((_endian == LITTLE) && !littleEndianHost())) {
        // swap needed
        val = __bswap_32(val);
    }
    _position += sizeof(double);
    return val;
}

bool GeetPutula::ByteBuffer::putFloat(float val)
{
    if ((_position + sizeof(float)) > _size)
        return false;
    if (((_endian == BIG) && littleEndianHost()) ||
            ((_endian == LITTLE) && !littleEndianHost())) {
        // swap needed
        val = __bswap_32(val);
    }
    memcpy((char *)_data + _position, (void *)&val, sizeof(float));
    _position += sizeof(float);
}

float GeetPutula::ByteBuffer::getFloat()
{
    float val = 0.0;

    if ((_position + sizeof(float)) > _size)
        throw ByteBufferException("Cannot get a float from current position");
    memcpy((void *)&val, (char *)_data + _position, sizeof(float));
    if (((_endian == BIG) && littleEndianHost()) ||
            ((_endian == LITTLE) && !littleEndianHost())) {
        // swap needed
        val = __bswap_32(val);
    }
    _position += sizeof(float);
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

size_t GeetPutula::ByteBuffer::position(size_t newposition)
{
    size_t oldposition = _position;
    if (newposition > _size)
        _position = _size;
    else
        _position = newposition;
    return oldposition;
}

bool GeetPutula::ByteBuffer::putBytes(void *bytes, size_t size)
{
    if ((_position + size ) > _size)
        return false;
    memcpy((char *)_data + _position, bytes, size);
    _position += size;
    return true;
}

void GeetPutula::ByteBuffer::readBytes(void *dest, size_t size)
{
    if ((_position + size ) > _size)
        throw ByteBufferException("Not enough data to read");
    memcpy(dest , (char *)_data + _position, size);
    _position += size;
}

void GeetPutula::ByteBuffer::proceed(size_t steps)
{
    if ((_position + steps) > _size )
        throw ByteBufferException("Overflow error");
    _position += steps;
}

void GeetPutula::ByteBuffer::back(size_t steps)
{
    if (_position < steps)
        throw ByteBufferException("Underflow error");
    _position -= steps;
}

bool GeetPutula::ByteBuffer::littleEndianHost()
{
#if __BYTE_ORDER == __LITTLE_ENDIAN
    return true;
#else
    return false;
#endif
}
