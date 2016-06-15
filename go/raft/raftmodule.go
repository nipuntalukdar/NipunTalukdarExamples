package main

import (
	"fmt"
	"github.com/hashicorp/raft"
	"github.com/hashicorp/raft-boltdb"
	"io"
	"os"
	"time"
)

type MyFsm struct {
}

type MyFsmSnapshot struct {
}

func (mfsm *MyFsm) Apply(log *raft.Log) interface{} {
	return true
}

func (mfsm *MyFsm) Snapshot() (raft.FSMSnapshot, error) {
	return &MyFsmSnapshot{}, nil
}

func (mfsm *MyFsm) Restore(inp io.ReadCloser) error {
	inp.Close()
	return nil
}

func (mfsmsh *MyFsmSnapshot) Persist(sink raft.SnapshotSink) error {
	return nil
}

func (mfsmsh *MyFsmSnapshot) Release() {
}

func errorOnExit(err error) {
	if err != nil {
		fmt.Printf("Error %s\n", err)
		os.Exit(1)
	}
}

func main() {
	var syr *raft.Raft = nil
	fmt.Printf("%v\n", syr)
	sstore, err := raftboltdb.NewBoltStore("/tmp/stablestore")
	fmt.Printf("%v\n", sstore)

	if err != nil {
		fmt.Printf("%v", err)
		os.Exit(1)
	}

	logstore, err := raftboltdb.NewBoltStore("/tmp/logstore")
	if err != nil {
		fmt.Printf("Failed to create logstore")
		os.Exit(1)
	}
	fmt.Printf("%v\n", logstore)

	snaps, err := raft.NewFileSnapshotStoreWithLogger("/tmp/snapshots", 3, nil)
	errorOnExit(err)
	transport, err := raft.NewTCPTransport("127.0.0.1:7000", nil, 10, 10*time.Second, nil)
	errorOnExit(err)
	peerstore := raft.NewJSONPeers("/tmp/peers", transport)
	conf := raft.DefaultConfig()
	conf.EnableSingleNode = true
	raftmod, err := raft.NewRaft(conf, &MyFsm{}, logstore, sstore,
		snaps, peerstore, transport)
	fmt.Printf("%v\n", raftmod)
	time.Sleep(2 * time.Second)
	fmt.Printf("Leader is %v\n", raftmod.Leader())
	time.Sleep(200000 * time.Second)
}
