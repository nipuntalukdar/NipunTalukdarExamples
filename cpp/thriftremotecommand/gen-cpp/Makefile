SRCS=   remotecommand_constants.cpp remotecommand_constants.h \
		RemoteCommandServiceClient.cpp RemoteCommandService.cpp \
		RemoteCommandService.h RemoteCommandServiceServer.cpp \
		remotecommand_types.cpp remotecommand_types.h
THRIFT_LIB_DIR=/usr/local/lib
BOOST_INCL=/usr/local/include
THRIFT_INCLUDE=/usr/local/include/thrift


OBJS=$(SRCS:.cpp=.o)

CFLAGS+=-Wall  -I. -I${BOOST_INCL} -I${THRIFT_INCLUDE} -g  

LDFLAGS+=  -levent -lthrift -lthriftnb -lrt

%.o : %.cpp
	${CXX} -c ${CFLAGS} -o $@ $<

remclient: ${OBJS}
	${CXX} -g  -o remclient RemoteCommandServiceClient.o  \
		remotecommand_constants.o RemoteCommandService.o \
		remotecommand_types.o   ${LDFLAGS}

remserver: ${OBJS}
	${CXX} -g  -o remserver RemoteCommandServiceServer.o  \
		remotecommand_constants.o RemoteCommandService.o \
		remotecommand_types.o   ${LDFLAGS}

all: remclient remserver 

clean:
	rm -f *.o remclient remserver
