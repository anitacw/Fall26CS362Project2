### A graph class for storing the Romania Map.
### We'll use strings to represent each city. Those will
### be the vertices in our graph.
### The edges will be (name, dist) tuples

import re


# We're implementing a graph as an adjacency list.

class Graph :
    def __init__(self):
        ## our adjacency list
        self.g = {}

    def add_node(self, index):
            self.g[index] = []

    def add_edge(self, source, edge):
        self.g[source].append(edge)

    def get_edge(self, src, dest):
        if src in self.g :
            edges = self.g[src]
            for e in edges :
                if e[0] == dest :
                    return e

    def get_edges(self, src):
        if src in self.g:
            return self.g[src]


# use romania.graph as input
def build_graph(infile):

    g = Graph()
    with open(infile) as f:
        for line in f:
            city, edges = line.strip().split(':')
            city = city.strip()
            g.add_node(city)
            edgelist = edges.split(';')
            for edge in edgelist :
                dest, cost = edge.strip(" ()").split(',')
                cost = int(cost)
                g.add_edge(city, (dest, cost))
    return g

if __name__ == "__main__":
    g = build_graph("romania.graph")