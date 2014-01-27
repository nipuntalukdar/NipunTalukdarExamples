#!/bin/bash
BlankLine()
{
    echo ""
}
openssl genrsa -des3 -out server.key 1024
BlankLine
echo "Now we remove the password for the server key, please enter the password for the server key, when prompted "
echo "*****************************"
openssl rsa -in server.key -out server_nopassword.key
rm -f server.key
mv server_nopassword.key server.key
BlankLine
echo "Now generating certificate sigining request named server.csr"
rm -f server.csr
openssl req -new -key server.key -out server.csr
BlankLine
echo "Now creating the server certificate nameed server.crt"
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
BlankLine
echo "Displaying the content of the certificate you just created"
openssl x509 -in server.crt -text -noout
echo "Private key is stored in file server.key"
echo "Certificate sign request in file server.csr"
echo "Self-signed certificate in server.crt"
exit $?
