"""
Fiddling with graphs.

@author: Elias Gabriel
"""
import networkx as nx
import numpy as np
import queue
from itertools import combinations
import matplotlib.pyplot as plt

def bfs(G, start):
    """ A simple breadth-first search algorithm implemented using native queues. """
    seen = set()
    q = queue.Queue()
    # we don't care about threading so don't ask Queue to block execution
    q.put_nowait(start)

    while not q.empty():
        # get the waiting node, again without blocking execution
        u = q.get_nowait()

        if u not in seen:
            seen.add(u)
            # get all of u's neighbors and enqueue them
            for n in G[u]: q.put_nowait(n)

    return seen

def num_components(G):
    """
    Counts the number of components in the provided graph via BFS on each node and tracking
    all the nodes that have been previously seen. The number of components is equal to the 
    number of BFSs that must be made to find every known node.
    """
    num = 0
    seen = set()

    # for every node in G
    for v in G:
        # if we haven't seen it
        if v not in seen:
            # increase the number of components and add all the nodes to which there is a path
            # to the list of already-seen nodes
            num += 1
            seen.update(bfs(G, v))

    return num

def rand_bigraph(n, p):
    """ Generate a random binomial graph with `n` nodes and with edges of probability `p`. """
    G = nx.Graph()
    # loop through all the possible edges and add them if we generate True with chance p
    E = [e for e in combinations(range(n), 2) if np.random.random() < p]
    G.add_edges_from(E)
    return G



if __name__ == "__main__":
    ## Problem 2:
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)
    G.add_edge(2, 5)
    G.add_edge(3, 6)
    G.add_edge(4, 7)
    G.add_edge(5, 6)
    G.add_edge(5, 8)
    G.add_edge(6, 8)
    G.add_edge(7, 8)
    G.add_edge(9, 10)
    print("Number of components:", num_components(G))
    
    ## Problem 3:
    xs = range(5, 251)
    ys = []
    
    for n in xs:
        for p in np.linspace(0, 1, 100):
            flag = 0

            for _ in range(10):
                G = rand_bigraph(n, p)
                if num_components(G) == 1: flag += 1
            
            if flag == 10:
                ys.append(p)
                break

    plt.plot(xs, ys)
    plt.title("Probability for Connectedness vs. Graph Size")
    plt.xlabel("number of nodes")
    plt.ylabel("probability")
    plt.show()
