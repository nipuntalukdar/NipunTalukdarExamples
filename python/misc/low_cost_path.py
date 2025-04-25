''' There are n cities connected by some number of flights. You are given an array flights where
flights[i] = [fromi, toi, pricei] indicates that there is a flight from city fromi to city toi with
cost pricei.

You are also given three integers src, dst, and k, return the cheapest price from src to dst with at
most k stops. If there is no such route, return -1.

'''


def from_graph(nodes):
    graph = {}
    for node in nodes:
        if node[0] in graph:
            graph[node[0]].add((node[1], node[2]))
        else:
            graph[node[0]] = {(node[1], node[2])}
    return graph

def low_cost(visited, costs, graph, src, dst, k):
    if k < 0:
        return
    dsts = [node for node in graph[src]]
    for d in dsts:
        if d in visited:
            continue
        if d[0] == dst:
            cost = d[1] + sum([a[1] for a in visited])
            costs.append(cost)
            continue
        visited.add(d)
        low_cost(visited, costs, graph, d[0], dst, k - 1)
        visited.remove(d)
        

def find_low_cost(graph, src, dst, k):
    costs = []
    if src not in graph:
        costs.append(-1)
    if src == dst:
        costs.append(0)
    low_cost(set(), costs, graph, src, dst, k)
    return min(costs)
    
paths = [[0,1,100],[1,2,100],[0,2,500]]
src = 0
dst = 2
k = 0
graph = from_graph(paths)
print(find_low_cost(graph, src, dst, k))

paths = [[0,1,100],[1,2,100],[0,2,500]]
src = 0
dst = 2
k = 1
graph = from_graph(paths)
print(find_low_cost(graph, src, dst, k))






