#! /usr/bin/env python3
# -*- coding: utf-8 -*-



def map_in_order(nodes, edges):
    '''
        Rebuilds a graph with successive nodes' ids.
        _nodes: a dict of int
        _edges: a list of ((int, int), weight) pairs
    '''
    # rebuild graph with successive identifiers
    nodes = list(nodes.keys())
    nodes.sort()
    i = 0
    nodes_ = []
    d = {}
    map_reverse = {}
    for n in nodes:
        nodes_.append(i)
        d[n] = i
        map_reverse[i] = n
        i += 1
    edges_ = []
    for e in edges:
        edges_.append((d[e[0]], d[e[1]]))
    return (nodes_, edges_, map_reverse)

class MergeSet:
    @classmethod
    def from_line(cls, _path):
        f = open(_path, 'r')
        lines =  f.readlines()
        f.close()
        nodes = {}          # hash & map?
        edges = []
        for line in lines:
            n = line.split()
            if not n:
                break
            i = int(n[0])
            j = int(n[1])
            nodes[i] = 1
            nodes[j] = 1
            edges.append((i,j))  # ((id1, id2),weight)


        # rebuild graph with successive identifiers
        nodes_, edges_, map_reverse = map_in_order(nodes, edges)

        print("%d nodes, %d edges" % (len(nodes_), len(edges_)))
        return cls(nodes_, edges_, map_reverse)

    @classmethod
    def from_list(cls, es):
        nodes = {}  # hash & map?
        edges = []
        for e in es:
            i = int(e[0])
            j = int(e[1])
            nodes[i] = 1
            nodes[j] = 1
            edges.append((i,j))  # ((id1, id2),weight)

        # rebuild graph with successive identifiers
        nodes_, edges_, map_reverse = map_in_order(nodes, edges)

        print("%d nodes, %d edges" % (len(nodes_), len(edges_)))
        return cls(nodes_, edges_, map_reverse)

    def __init__(self, nodes, edges, map_reverse):
        self.f = {}
        self.nodes = nodes
        self.edges = edges
        self.map_reverse = map_reverse
        self.community = {}
        for i in nodes:
            self.f[i] = i

    def find(self, x):
        if self.f[x] != x:
            self.f[x] = self.find(self.f[x])
        return self.f[x]

    def Merge(self):
        for e in self.edges:
            u = e[0]
            v = e[1]
            if self.find(u) == self.find(v):
                continue
            self.f[v] = self.find(u)

        # relabel.
        label = {}
        i = 1
        for key,val in self.f.items():
            if val not in label:
                label[val] = i
                i+=1
            self.community[str(self.map_reverse[key])] = label[val]


        return self.community


