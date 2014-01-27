from collections import deque
graph = { 'a' :  [ 'b' , 'c' , 'd' , 'e', 'f' ],
          'b' :  [ 'x' , 'y', 'z' , 'c' , 'd' , 'e' ],
          'c' :  [ 'x' , 'd' , 'l' ],
          'd' :  [ 'l' , 'm' ],
          'l' : ['p'],
          'x' : [],
          'y' : [],
          'z' : [],
          'p' : [],
          'm' : [],
          'e' : [],
          'f' : []

        }

def shortest_path(graph, start, end, path = []):
    if not graph.has_key(start):
        return None
    if start == end : 
        return path
    path.append(start)
    paths=deque([])
    paths.append(path)
    curpath = paths.popleft()
    while not curpath is None:
        for node in graph[curpath[len(curpath) -1]]:
            if node == end:
                curpath.append(node)
                return curpath
            if node not in curpath:
                newpath = curpath[:]
                newpath.append(node)
                paths.append(newpath)
        curpath = paths.popleft()    
    return None

# Example run below
x = shortest_path(graph, 'a' , 'p' , [])
print x

