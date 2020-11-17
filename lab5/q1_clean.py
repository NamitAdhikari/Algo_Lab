import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

class GraphAnalyze():

    def readCsvToEdgelist(self, url, header_list=["a", "b"]):
        E = pd.read_csv(url, sep=" ", header=None, names=header_list)
        G = nx.from_pandas_edgelist(E, "a", "b", ["w"])
        return G

    def findNodeEdge(self, G, nFlag = False, eFlag = False):
        nodes = nx.nodes(G)
        edges = nx.edges(G)

        if nFlag:
            return nodes
        elif eFlag:
            return edges
        else:
            return nodes, edges

    def findAvgDegree(self, G):
        totDeg = 0
        degree = G.degree()
        l = len(degree)

        for x in degree:
            totDeg += x[1]

        return (totDeg / l)

    def findDensity(self, n, e):
        density = (2 * e) / (n * (n - 1))
        return density

    def findDiameter(self, G):
        pass
        # nodes = nx.nodes(G)
        # pairs = [(nodes[i], nodes[j]) for i in range(len(nodes)) for j in range (i+1, len(nodes)-1)]
        # smallest_paths = []
        #
        # for (s, e) in pairs:
        #     paths = []
        #
        #
        #     smallest = sorted(paths, key=len)
        #     smallest_paths.append(smallest)
        #
        # smallest_paths.sort(key=len)
        # diameter = len(smallest_paths[-1])
        # return diameter


    def findAvgClusteringCoeff(self, nodes, edges):
        clusterCoeff = {}
        neighbours = []

        for x in nodes:
            neighbours.clear()
            for y in edges:
                if x == y[0]:
                    neighbours.append(y[1])
                if x == y[1]:
                    neighbours.append(y[0])

            num = len(neighbours)

            N = G.subgraph(neighbours)
            ei = len(self.findNodeEdge(N, eFlag=1))

            if num == 0 or num == 1:
                clusterCoeff.update({x: 0})
            else:
                clusterCoeff.update({x: (2*ei)/(num*(num-1)) })

        totCluster = 0
        for x in clusterCoeff:
            totCluster += clusterCoeff[x]

        avgClusterCoeff = totCluster / len(nodes)
        return avgClusterCoeff

    def printEverything(self, G):
        nodes, edges = self.findNodeEdge(G)
        n, e = len(nodes), len(edges)
        print(f"Number of nodes in graph : {n}")
        print(f"Number of edges in graph : {e}")

        print(f"Average Degree of graph : {self.findAvgDegree(G)}")

        print(f"Density of graph : {self.findDensity(n, e)}")

        print(f"Diameter of graph : {nx.diameter(G)}")

        print(f"Average Clustering of graph : {self.findAvgClusteringCoeff(nodes, edges)}")


if __name__ == "__main__":

    graph = GraphAnalyze()
    G = graph.readCsvToEdgelist('data/aves-sparrowlyon-flock-season2.edges', ["a", "b", "w"])
    graph.printEverything(G)
