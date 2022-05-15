from heapq import heappush, heappop
from itertools import count
from typing import Dict, Tuple
import networkx as nx
from finder_app.path_algos.models import NoRouteException
from networkx.algorithms.shortest_paths.weighted import _weight_function

__all__ = ["path_length", "astar_path", "greedy", "BFS"]

def path_length(g, path, mode="driving_cost"):
    
    cost = _weight_function(g, mode)
    
    accumulated_cost = 0
    
    step_lengths = []
    
    prvs_node = path[0]
    for node in path[1:]:
        
        step_lengths.append(cost(prvs_node, node, g[prvs_node][node]))
        
        accumulated_cost += step_lengths[-1]
        prvs_node = node
    
    return accumulated_cost, step_lengths
    
def astar_path(g, source, destination, heuristic=None, mode="driving_cost"):
    
    
    # in case no heuristic is passed to the function it will act as UCS(Weighted BFS)
    if heuristic is None:

        def heuristic(u, v):
            return 0

    # replace push and pop with heap pop and push, so we can use a priority queue
    push = heappush
    pop = heappop
    
    # so we can use driving or walking distance
    cost = _weight_function(g, mode)
    
    # use iterator to count
    c = count()
    
    # priority queue containing tuples in the format:
    #        [priority, iteration,   node, cost from src, parent node]
    fringe = [(   0   , next(c)  , source,             0, None)]
    
    # dict holding both the heuristic value and the lowest found cost to reach the node, with key being node name
    enqueued: Dict[str, Tuple[float, float]] = {}
    
    # dict holding the parent of explored nodes, with key being node name
    explored = {}

    while fringe:
        _, __, current_node, dist, parent = pop(fringe)

        if current_node == destination:
            path = [current_node]
            node = parent
            while node is not None:
                # go from parent to parent until we reach the starting node
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if current_node in explored:
            # this condition means that the node is the src node
            if explored[current_node] is None:
                continue
            # get the heuristic and reach cost of the node
            qcost, h = enqueued[current_node]
            if qcost < dist:
                continue

        # save the parent of the current node
        explored[current_node] = parent

        for child, w in g[current_node].items():
            # get the accumelated cost to reach the child node from the source
            ncost = dist + cost(current_node, child, w)
            if child in enqueued:
                # if we already know the heuristic and a shorter path we can get it from the enqueued queue
                qcost, h = enqueued[child]
                if qcost <= ncost:
                    continue
            else:
                # calculate heuristic
                h = heuristic(child, destination)
            # write new heuristic value or the shorter path to reach this node
            enqueued[child] = ncost, h
            # push the produced values into the priority queue
            # [priority, iteration, node, cost to reach from src, parent node]
            push(fringe, (ncost + h, next(c), child, ncost, current_node))

    raise NoRouteException()


def greedy(G, source, destination, heuristic=None):
    
    # replace push and pop with heap pop and push, so we can use a priority queue
    push = heappush
    pop = heappop
    # use iterator to count
    c = count()
    fringe = [(0, next(c), source, None)]
    
    # dict holding heuristic and lowest cost to reach from src, with key being node name
    enqueued = {}
    
    # dict holding the parent of explored nodes, with key being node name
    explored = {}

    while fringe:
        _, __, current_node, parent = pop(fringe)

        if current_node == destination:
            path = [current_node]
            node = parent
            while node is not None:
                # go from parent to parent until we reach the starting node
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if current_node in explored:
            # this condition means that the node is the src node
            if explored[current_node] is None:
                continue
            # get the heuristic and cost reach of the node
            h = enqueued[current_node]

        # get the parent of the current node
        explored[current_node] = parent
        for child, w in G[current_node].items():
            if child in enqueued:
                
                # if the heuristic was already calculated read it from the enqueued queue
                h = enqueued[child]
            else:
                # else calculate heuristic
                h = heuristic(child, destination)

            # save the new heuristic value or the shorter path to reach this node
            enqueued[child] = h
            # push the produced values into the priority queue
            # [priority, iteration, node, cost to reach from src, parent node]
            push(fringe, (h, next(c), child, current_node))

    raise NoRouteException()


def BFS(G, source, destination):
    
    # replace push and pop with heap pop and push, so we can use a priority queue
    pop = heappop
    push = heappush
    
    # use iterator to count
    c = count()
    fringe = [(next(c), source, None)]
    
    # dict holding the parent of explored nodes, with key being node name
    explored = {}

    while fringe:
        __, current_node, parent = pop(fringe)

        if current_node == destination:
            path = [current_node]
            node = parent
            while node is not None:
                # go from parent to parent until we reach the starting node
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if current_node in explored:
            # this condition means that the node is the src node
            if explored[current_node] is None:
                continue
        # get the parent of the current node
        explored[current_node] = parent

        for child, w in G[current_node].items():
            # write new shorter path to reach this node
            # push the produced values into the priority queue
            # [iteration, node, parent node]
            push(fringe, (next(c), child, current_node))

    raise NoRouteException()

def zero():
    ''' returns always zero, used as heuristic for a star to be uniform cost '''
    return 0

def UCS(G, source, destination, mode="driving_cost"):
    
    return astar_path( g=G, source=source, destination=destination, heuristic=zero, mode=mode )