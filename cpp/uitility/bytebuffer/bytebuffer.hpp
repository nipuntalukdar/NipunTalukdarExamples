#ifndef __GEETPUTULA_BYTEBUFFER__
#define __GEETPUTULA_BYTEBUFFER__

#include <inttypes.h>
#include <sys/types.h>

#include <bytebuffer_exception.hpp>

namespace GeetPutula
{

class ByteBuffer
{
public:
    enum Endian{
        BIG, 
        LITTLE
    };

    ByteBuffer(size_t size = 256, Endian endian = BIG  );
    void resize(size_t size);

    bool putInt32(int32_t val);
    int32_t getInt32();
    bool putInt16(int16_t val);
    int16_t getInt16();
    bool putInt64(int64_t val);
    int64_t getInt64();

    bool putUInt32(uint32_t val);
    uint32_t getUInt32();
    bool putUInt16(uint16_t val);
    uint16_t getUInt16();
    bool putUInt64(uint64_t val);
    uint64_t getUInt64();

    bool putFloat(float val);
    float getFloat();
    bool putDouble(double val);
    double getDouble();

    void rewind();
    size_t position(size_t newposition);
    size_t currentPosition() const;
    bool putBytes(void *bytes, size_t size);
    void readBytes(void *dest, size_t size);
    void proceed(size_t steps);
    void back(size_t steps);

    ~ByteBuffer();
private:
    size_t _size;
    size_t _position;
    void *_data;
    Endian _endian;
   
    bool littleEndianHost(); 

};

inline size_t ByteBuffer::currentPosition() const
{
    return _position;
}

} // namespace close

#endif
