#include <unistd.h>
#include <iostream>
#include <boost/asio.hpp>
#include <boost/lexical_cast.hpp>

using boost::asio::ip::tcp;
using boost::asio::ip::address;
using boost::asio::io_service;
using boost::system::error_code;
using boost::lexical_cast;
using boost::bad_lexical_cast;

using std::cout;
using std::endl;

int main(int argc, char *argv[])
{
    if (argc < 3) {
        cout << "Usage " << " <host> <port> " << endl;
        exit(1);    
    }
    
    try {
        io_service ios;
        error_code error;
        tcp::endpoint hostport(address::from_string(argv[1]), lexical_cast<short>(argv[2]));
        tcp::socket socket(ios);
        socket.connect(hostport, error);
        if (error){
            cout << boost::system::system_error(error).what() << endl;
            exit(1);
        }
        int i = 0;
        while (i++ < 20) {
            boost::asio::write(socket, boost::asio::buffer("This is a message"),
                    boost::asio::transfer_all(), error);
            if (error) {
                cout << boost::system::system_error(error).what() << endl;
                exit(1);
            }
            boost::array<char, 128> buff;
            size_t len = socket.read_some(boost::asio::buffer(buff), error);
            if (error) {
                cout << boost::system::system_error(error).what() << endl;
                exit(1);
            }
            cout.write(buff.data() , len);
            cout << endl;
            sleep(2);
        }
        socket.close();
    } catch (bad_lexical_cast &e){
        cout << " problem  " << e.what() << endl;
        exit(2);
    }
    return 0;
}
