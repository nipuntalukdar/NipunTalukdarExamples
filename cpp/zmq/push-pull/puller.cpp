#include <zmq.hpp>
#include <string>
#include <iostream>
#include <unistd.h>
int main ()
{
  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_PULL);
  socket.connect("tcp://127.0.0.1:5556");
  int i  = 0;
  while (true){
      zmq::message_t pulleddata;
      socket.recv (&pulleddata);
      std::cout << "Pulled: " << (char *)pulleddata.data() << std::endl;
  }
  return 0;
}
