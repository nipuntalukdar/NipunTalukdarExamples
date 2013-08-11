#ifndef __GEETPUTULA_BYTEBUFFEREXCEPTION__
#define __GEETPUTULA_BYTEBUFFEREXCEPTION__

#include <inttypes.h>
#include <sys/types.h>
#include <exception>

using std::exception;

namespace GeetPutula
{

class ByteBufferException : public exception
{
public:
    ByteBufferException(const char* message = "ByteBuffer execption");
    virtual const char* what() const throw();

private:
    const char *_message;

};

} // namespace GeetPutula

#endif
