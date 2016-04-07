#!/usr/bin/python

from copy import copy

class GraphNode(object):
    def __init__(self, x):
        self.__in_nodes = None
        self.__out_nodes = None
        self.__value = x

    def get_value(self):
        return self.__value

    def add_in_nodes(self, node):
        if self.__in_nodes is None:
            self.__in_nodes = set()
        if node in self.__in_nodes:
            return
        self.__in_nodes.add(node)
        node.add_out_nodes(self)

    def get_out_nodes(self):
        return self.__out_nodes

    def add_out_nodes(self, node):
        if self.__out_nodes is None:
            self.__out_nodes = set()
        if node in self.__out_nodes:
            return
        self.__out_nodes.add(node)
        node.add_in_nodes(self)


class NodePool(object):
    def __init__(self):
        self.__nodes  = {}
 
    def get_node(self, val):
        if val not in self.__nodes:
            self.__nodes[val] = GraphNode(val)
        return self.__nodes[val]
    
    def get_keys(self):
        return self.__nodes.keys()

np = NodePool()

one = np.get_node(1)
two = np.get_node(2)
three = np.get_node(3)
four = np.get_node(4)
five = np.get_node(5)

one.add_out_nodes(two)
two.add_out_nodes(three)
three.add_out_nodes(four)
four.add_out_nodes(five)
five.add_out_nodes(one)

def detect_cycle(visited_set, cur_node):
    if cur_node in visited_set:
        return True
    out_nodes = cur_node.get_out_nodes()
    if not out_nodes:
        return False
    copy_set = copy(visited_set)
    copy_set.add(cur_node)
    for node in out_nodes:
        if detect_cycle(copy_set, node):
            return True

for k in np.get_keys():
    node = np.get_node(k)
    visited = set()
    if detect_cycle(visited, node):
        print "Cycle detected"
        break
