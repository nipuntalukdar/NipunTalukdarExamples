#include <zmq.hpp>
#include <string>
#include <iostream>

using std::cerr;
using std::cout;
using std::endl;

int main (int argc, char *argv[])
{
  if (argc != 2) {
    cerr << argv[0] << " " << "bind-port" << endl;
    exit(1);
  }

  char transport[255] = "";
  zmq::context_t context (1);
  zmq::socket_t socket (context, ZMQ_REP);
  snprintf(transport, 255, "tcp://*:%s", argv[1]);
  socket.bind (transport);

  char response[2048]; 
  memset(response, 0, 2048);
  snprintf(response, 2048, "Response from server lisetning on %s", argv[1]);
  int i = strlen(response);
  int times = 0;
  
  while (true){
      zmq::message_t request;
      socket.recv (&request);
      zmq::message_t reply (2048);
      snprintf(response + i , 2048, " #%d -- request data: %s", 
              times++, (char *)request.data());
      memcpy ((void *) reply.data (), response, strlen(response));
      socket.send (reply);
  }
  socket.close();
  context.close();
  return 0;
}
