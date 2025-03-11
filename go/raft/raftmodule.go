package main

import (
	"bufio"
	"bytes"
	"encoding/gob"
	"errors"
	"fmt"
	"github.com/hashicorp/raft"
	raftboltdb "github.com/hashicorp/raft-boltdb/v2"
	"io"
	"os"
	"strings"
	"sync"
	"time"
)

type MyFsm struct {
	mutex *sync.Mutex
	data  map[string]string
}

func NewMyFsm() *MyFsm {
	mutex := &sync.Mutex{}
	data := make(map[string]string)
	return &MyFsm{mutex: mutex, data: data}
}

type MyFsmSnapshot struct {
	mfsm *MyFsm
}

func NewMyFsmSnapshot(fsm *MyFsm) *MyFsmSnapshot {
	return &MyFsmSnapshot{fsm}
}

func (mfsm *MyFsm) Get(key string) (string, error) {
	mfsm.mutex.Lock()
	defer mfsm.mutex.Unlock()
	val, ok := mfsm.data[key]
	if ok {
		return val, nil
	} else {
		return "", errors.New("Key not found")
	}

}

func (mfsm *MyFsm) Apply(log *raft.Log) interface{} {
	mfsm.mutex.Lock()
	defer mfsm.mutex.Unlock()
	ds := string(log.Data)
	kvs := strings.SplitN(ds, ":", 2)
	if len(kvs) != 2 {
		return false
	}
	mfsm.data[kvs[0]] = kvs[1]
	return true
}

func (mfsm *MyFsm) Snapshot() (raft.FSMSnapshot, error) {
	fmt.Printf("Do snapshot..................\n")
	return NewMyFsmSnapshot(mfsm), nil
}

func (mfsm *MyFsm) Restore(inp io.ReadCloser) error {
	defer inp.Close()
	fmt.Printf("Restore......................\n")
	mfsm.mutex.Lock()
	defer mfsm.mutex.Unlock()
	var buffer bytes.Buffer
	readdata := make([]byte, 1024)
	for {
		n, err := inp.Read(readdata)
		if err != nil {
			panic(err)
		}
		if n < 1024 {
			if n > 0 {
				lastbytes := make([]byte, n)
				copy(readdata, lastbytes)
				buffer.Write(lastbytes)
			}
			break
		} else {
			buffer.Write(readdata)
		}
	}
	dec := gob.NewDecoder(&buffer)
	err := dec.Decode(&mfsm.data)
	exitOnError(err)
	return nil
}

func (mfsm *MyFsm) Persist(sink raft.SnapshotSink) error {
	mfsm.mutex.Lock()
	defer mfsm.mutex.Unlock()

	var buffer bytes.Buffer
	enc := gob.NewEncoder(&buffer)
	enc.Encode(mfsm.data)
	n, err := sink.Write(buffer.Bytes())
	if err != nil {
		fmt.Printf("Error in snapshotting %s\n", err)
		return err
	}
	fmt.Printf("Snapshotted %d bytes", n)
	return nil
}

func (mfsmsh *MyFsmSnapshot) Persist(sink raft.SnapshotSink) error {
	fmt.Printf("Persist...................\n")
	mfsmsh.mfsm.Persist(sink)
	return nil
}

func (mfsmsh *MyFsmSnapshot) Release() {
	fmt.Printf("Released\n")
}

func exitOnError(err error) {
	if err != nil {
		fmt.Printf("Error %s\n", err)
		os.Exit(1)
	}
}

func raftFutureErrorCheck(future raft.ApplyFuture) {
	if err := future.Error(); err != nil {
		fmt.Printf("Apply Error 1: %v\n", err)
	}

	if !future.Response().(bool) {
		fmt.Printf("Apply Error 2:\n")
	}
}

func main() {
	sstore, err := raftboltdb.NewBoltStore("/tmp/stablestore")
	if err != nil {
		fmt.Printf("%v", err)
		os.Exit(1)
	}

	logstore, err := raftboltdb.NewBoltStore("/tmp/logstore")
	if err != nil {
		fmt.Printf("Failed to create logstore")
		os.Exit(1)
	}
	snaps, err := raft.NewFileSnapshotStoreWithLogger("/tmp/snapshots", 3, nil)
	exitOnError(err)
	transport, err := raft.NewTCPTransport("127.0.0.1:7000", nil, 10, 10*time.Second, nil)
	exitOnError(err)
	conf := raft.DefaultConfig()
	conf.SnapshotThreshold = 40
	conf.SnapshotInterval = 10 * time.Second
	conf.LocalID = raft.ServerID("myid")
	var configuration raft.Configuration
	configuration.Servers = append(configuration.Servers, raft.Server{Suffrage: raft.Voter,
		ID: conf.LocalID, Address: transport.LocalAddr()})
	raft.BootstrapCluster(conf, logstore, sstore, snaps, transport, configuration)
	fsm := NewMyFsm()
	raftmod, err := raft.NewRaft(conf, fsm, logstore, sstore, snaps, transport)
	time.Sleep(2 * time.Second)
	fmt.Printf("Leader is %v\n", raftmod.Leader())
	future := raftmod.Apply([]byte("hello:value"), 0)
	raftFutureErrorCheck(future)
	i := 0
	for ; i < 100; i++ {
		time.Sleep(2 * time.Millisecond)
		future := raftmod.Apply([]byte(fmt.Sprintf("key%d:value%d", i, i)), 0)
		raftFutureErrorCheck(future)
	}
	fmt.Printf("Do some fun\n")

	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Printf("Enter 1 to put, 2 to get, 3 to quit: ")
		text, _ := reader.ReadString('\n')
		text = strings.Trim(text, "\n")
		if text == "3" {
			os.Exit(0)
		} else if text == "1" {
			fmt.Printf("Key: ")
			key, _ := reader.ReadString('\n')
			key = strings.Trim(key, "\n\b \t\b")
			if key == "" {
				fmt.Printf("Empty key, continuing")
				continue
			}
			fmt.Printf("Value: ")
			value, _ := reader.ReadString('\n')
			value = strings.Trim(value, "\n")
			raftmod.Apply([]byte(fmt.Sprintf("%s:%s", key, value)), 0)
		} else if text == "2" {
			fmt.Printf("Key: ")
			key, _ := reader.ReadString('\n')
			key = strings.Trim(key, "\n\b \t\b")
			if key == "" {
				fmt.Printf("Empty key, continuing")
				continue
			}
			val, err := fsm.Get(fmt.Sprintf(key))
			if err != nil {
				fmt.Printf("Failed to get %s\n", key)
			} else {
				fmt.Printf("The value for key:%s is %s\n", key, val)
			}
		}
	}

}
