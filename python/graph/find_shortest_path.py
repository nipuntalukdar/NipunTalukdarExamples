graph = { 'a' :  [ 'b' , 'c' , 'd' , 'e', 'f' ],
          'b' :  [ 'x' , 'y', 'z' , 'c' , 'd' , 'e' ],
          'c' :  [ 'x' , 'd' , 'l' ],
          'd' :  [ 'l' , 'm' ],
          'l' : ['p'] 

        }

def shortest_path(graph, start, end, path = [])
    if not graph.has_key(start):
        return None
    if start == end : 
        return path
    path.append(start)
    paths = []
    for node in graph['start']:
        if node == start:
            return path
    
    return None
