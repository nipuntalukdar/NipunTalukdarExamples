from random import randint
import unittest


class Node(object):
    def __init__(self, val):
        self.__val__ = val
        self.__thread__ = None
        self.__left__ = None
        self.__right__ = None

    @property
    def val(self):
        return self.__val__
    
    @val.setter
    def val(self, val):
        self.__val__ = val

    @property
    def thread(self):
        return self.__thread__

    @thread.setter
    def thread(self, thr):
        self.__thread__ = thr

    @property
    def right(self):
        return self.__right__
    
    @right.setter
    def right(self, right):
        self.__right__ = right

    @property
    def left(self):
        return self.__left__
    
    @left.setter
    def left(self, left):
        self.__left__ = left
    '''
    def __repr__(self):
        print '[val={} left={} right={} thread={}]'.format(self.__val__,
            self.__left__, self.__right__, self.__thread__)
    '''


class RThreaded(object):
    
    def __init__(self):
        self.__root__ = None

    def add(self, node):
        if not self.__root__:
            self.__root__ = node
        else:
            start = self.__root__
            while True:
                if start == start.val:
                    break
                if start.val < node.val:
                    if not start.right:
                        start.right = node
                        if start.thread:
                            node.thread = start.thread
                            start.thread = None
                        break
                    else:
                        start = start.right
                else:
                    if not start.left:
                        start.left = node
                        node.thread = start
                        break
                    else:
                        start = start.left
    
    def traverse(self):
        start = self.__root__
        while start:
            if start.left:
                start = start.left
            else:
                # No left node
                print start.val
                # Now print the nodes pointed by the thread
                while start.thread:
                    start = start.thread
                    print start.val
                    #Now move to the right node
                start = start.right

    def count(self):
        start = self.__root__
        count = 0
        while start:
            if start.left:
                start = start.left
            else:
                # No left node
                count += 1 
                # Now print the nodes pointed by the thread
                while start.thread:
                    start = start.thread
                    count += 1
                    #Now move to the right node
                start = start.right
        return count

    def smallest(self):
        if not self.__root__:
            raise("Empty tree")
        start = self.__root__
        while start.left:
            start = start.left
        return start.val

    def biggest(self):
        if not self.__root__:
            raise("Empty tree")
        start = self.__root__
        while start.right:
            start = start.right
        return start.val

class TestMe(unittest.TestCase):
    def setUp(self):
        self.__tree__ = RThreaded()

    def test_print(self):
        self.__tree__.add(Node(100))
        self.__tree__.add(Node(2))
        self.__tree__.add(Node(3))
        self.__tree__.add(Node(50))
        self.__tree__.add(Node(699))
        self.__tree__.add(Node(99))
        self.__tree__.add(Node(1000))
        self.__tree__.traverse()
        self.assertEqual(self.__tree__.count(), 7)
        self.assertEqual(self.__tree__.smallest(), 2)
        self.assertEqual(self.__tree__.biggest(), 1000)

if __name__ == '__main__':
    unittest.main()
