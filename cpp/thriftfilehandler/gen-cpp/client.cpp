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

#include <iostream>
#include <protocol/TBinaryProtocol.h>
#include <transport/TSocket.h>
#include <transport/TTransportUtils.h>

#include "FileService.h"

using std::cout;
using std::endl;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace FileHandler;

using namespace boost;

int main(int argc, char** argv) {
  shared_ptr<TTransport> socket(new TSocket("127.0.0.1", 9090));
  shared_ptr<TTransport> transport(new TBufferedTransport(socket));
  shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
  FileServiceClient client(protocol);

  try {
    transport->open();

    Work work;
    work.op = Operation::CREATE;
    work.filename = "myfile";
    work.data = "mydata";
    work.rootdir = "/home/nipun/test";

    try {
      int32_t status = client.createFile(work);
      cout << "Returned status " << status << endl;
    } catch (BadOperation &op) {
        cout << "Exception "  <<  op.reason  << endl;
    }
    transport->close();

  } catch (TException &tx) {
    printf("ERROR: %s\n", tx.what());
  }

}
