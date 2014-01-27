/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements. See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership. The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <sstream>
#include <string>
#include <protocol/TBinaryProtocol.h>
#include <transport/TSocket.h>
#include <transport/TTransportUtils.h>

#include "FileService.h"

using std::cout;
using std::endl;
using std::stringstream;
using std::string;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace FileHandler;

using namespace boost;

int main(int argc, char** argv) {
    shared_ptr<TTransport> file(new TFileTransport("testfiletransport", true));
    shared_ptr<TTransport> transport(new TBufferedTransport(file));
    shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
    FileServiceClient client(protocol);
    string fname;
    TMessageType mtype;
    int32_t seqid;
    Work w;
    try {
        while (true) {
            protocol->readMessageBegin(fname, mtype, seqid);
            cout << fname << endl;
            if (fname == "createFile") {
                FileService_createFile_args args;
                args.read(protocol.get());
                protocol->readMessageEnd();
                w = args.w;
            } else if (fname == "getFiles") {
                FileService_getFiles_args args;
                args.read(protocol.get());
                protocol->readMessageEnd();
                w = args.w;
            }
            cout <<"\tData:\t" << w.data << endl;
            cout <<"\tFilename:\t" << w.filename << endl;
            cout <<"\tRootdir:\t" << w.rootdir << endl;
            cout <<"\tOperation:\t" << w.op << endl;

        }
    } catch (TTransportException& e) {
        if (e.getType() == TTransportException::END_OF_FILE) {
            cout << "\n\n\t\tRead All Data successfully\n";
        }
    } catch (TException &tx) {
        cout << "ERROR " <<  tx.what() << endl;
    }
}
