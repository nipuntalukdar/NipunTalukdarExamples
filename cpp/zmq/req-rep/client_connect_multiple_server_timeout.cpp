#include <zmq.hpp>
#include <string>
#include <iostream>
#include <unistd.h>

using std::cerr;
using std::cout;
using std::endl;

int main (int argc, char *argv[])
{
  if (argc < 2){
      cerr << "Usage: " << argv[0] << " server1-port server2-port ... ";
      exit(1);
  }

  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_REQ);
  int timeout = 4000;
  socket.setsockopt(ZMQ_SNDTIMEO, &timeout, sizeof(int)); 
  socket.setsockopt(ZMQ_RCVTIMEO, &timeout, sizeof(int)); 

  int i  = 1;
  char transport[128];

  while (i < argc) {
    snprintf(transport, 128, "tcp://127.0.0.1:%s", argv[i++]);
    socket.connect(transport);
  }

  char request_data[1024];
  i = 0;
  while (true){
      do {
        zmq::message_t request (1024);
        snprintf(request_data, 1024, "Hello %08d", i++); 
        memcpy ((void *) request.data (), request_data, strlen(request_data));
        if ( socket.send (request) == false) {
            cout << "Some error in sending request " << endl;
            continue;
        }
        break;
      } while (true);
      do {
        zmq::message_t reply;
        if (socket.recv (&reply) == 0) {
            cout << "Some error in read " << endl;
            continue;
        }
        cout << "Received " << (char *)reply.data() << endl;
        break;
      }while (true);
      sleep(1);
  }
  socket.close();
  context.close();
  return 0;
}
