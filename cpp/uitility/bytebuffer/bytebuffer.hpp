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
    void rewind();
    size_t position();
    ~ByteBuffer();
private:
    size_t _size;
    size_t _position;
    void *_data;
    Endian _endian;
    
    void proceed(size_t steps);

};

} // namespace close

#endif
