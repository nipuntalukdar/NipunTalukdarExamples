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
	fmt.Printf("TimeOut for %s, at %v\n", id, time.Now().Unix())
}

func TestAcker(t *testing.T) {
	tr := new(mytracker)
	acker := NewLocalAcker(8, 4)
	acker.AddTracker(1, tr)
	acker.Start()
	id := acker.AddTracking("hello", 1)
	fmt.Printf("Id returned by acker %d for hello\n", id)
	acker.AddAck(id, 100)
	acker.AddAck(id, 200)
	acker.AddAck(id, 200)
	acker.AddAck(id, 100)
	id = acker.AddTracking("hi", 1)
	fmt.Printf("Id returned by acker %d for hi\n", id)
	acker.AddAck(id, 100)
	acker.AddAck(id, 200)
	acker.AddAck(id, 200)
	acker.SignalFail(id)
	time.Sleep(5 * time.Second)
	id = acker.AddTracking("hey", 1)
	fmt.Printf("Id returned by acker %d for hey\n", id)
	time.Sleep(2 * time.Second)
	id = acker.AddTracking("after4", 1)
	fmt.Printf("Id returned by acker %d for after4\n", id)
	id = acker.AddTracking("after4_1", 1)
	fmt.Printf("Id returned by acker %d for after4_1\n", id)
	time.Sleep(7 * time.Second)

}
