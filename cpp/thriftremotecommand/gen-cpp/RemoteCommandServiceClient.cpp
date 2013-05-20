#include <iostream>
#include <protocol/TBinaryProtocol.h>
#include <transport/TSocket.h>
#include <transport/TTransportUtils.h>

#include "RemoteCommandService.h"

using std::cout;
using std::endl;
using std::cerr;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace RemoteCommand;


int main(int argc, char** argv) {

    if (argc < 3 ) {
        cerr << "Usage " << argv[0] << " host " << " command-file " << " parameters\n";
    }

    boost::shared_ptr<TTransport> socket(new TSocket(argv[1], 9090));
    boost::shared_ptr<TTransport> transport(new TBufferedTransport(socket));
    boost::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
    RemoteCommandServiceClient client(protocol);

    try {
        Command cmd;
        cmd.op = Operation::EXECUTEBIN;
        cmd.commandFile = argv[2];
        cmd.isBinary = true;
        int i = 3;
        while (i < argc) 
            cmd.parameters.push_back(argv[i++]);
        cmd.stdErrorFile = "/dev/null";
        cmd.stdOutFile = "/dev/null";
        cmd.daemonize = true;

        transport->open();
        int32_t status = client.executeCommand(cmd);
        cout << "Returned status " << status << endl;
        transport->close();

    } catch (BadOperation &op) {
        cout << "Exception "  <<  op.reason  << endl;
    } catch (TException &tx) {
        printf("ERROR: %s\n", tx.what());
    }
    if (transport->isOpen()){
        transport->close();
    }
}
