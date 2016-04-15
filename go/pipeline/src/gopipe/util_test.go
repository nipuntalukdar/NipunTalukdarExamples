package gopipe

import (
	"fmt"
	"testing"
)

func TestUtil(t *testing.T) {
	x := NewRandomUUID()
	if x == nil {
		t.Fatalf("Invalid value returned")
	} else {
		fmt.Printf("UUID %v\n", x)
	}
	x = NewRandomUUID()
	if x == nil {
		t.Fatalf("Invalid value returned")
	} else {
		fmt.Printf("UUID %v\n", x)
	}
}
