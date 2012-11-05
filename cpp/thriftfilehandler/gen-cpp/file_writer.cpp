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
#include <protocol/TBinaryProtocol.h>
#include <transport/TSocket.h>
#include <transport/TTransportUtils.h>

#include "FileService.h"

using std::cout;
using std::endl;
using std::stringstream;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace FileHandler;

using namespace boost;

int main(int argc, char** argv) {
    shared_ptr<TTransport> file(new TFileTransport("testfiletransport"));
    shared_ptr<TTransport> transport(new TBufferedTransport(file));
    shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
    FileServiceClient client(protocol);
    try {
        int i = 0;
        stringstream ss (stringstream::in | stringstream::out);
        Work work;
        work.data = "mydata";
        work.rootdir = "/home/nipun/test";

        try {
            while (i++ < 100) {
                work.op = Operation::CREATE;
                ss << "filename" << i ;
                work.filename = ss.str();
                ss.clear();
                ss.str("");
                ss << "data" << rand() << "-" << rand() << time(0);
                work.data = ss.str();
                ss.clear();
                ss.str("");
                client.send_createFile(work);

                work.op = Operation::DIRCONTENT;
                ss << "filename" << i  << rand();
                work.filename = ss.str();
                ss.clear();
                ss.str("");
                ss << "data" << rand() << "-" << rand() << time(0) << rand();
                work.data = ss.str();
                ss.clear();
                ss.str("");
                client.send_getFiles(work);
            }
        } catch (BadOperation &op) {
            cout << "Exception "  <<  op.reason  << endl;
        }

    } catch (TException &tx) {
        cout <<  "ERROR: " << tx.what() << endl;
    }
}
