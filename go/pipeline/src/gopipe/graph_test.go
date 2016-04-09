package gopipe

import (
	"testing"
)

func TestExecutionGraphCycle(t *testing.T) {
	npl := GetNewGraphNodePool()
	node1 := npl.Get("1")
	node2 := npl.Get("2")
	node3 := npl.Get("3")
	node4 := npl.Get("4")
	node1.AddOutNode(node2)
	node2.AddOutNode(node3)
	node3.AddOutNode(node4)
	node4.AddOutNode(node1)
	if !npl.DetectAnyCycle() {
		t.Error("Failed to detect cycle")
	}
}

func TestExecutionGraphNoCycle(t *testing.T) {
	npl := GetNewGraphNodePool()
	node1 := npl.Get("1")
	node2 := npl.Get("2")
	node3 := npl.Get("3")
	node4 := npl.Get("4")
	node1.AddOutNode(node2)
	node2.AddOutNode(node3)
	node3.AddOutNode(node4)
	if npl.DetectAnyCycle() {
		t.Error("False cycle detected")
	}
}
