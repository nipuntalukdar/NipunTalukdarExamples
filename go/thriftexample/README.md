 A source code line counter

## Thrift example for go with steps added
This is built upon the sources from [Thrift tutorial](https://github.com/apache/thrift/tree/master/tutorial) and [Thrift Go Example](https://github.com/apache/thrift/tree/master/tutorial/go)

Go module "thriftex inited by running the below command:
```
$ go mod init thriftex
```
The files in shared and tutorial folders are generated using the below commands:
```
thrift --gen go:package_prefix=thriftex/  -out . thriftfiles/shared.thrift
thrift --gen go:package_prefix=thriftex/  -out . thriftfiles/tutorial.thrift
```
Files in main directory was modifed to reflect the structure of the module (thriftex). 
Go dependency was updated:
```
$ go mod tidy
```

Then we can run the clients and servers as shown:
```
$ cd main
$ go build
$ ./main -server
$ # From another ternminal run the client:
$ ./main
```
