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

func TestAcker(t *testing.T) {
	tr := new(mytracker)
	acker := NewLocalAcker(8, tr)
	acker.Start()
	id := acker.AddTracking("hello")
	fmt.Printf("Id returned by acker %d\n", id)
	acker.AddAck(id, 100)
	acker.AddAck(id, 200)
	acker.AddAck(id, 200)
	acker.AddAck(id, 100)
	time.Sleep(2 * time.Second)
}
