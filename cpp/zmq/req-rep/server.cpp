#include <zmq.hpp>
#include <string>
#include <iostream>
#include <unistd.h>
int main ()
{
  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_REP);
  socket.bind ("tcp://*:5555");
  int i = 0;
  while (true){
      zmq::message_t request;
      socket.recv (&request);
      std::cout << "Received " << (char *)request.data() << " #times: " << i++ << std::endl;
      zmq::message_t reply (1024);
      memcpy ((void *) reply.data (), "World", 6);
      socket.send (reply);
  }
  socket.close();
  context.close();
  return 0;
}
