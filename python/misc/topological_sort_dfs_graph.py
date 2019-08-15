'''
Topological sort with DFS:

Start with any node in graph and add it to the head of a list L, if the node
is not in L already
    do a DFS on the node's children (denoted by nodech)
        if nodech has children
            if some children are already in L, add nodech before \
                the children with lowest index in the L
            else
                add the nodech to the tail of L
        if some children of nodech are not already on the L
            do DFS on each of them

Finally L will contain the topologically sorted list  of nodes
'''

import unittest

class Graph(object):
    def __init__(self):
        self.__nodes__ = set()

    def add_node(self, node):
        self.__nodes__.add(node)

    def iter(self):
        return iter(self.__nodes__)


class Node(object):
    def __init__(self, identifier):
        self.__out_going__ = set()
        self.__in_coming__ = set()
        self.__identifier__ = identifier

    def add_incoming(self, node):
        if self.__identifier__ == node.__identifier__:
            return
        self.__in_coming__.add(node)
        node.__out_going__.add(self)
    
    def add_outgoing(self, node):
        if self.__identifier__ == node.__identifier__:
            return
        self.__out_going__.add(node)
        node.__in_coming__.add(self)

    def iterout(self):
        return iter(self.__out_going__)

    def iterin(self):
        return iter(self.__in_coming__)

    @property
    def value(self):
        return self.__identifier__

    def __str__(self):
        outgoing = ','.join([str(x.__identifier__) for x  in self.__out_going__])
        incoming = ','.join([str(x.__identifier__) for x  in self.__in_coming__])
        return 'id={}, incoming={}, outgoing={}'.format(self.__identifier__,
            incoming, outgoing)

def startdfs(node, visited, L):
    itero = node.iterout()
    try:
        while True:
            nodeo = itero.next()
            dfs(nodeo, visited, L)
    except StopIteration:
        pass

def dfs(node, visited, L):
    if node in visited:
        return
    visited.add(node)
    already_seen = []
    not_seen = []
    try:
        itero = node.iterout()
        while True:
            nodeo = itero.next()
            if nodeo in visited:
                already_seen.append(nodeo)
            else:
                not_seen.append(nodeo)
    except StopIteration:
        pass
    if already_seen:
        # Some of the children were already added, 
        # Ensure this node inserted before all of its children index
        where_to_insert = min([L.index(a) for a in already_seen])
        L.insert(where_to_insert, node)
    else:
        L.append(node)
    for not_seen_node in not_seen:
        dfs(not_seen_node, visited, L)
    
def topological_sort_dfs(graph):
    L = []
    itern = graph.iter()
    visited = set()
    try:
        while True:
            node = itern.next()
            if node not in visited:
                visited.add(node)
                L.insert(0,node)
                startdfs(node, visited, L)
    except StopIteration:
        pass
    return L


class MyTest(unittest.TestCase):
    def test_one(self):
        nodes = []
        i = 0
        while i < 10:
            nodes.append(Node(i))
            i += 1
        nodes[0].add_outgoing(nodes[1])
        nodes[0].add_outgoing(nodes[2])
        nodes[0].add_outgoing(nodes[9])
        nodes[1].add_outgoing(nodes[3])
        nodes[1].add_outgoing(nodes[4])
        nodes[1].add_outgoing(nodes[5])
        nodes[6].add_outgoing(nodes[7])
        nodes[6].add_outgoing(nodes[9])
        nodes[7].add_outgoing(nodes[8])
        nodes[7].add_outgoing(nodes[9])
        nodes[8].add_outgoing(nodes[9])
        gr = Graph()
        for node in nodes:
            gr.add_node(node)
        L = [x for x in topological_sort_dfs(gr)]
        self.assertTrue(L.index(nodes[0]) < L.index(nodes[1]))
        self.assertTrue(L.index(nodes[0]) < L.index(nodes[2]))
        self.assertTrue(L.index(nodes[0]) < L.index(nodes[9]))
        self.assertTrue(L.index(nodes[7]) < L.index(nodes[8]))
        self.assertTrue(L.index(nodes[8]) < L.index(nodes[9]))
        i = 0
        nodes = []
        while i < 3:
            nodes.append(Node(i))
            i += 1
        nodes[0].add_outgoing(nodes[1])
        nodes[1].add_outgoing(nodes[2])
        gr = Graph()
        for node in nodes:
            gr.add_node(node)
        L = [x for x in topological_sort_dfs(gr)]
        self.assertTrue(L.index(nodes[0]) < L.index(nodes[1]))
        self.assertTrue(L.index(nodes[1]) < L.index(nodes[2]))


if __name__ == '__main__':
    unittest.main()
