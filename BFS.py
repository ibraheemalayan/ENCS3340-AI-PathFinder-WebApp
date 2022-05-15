def BFS(G, source, target):
    
    
    #replace push and pop with heap pop and push, so we can use a priority queue
    push = heappush
    pop = heappop
    #use iterator to count
    c = count()
    fringe = [(next(c), source, 0, None)]
    #dict holding hearistic and lowest cost to reach from src, with key being node name
    enqueued = {}
    #dict holding parent of node, with key being node name
    explored = {}

    while fringe:
        __, curnode, dist, parent = pop(fringe)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
            #go from parent to parent until we reach the starting node
                path.append(node)
                node = explored[node]
            path.reverse()
            return path
        
        if curnode in explored:
            #this condition means that the node is the src node
            if explored[curnode] is None:
                continue
            #get the heauristic and cost reach of the node
            qcost = enqueued[curnode]
            if qcost < dist:
                continue
            
        #get the parent of the current node
        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            #get the accumelated cost to reach the neighbor node from the source
            ncost = dist + 1
            if neighbor in enqueued:
                # if we already know a shorter path we can get it from the enqueued queue
                qcost = enqueued[neighbor]
                if qcost <= ncost:
                    continue
            # write new shortest path to reach this node
            enqueued[neighbor] = ncost
            # push the produced values into the priority queue
            # [priority/iteration, node, cost to reach from src, parent node]
            push(fringe, (next(c), neighbor, ncost, curnode))

    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")