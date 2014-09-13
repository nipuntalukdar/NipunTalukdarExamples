server : server.cpp
	g++ -g -o server server.cpp -lzmq
server_arg: server_arg_port.cpp 
	g++ -g -o server_arg server_arg_port.cpp -lzmq
client : client.cpp
	g++ -g -o client client.cpp -lzmq
client_connect_to_many : client_connect_multiple_server.cpp
	g++ -g -o client_connect_to_many client_connect_multiple_server.cpp -lzmq

all: server server_arg client client_connect_to_many client
clean:
	rm -f server server_arg client client_connect_to_many client
