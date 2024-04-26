import networkx as nx
import matplotlib.pyplot as plt


# Class to represent a graph
class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def create_graph_from_file(self,file_path):
        # Create a directed graph
        self.graph = nx.DiGraph()

        # Read edges from the file and add them to the graph
        with open(file_path, 'r') as file:
            for line in file:
                edge = line.strip().split()
                if len(edge) == 2:
                    source, target = map(str, edge)
                    self.graph.add_edge(source, target)

        return self.graph

    def visualize_graph(graph):
        # Draw the graph using matplotlib
        pos = nx.spring_layout(graph)  # You can choose a different layout if needed
        nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='purple', arrowsize=15)

        # Show the plot
        plt.show()

    def __str__(self):
        return f"Nodes: {self.nodes}\nedges: {self.edges()}"
    
    def find_isolated_nodes(self):
        isolated = [node for node, neighbors in self.graph.adjacency() if not neighbors]
        return isolated
    
    def find_num_of_components(self):
        return nx.number_connected_components(self.graph)
    
    def find_components(self):
        return nx.connected_components(self.graph)
    
    def node_degree(self, node):
        return nx.degree(self.graph, node)
    
    def degree_sequence(self):
        return sorted([d for n, d in self.graph.degree()], reverse=True)
    
    def find_all_paths(self, start, end):
        try:
            return nx.all_simple_paths(self.graph, start, end)
        except nx.NodeNotFound:
            return f"Node not found"

    
    def find_path(self, start, end):
        return nx.shortest_path(self.graph, start, end)


# Specify the path to your file
file_path = '/home/ioanna/Desktop/Mobile-Pervasive-Computing/Project/Net_1_15n_50r_6_6d.txt'  
# Replace with the actual file path

# Create a graph from the file
graph = Graph.create_graph_from_file(Graph,file_path)

# Visualize the graph

Graph.visualize_graph(graph)


