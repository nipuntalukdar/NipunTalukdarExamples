#include <bytebuffer_exception.hpp>

GeetPutula::ByteBufferException::ByteBufferException(const char *message) 
    :_message(message)
{
}

const char* GeetPutula::ByteBufferException::what() const throw()
{
    return _message;
}

