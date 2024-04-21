import random
import matplotlib.pyplot as plt
import networkx as nx
import time

executions = []
attempts = []


class Graph(object):
    def __init__(self, num_vertices):
        self.V = num_vertices
        self.graph = []
        self.adj_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])
        self.adj_matrix[u][v] = w
        self.adj_matrix[v][u] = w

    def find(self, root, i):
        if root[i] == i:
            return i
        return self.find(root, root[i])

    def union(self, root, rank, x, y):
        xroot = self.find(root, x)
        yroot = self.find(root, y)
        if rank[xroot] < rank[yroot]:
            root[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            root[yroot] = xroot
        else:
            root[yroot] = xroot
            rank[xroot] += 1

    def kruskals(self):
        start_time = time.time()
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        root = []
        rank = []
        for node in range(self.V):
            root.append(node)
            rank.append(0)

        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(root, u)
            y = self.find(root, v)
            if x != y:
                e = e + 1
                result.append((u, v, w))
                self.union(root, rank, x, y)

        G = nx.Graph()
        G.add_nodes_from(range(self.V))
        for u, v, w in result:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, edge_color='b')
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): w for u, v, w in result})
        end_time = time.time()
        execution_time = end_time - start_time
        executions.append(execution_time)
        print(f"Execution time: {execution_time:.4f} seconds")
        plt.show()


def setup(vertices, input_density):
    g = Graph(vertices)
    for i in range(g.V):
        for j in range(g.V):
            if i != j:
                g.add_edge(i, j, 0)
    random.shuffle(g.graph)
    density = int(g.V * (g.V - 1) * input_density)
    g.graph = g.graph[:density]
    for edge in g.graph:
        weight = random.randint(1, g.V)
        vertex_one = edge[0]
        vertex_two = edge[1]
        g.adj_matrix[vertex_one][vertex_two] = weight
        edge[2] = weight
    g.kruskals()


for experiment in range(10):
    for attempt in range(20):
        setup(20 + 10 * experiment, 0.35 + 0.05 * experiment)
    attempts.append(sum(executions) / 20)
    executions = []
    print(f"Experiment #{experiment} execution time: {attempts[experiment]:.4f} seconds")
