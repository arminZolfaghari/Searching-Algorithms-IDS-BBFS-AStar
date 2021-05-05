from collections import defaultdict


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    # for add edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Depth Limited Search
    def DLS(self, src, target, max_depth):
        if src == target:
            return True
        if max_depth <= 0:
            return False
        # Recursive for all the vertices adjacent to this vertex
        for v in self.graph[src]:
            if self.DLS(v, target, max_depth - 1):
                return True
        return False

    # Recursive DLS (Iterative Deepening Search)
    def IDS(self, src, target, max_depth):
        for depth in range(max_depth):
            if self.DLS(src, target, depth):
                return True
        return False


if __name__ == "__main__":

    g = Graph(7)
    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(1, 3)
    g.addEdge(1, 4)
    g.addEdge(2, 5)
    g.addEdge(2, 6)

    target = 6
    maxDepth = 3
    src = 0

    print(g.IDS(src, target, maxDepth))
