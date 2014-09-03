#include <zmq.hpp>
#include <string>
#include <iostream>
#include <unistd.h>
int main ()
{
  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_REQ);
  socket.connect("tcp://127.0.0.1:5555");
  int i  = 0;
  while (true){
      zmq::message_t request (1024);
      memcpy ((void *) request.data (), "Hello", 6);
      socket.send (request);
      zmq::message_t reply;
      socket.recv (&reply);
      std::cout << "Received " << (char *)reply.data() 
          << "#times " << i++  << std::endl;
  }
  return 0;
}
