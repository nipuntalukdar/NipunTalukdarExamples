package gopipe

import (
	"fmt"
	"testing"
	"time"
)

type mytracker struct {
}

func (tr *mytracker) Ack(id string) {
	fmt.Printf("Received ack for %s\n", id)
}

func (tr *mytracker) Fail(id string) {
	fmt.Printf("Failure for %s\n", id)
}

func (tr *mytracker) TimedOut(id string) {
	fmt.Printf("TimeOut for %s\n", id)
}

func TestAcker(t *testing.T) {
	tr := new(mytracker)
	acker := NewLocalAcker(8, tr, 4)
	acker.Start()
	id := acker.AddTracking("hello")
	fmt.Printf("Id returned by acker %d\n", id)
	acker.AddAck(id, 100)
	acker.AddAck(id, 200)
	acker.AddAck(id, 200)
	acker.AddAck(id, 100)
	id = acker.AddTracking("hi")
	acker.AddAck(id, 100)
	acker.AddAck(id, 200)
	acker.AddAck(id, 200)
	acker.SignalFail(id)
	id = acker.AddTracking("hey")
	time.Sleep(10 * time.Second)

}
