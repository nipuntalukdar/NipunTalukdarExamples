#include <string>
#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <zmq.hpp>

int main ()
{
  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_PUSH);
  socket.bind ("tcp://*:5556");
  int i = 0;
  char data[1024] = "";
  while (true){
      memset(data, 0, 1024);
      snprintf(data,1024, "Pushed data %d", i++);
      zmq::message_t pushdata (strlen(data) + 1);
      memcpy((void *)pushdata.data(), data, strlen(data) + 1);
      socket.send (pushdata);
      sleep(1);
  }
  socket.close();
  context.close();
  return 0;
}
