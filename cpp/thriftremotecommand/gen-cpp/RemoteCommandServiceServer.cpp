#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <stdio.h>
#include <pthread.h>
#include <iostream>
#include <Thrift.h>
#include <protocol/TBinaryProtocol.h>
#include <server/TSimpleServer.h>
#include <transport/TServerSocket.h>
#include <transport/TBufferTransports.h>
#include <concurrency/PosixThreadFactory.h>

#include "RemoteCommandService.h"

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;
using namespace ::apache::thrift::concurrency;

using boost::shared_ptr;
using std::cout;
using std::endl;

using namespace  ::RemoteCommand;

class RemoteCommandServiceHandler : virtual public RemoteCommandServiceIf {
public:
    RemoteCommandServiceHandler() {
    }

    int32_t executeCommand(const Command& cmd) {
        char *args[256];
        size_t paramsize = cmd.parameters.size();
        size_t i = 1;
        args[0] = (char *)cmd.commandFile.c_str();
        if (paramsize > 255)
            paramsize = 255;
        if (paramsize > 0) {
            while (i <= paramsize) {
                args[i] = (char *)cmd.parameters[i - 1].c_str();
                i++;
            }
        }
        args[i] = 0; 
        pid_t pid = fork();
        if (0 == pid) {
            int fd = open(cmd.stdOutFile.c_str(), O_RDWR| O_TRUNC | O_CREAT, 0644 );
            if (fd > 0 )
                dup2(fd, 1);
            fd = open(cmd.stdErrorFile.c_str(), O_RDWR| O_TRUNC | O_CREAT, 0644 );
            if (fd > 0 )
                dup2(fd, 2);
          
            if (cmd.daemonize)
                daemon(1,1);
            execvp(args[0], args);
        } else if (pid < 0) {
            cout << "Error creating process" << endl;
        }
        return 0;
    }

};

void myoutputdummy(const char *message)
{
    (void) message;
}

void *waitforchildren(void *ptr) 
{
    int status = 0;
    while(true) {
        status = 0;
        usleep(100000);
        wait(&status);
    }
    return 0;
}

int main(int argc, char **argv) {
    GlobalOutput.setOutputFunction(myoutputdummy);
    shared_ptr<RemoteCommandServiceHandler> handler(new RemoteCommandServiceHandler());
    shared_ptr<TProcessor> processor(new RemoteCommandServiceProcessor(handler));
    shared_ptr<TServerTransport> serverTransport(new TServerSocket(9090));
    shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
    shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());
    TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);

    pthread_t childwaiter;
    pthread_create(&childwaiter, 0, waitforchildren, 0);
    server.serve();
    return 0;
}

