import networkx as nx
from graph import Graph
import random

class Algorithm:
    @staticmethod
    def find_N(graph, C):
        N_c = {}
        for vertex1 in graph.nodes:
            all_paths = Algorithm.find_all_paths(graph, vertex1, C)
            temp = []
            for path in all_paths:
                if len(path) == 2:
                    temp.append(path[1])
            N_c[vertex1] = temp
        return N_c

    @staticmethod
    def find_all_paths(graph, start, end):
        try:
            return nx.all_simple_paths(graph, start, end)
        except nx.NodeNotFound:
            return []

    @staticmethod
    def v_sub_c(graph, C):
        return [vertex for vertex in graph.nodes if vertex not in C]

    @staticmethod
    def V_i(graph, C, m):
        V_sub_C = Algorithm.v_sub_c(graph, C)
        V_i = {str(i): [] for i in range(m)}
        N = Algorithm.find_N(graph, C)

        for vertex in V_sub_C:
            if len(N[vertex]) > m - 1:
                continue
            V_i[str(len(N[vertex]))].append(vertex)

        return V_i

    @staticmethod
    def V_m(graph, C, m):
        V_sub_C = Algorithm.v_sub_c(graph, C)
        V_m = [vertex for vertex in V_sub_C if len(Algorithm.find_N(graph, C)[vertex]) >= m]
        return V_m

    @staticmethod
    def m(graph, C, m):
        m_c = {}
        vi = Algorithm.V_i(graph, C, m)
        vm = Algorithm.V_m(graph, C, m)

        for vertex in graph.nodes:
            for el in vi:
                if int(el) > 0 and (vertex in vi[el]):
                    m_c[vertex] = m - int(el)

            if (vertex in C) or (vertex in vm):
                m_c[vertex] = 0
            if vertex in vi[str(0)]:
                m_c[vertex] = m - 1

        return m_c

    @staticmethod
    def sum_m_C(graph, m, m_c):
        return sum(m_c.values())

    @staticmethod
    def black_nodes(graph, C):
        return [vertex for vertex in graph.nodes if vertex in C]

    @staticmethod
    def gray_nodes(graph, C, m):
        return Algorithm.V_m(graph, C, m)

    @staticmethod
    def red_nodes(graph, C, m):
        vi = Algorithm.V_i(graph, C, m)
        return [vertex for i in range(1, m) for vertex in vi[str(i)]]

    @staticmethod
    def white_nodes(graph, C, m):
        vi = Algorithm.V_i(graph, C, m)
        return vi[str(0)]

    @staticmethod
    def spanning_subgraph(graph, C):
        spanning_sub = {}

        for vertex in graph.nodes:
            spanning_sub[vertex] = []

            if vertex in C:
                spanning_sub[vertex] = []
                spanning_sub[vertex] = graph.neighbors(vertex)
                continue

            flag = 1
            for neighbour in graph.neighbors(vertex):
                if (neighbour in C) and (flag == 1):
                    spanning_sub[vertex] = []
                    flag = 0

                if neighbour in C:
                    spanning_sub[vertex].append(neighbour)

        return spanning_sub

    @staticmethod
    def G_C(graph, C):
        subgraph = {}

        for vertex in graph.nodes:
            subgraph[vertex] = []
            if vertex in C:
                subgraph[vertex] = []
                for neighbour in graph.neighbors(vertex):
                    if neighbour in C:
                        subgraph[vertex].append(neighbour)

        return subgraph

    @staticmethod
    def f_C(graph, C, m):
        return (
            nx.number_connected_components(Algorithm.G_C(graph, C)) +
            nx.number_connected_components(Algorithm.spanning_subgraph(graph, C)) +
            Algorithm.sum_m_C(graph, m, Algorithm.m(graph, C, m))
        )

    @staticmethod
    def delta_x_f_C(graph, C, m, x):
        return Algorithm.f_C(graph, C + [x], m) - Algorithm.f_C(graph, C, m)

if __name__ == "__main__":
    # Specify the path to your file
    file_path = '/home/ioanna/Desktop/Mobile-Pervasive-Computing/Project/Net_1_15n_50r_6_6d.txt'
    
    # Create a graph from the file
    graph = Graph()
    graph.create_graph_from_file(file_path)

    # Ensure that the graph has nodes
    if not graph.graph.nodes:
        print("The graph has no nodes. Please check your file or graph initialization.")
    else:
        algorithm = Algorithm()

        # Convert the set of nodes to a list before sampling
        nodes_list = list(graph.graph.nodes)
        
        # Ensure that the sample size is not greater than the number of nodes
        sample_size = min(5, len(nodes_list))
        
        C = random.sample(nodes_list, sample_size)

        #Experiment 1
        # m = 2 
        # C = ["b", "e"]

        #Experiment 2 
        # # m = 1
        # # C = ["a","b", "e"]
        
        # m = 2 
        # C = ["b", "e"]

        # m = 2
        # C = ["a","b","c", "e", "f"]

        # Experiment 3
        # m = 1
	    
        # C =["c", "d", "g", "k", "q", "p"]

        # m = 2
        # C = ['a', 'c', 'd', 'g', 'k', 'j', 'm', 'q', 'p', 'r']

        # m = 3
        # C = ['k', 'd', 'j', 'q', 'a', 'e', 'm', 'r', 'c', 'g', 'o', 'b', 'i', 'h', 'l', 'n', 'p', 's', 't']

        for i in range(1, 4):
            m = i
            print(f"Initial set C: {C}")
            
            result = algorithm.find_N(graph.graph, C)
            print(f"Result of find_N: {result}")

            print(f"black_nodes: {algorithm.black_nodes(graph.graph, C)}")

            print(f"gray_nodes: {algorithm.gray_nodes(graph.graph, C, m)}")

            print(f"red_nodes: {algorithm.red_nodes(graph.graph, C, m)}")

            print(f"white_nodes: {algorithm.white_nodes(graph.graph, C, m)}")

        


