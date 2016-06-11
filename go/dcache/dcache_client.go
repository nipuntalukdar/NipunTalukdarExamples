package main

import (
	"dcache"
	"fmt"
	"git.apache.org/thrift.git/lib/go/thrift"
)

func main() {
	trans, err := thrift.NewTSocket("127.0.0.1:9090")
	if err != nil {
		panic(err)
	}
	protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()
	transport := thrift.NewTBufferedTransport(trans, 204800)
	defer transport.Close()
	if err = transport.Open(); err != nil {
		panic(err)
	}
	client := dcache.NewDcacheServiceClientFactory(trans, protocolFactory)
	status, err := client.Put(&dcache.PutCommand{"key1", []byte("value for key1")})
	if !status {
		fmt.Println(err)
	}
	status, err = client.Put(&dcache.PutCommand{"key2", []byte("value for key2")})
	if !status {
		fmt.Println(err)
	}
	resp, err := client.Get("key1")
	if err == nil {
		fmt.Printf("Value for key:%s is: %s\n", resp.GetKey(), string(resp.GetData()))
	}
}
