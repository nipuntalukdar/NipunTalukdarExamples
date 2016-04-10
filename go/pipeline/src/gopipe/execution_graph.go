package gopipe

import (
	"fmt"
)

type GraphNode struct {
	Name     string
	outnodes []*GraphNode
	innodes  []*GraphNode
}

type GraphNodePool struct {
	nodes map[string]*GraphNode
}

func GetNewGraphNodePool() *GraphNodePool {
	npl := new(GraphNodePool)
	npl.nodes = make(map[string]*GraphNode)

	return npl
}

func (npl *GraphNodePool) addNode(node *GraphNode) {
	_, ok := npl.nodes[node.Name]
	if ok {
		return
	}

	npl.nodes[node.Name] = node
}

func (npl *GraphNodePool) Exists(node *GraphNode) bool {
	_, ok := npl.nodes[node.Name]
	return ok
}

func (npl *GraphNodePool) Get(name string) *GraphNode {
	node, ok := npl.nodes[name]
	if !ok {
		node = new(GraphNode)
		node.Name = name
		npl.nodes[name] = node
	}
	return node
}

func (npl *GraphNodePool) DetectAnyCycle() bool {
	var checked_nodes map[*GraphNode]bool
	done_checking := make(map[*GraphNode]bool)
	for _, node := range npl.nodes {
		_, ok := done_checking[node]
		if ok {
			continue
		}
		checked_nodes = make(map[*GraphNode]bool)
		if node.DetectAnyCycle(checked_nodes, done_checking) {
			return true
		}
		done_checking[node] = true
	}

	return false
}

func (thisnode *GraphNode) DetectAnyCycle(found_in_path map[*GraphNode]bool,
	already_checked map[*GraphNode]bool) bool {
	_, ok := found_in_path[thisnode]
	already_checked[thisnode] = true
	if ok {
		fmt.Printf("Detected a cycle at node %v\n", thisnode.Name)
		return true
	}
	found_in_path[thisnode] = true
	found_in_path_copy := make(map[*GraphNode]bool)
	for k, _ := range found_in_path {
		found_in_path_copy[k] = true
	}
	for _, node := range thisnode.outnodes {
		if node.DetectAnyCycle(found_in_path_copy, already_checked) {
			return true
		}
		already_checked[node] = true
	}
	return false
}

func (node *GraphNode) isinInNodes(inn *GraphNode) bool {
	for _, nd := range node.innodes {
		if nd == inn {
			return true
		}
	}
	return false
}

func (node *GraphNode) isinOutNodes(outn *GraphNode) bool {
	for _, nd := range node.outnodes {
		if nd == outn {
			return true
		}
	}
	return false
}

func (node *GraphNode) AddOutNode(out *GraphNode) {
	if node.isinOutNodes(out) {
		return
	}
	if node.isinInNodes(out) {
		fmt.Printf("A cycle may be there")
		panic("Exiting")
	}
	node.outnodes = append(node.outnodes, out)
	out.AddInNode(node)
}

func (node *GraphNode) AddInNode(in *GraphNode) {
	if node.isinInNodes(in) {
		return
	}
	if node.isinOutNodes(in) {
		fmt.Printf("A cycle may be there")
		panic("Exiting")
	}
	node.innodes = append(node.innodes, in)
	in.AddOutNode(node)
}

func (node *GraphNode) String() string {
	var out string
	out = "[[[" + node.Name
	outs := ", Out Nodes: "
	for _, o := range node.outnodes {
		outs += o.Name
		outs += " "
	}
	ins := ", In nodes: "
	for _, i := range node.innodes {
		ins += i.Name
		ins += " "
	}

	return out + outs + ins + "]]]"
}
