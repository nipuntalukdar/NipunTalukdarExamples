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

  int i  = 1;
  char transport[128];

  while (i < argc) {
    snprintf(transport, 128, "tcp://127.0.0.1:%s", argv[i++]);
    socket.connect(transport);
  }

  while (true){
      zmq::message_t request (1024);
      memcpy ((void *) request.data (), "Hello", 6);
      socket.send (request);
      zmq::message_t reply;
      socket.recv (&reply);
      cout << "Received " << (char *)reply.data() << endl;
      sleep(1);
  }
  socket.close();
  context.close();
  return 0;
}
