SRCS=   client.cpp  filehandler_constants.cpp  filehandler_types.cpp  FileService.cpp  \
	FileService_server.skeleton.cpp
THRIFT_LIB_DIR=/usr/local/lib
BOOST_INCL=/usr/local/include
THRIFT_INCLUDE=/usr/local/include/thrift


OBJS=$(SRCS:.cpp=.o)

CFLAGS+=-Wall  -I. -I${BOOST_INCL} -I${THRIFT_INCLUDE} -g  

LDFLAGS+= -L/usr/local/lib   -lthrift

%.o : %.cpp
	${CXX} -c ${CFLAGS} -o $@ $<

client: ${OBJS}
	${CXX} -g  -o client client.o  filehandler_constants.o  filehandler_types.o \
	FileService.o   ${LDFLAGS}

server: ${OBJS}
	${CXX} -g  -o   server  filehandler_types.o \
	FileService.o  FileService_server.skeleton.o ${LDFLAGS}

all: client server

clean:
	rm -f *.o client server
