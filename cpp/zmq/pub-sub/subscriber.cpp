#include <zmq.hpp>
#include <string>
#include <iostream>
#include <unistd.h>
int main ()
{
  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_SUB);
  socket.connect("tcp://127.0.0.1:5556");
  socket.setsockopt(ZMQ_SUBSCRIBE, "Topic1 ", strlen("Topic1 ") -2);
  int i  = 0;
  while (true){
      zmq::message_t subdata;
      socket.recv (&subdata);
      std::cout << "Received " << (char *)subdata.data() << std::endl;
  }
  return 0;
}
