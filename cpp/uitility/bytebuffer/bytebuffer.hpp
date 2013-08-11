#ifndef __GEETPUTULA_BYTEBUFFER__
#define __GEETPUTULA_BYTEBUFFER___

#include <inttypes.h>
#include <sys/types.h>

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
    bool allocate(size_t size);
    void deallocate();
    bool reallocate(uint32_t size);
    void putInt32();
    void putInt32();
    void rewind();
    size_t position();
    ~ByteBuffer();
private:
    size_t _size;
    size_t _position;
    void *_data;
    Endian _endian;

};

} // namespace close

#endif
