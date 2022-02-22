# Christina LaPane Student ID: 008207171
import csv


# Takes data from 'distance.csv'
# Vertices are created based off name of location ('Western Goverenors University')
# graphs data using undirected edges.
# edge has a weight, which is the mileage between the two vertices

# Create distance graph pseudocode
# delivery_dictionary ={} initialize
# edge_weights ={} initialize

# add_vertex(vertex):
#   creates a dictionary with the street address as teh key
#   delivery_dictionary[vertex] = []

# add_edge(v1, v2, weight = 1.0):
#   adds an undirected edge between vertices. Weight = mileage between two locations
#   creates a dictionary where key : value == vertices : miles
#   edge_weights[v1, v2] = weight

# load_packages(table):
#   associates each package with its corresponding vertext on the graph
#   for bucket in table:
#       for item in bucket:
#            delivery_dictionary[item[1]].append(item)

class Graph:

    # Constructor creating empty lists for the locations and edge weights
    def __init__(self):
        self.delivery_dict = {}  # has the same function of an adjacency list
        self.edge_weights = {}

    # Adds a vertex to the graph
    def add_vertex(self, vertex):
        self.delivery_dict[vertex] = []  # creates a dictionary with the street address as the key

    # Adds an undirected edge between vertices. Weight is equivalent to miles
    def add_edge(self, v1, v2, weight=1.0):
        self.edge_weights[(v1, v2)] = weight  # creates a dict where key : value == vertices : miles

    # Associates each package with its corresponding vertex on the graph
    # O(N^2)
    def load_packages(self, ht):
        for bucket in ht.table:
            for item in bucket:
                self.delivery_dict[item[1]].append(item)


# Reads the entire 'distance.csv'
# This is needed in order to create edges between v1 and v2
# O(N)
def read_distance_csv(filename):
    csv_data = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)
        for row in csv_reader:
            csv_data.append(row)
    return csv_data


# This function creates the graph
# O(N^2)
def get_graph(filename):
    data = read_distance_csv(filename)
    graph_distances = Graph()
    for row in data:
        graph_distances.add_vertex(row[1])  # Vertex is associated with the street address
    for row in data:
        for i in range(3, len(row)):  # Starts at 3 because indices 0-2 are name, street, and zip, which are not needed
            graph_distances.add_edge(row[1], data[i - 3][1],
                                     float(row[i]))  # data[i-3][1] gets each connected street vertex
    return graph_distances


# Initialize the graph for further use
graph = get_graph('distance.csv')

# pseudocode
