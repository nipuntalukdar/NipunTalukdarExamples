#include <string>
#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <zmq.hpp>

int main ()
{
  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_PUB);
  socket.bind ("tcp://*:5556");
  int i = 0;
  char data[1024] = "Topic1 data ";
  while (true){
      memset(data, 0, 1024);
      snprintf(data,1024, "Topic1 data %ld", random());
      zmq::message_t reply (strlen(data) + 1);
      memcpy((void *)reply.data(), data, strlen(data) + 1);
      socket.send (reply);
      sleep(1);
  }
  socket.close();
  context.close();
  return 0;
}
