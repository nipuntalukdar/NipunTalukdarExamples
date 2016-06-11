package main

import (
	"dcache"
	"errors"
	"git.apache.org/thrift.git/lib/go/thrift"
)

type DcacheHandler struct {
	vals map[string][]byte
}

func NewDcacheHandler() *DcacheHandler {
	return &DcacheHandler{make(map[string][]byte)}
}

func (dc *DcacheHandler) Put(pc *dcache.PutCommand) (r bool, err error) {
	k := pc.GetKey()
	_, ok := dc.vals[k]
	if ok {
		r = false
		err = errors.New("key exists")
		return
	}
	dc.vals[k] = pc.GetData()
	return true, nil
}

func (dc *DcacheHandler) Get(key string) (r *dcache.GetResponse, err error) {
	d, ok := dc.vals[key]
	if !ok {
		r = nil
		err = errors.New("key doesn't exist")
		return
	}
	data := make([]byte, len(d), len(d))
	copy(data, d)
	return &dcache.GetResponse{key, data}, nil
}

func main() {
	dcacheHandler := NewDcacheHandler()
	dcacheServiceProcessor := dcache.NewDcacheServiceProcessor(dcacheHandler)
	ssock, err := thrift.NewTServerSocket("127.0.0.1:9090")
	if err != nil {
		panic("Problem in creating transport")
	}
	server := thrift.NewTSimpleServer4(dcacheServiceProcessor, ssock,
		thrift.NewTBufferedTransportFactory(204800), thrift.NewTBinaryProtocolFactoryDefault())
	server.Serve()
}
