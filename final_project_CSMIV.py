'''
Schaefer Wiskur
4/27/25
CSM IV

The first algorithm is used to find the shortest_path for the truck. I am using Dijkstra's algorithm.
Dijkstra's algorithm is used to find the shortest path of a weighted graph between nodes.
The algorithm assigns infinite paths to each node next from the starting node. It uses a queue which sorts the nodes therefore always giving the next smallest cost in the order.
It continues to only update when a shorter path is found. It will continue this process until the shortest path has been found.
It also tracks the order in which they’re visited by backtracking through which nodes have been visited to return the path it took, returning the path the algorithm took.


The second algorithm is used to find the best path from the hub. I am utilizing prim's algorithm.
Prim's algorithm is efficient for finding the best path starting at the hub or the lowest weight.
It grows the minimum spanning tree directly from the starting point which is our hub, by visiting the weighted edges, visiting the lowest first.
The algorithm will keep track of which nodes have been visited. Prims is a greedy algorithm by finding the smallest edge and connecting to an unvisited edge.
It uses a heapq to pop the smallest weight first. This means that it will only visit unvisited nodes and will avoid the visits to prevent a circuit.
For every weight in the program it will track the total cost of the weight to determine and return the total cost for the best path.
It finally returns the mst from popping the minimum data and finding if it was visited or not to find the output.


The last algorithm is used to find network changes in the path. This algorithm is used to change the weights and paths to then find the new path that adjusts to these changes.
For this algorithm I am using Kruskal's algorithm with a union-find method. This algorithm is a data structure which finds the 2 sets and merges them into 1.
The union find method finds the elements in whichever set they're in, and then the union sorts them and merges the 2 sets.  The Union-find method ensures that there are no circuits.
Kruskal's function then finds vertices and pushes them into the edge list and this is then used to pop and find the mst_edges and weight.
Kruskal's looks for the best path and adds to the mst until the circuit is found. This algorithm is helpful as I can update the paths, making it optimal for dynamic network changes.
It makes it easy to rebuild the mst to make quick adjustments in finding the new path with the changes to the edges.



'''


import heapq

#Graph class
class Graph:

    #Function initializes size, adj_matrix and vertex_data
    def __init__(self, size):
        self.size = size
        self.adj_matrix = [[0] * size for i in range(size)]
        self.vertex_data = [''] * size
        
    #Add edge function creates an edge between nodes
    def add_edge(self, v1, v2, weight):
        if 0 <= v1 < self.size and 0 <= v2 < self.size:
            self.adj_matrix[v1][v2] = weight
            self.adj_matrix[v2][v1] = weight
        
    #Function to store node_data
    def add_node_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data
        

    #Method used to find the lowest cost using Dijkstra's algorithm
    def lowest_cost(self, start_vertex_data, end_vertex_data):

        #Start initialized for vertex data
        start = self.vertex_data.index(start_vertex_data)

        #End initialized for vertex data
        end = self.vertex_data.index(end_vertex_data)

        #Sets all of the distances to infinity
        min_distances = [float('inf')] * self.size

        #Sets the initial distances to 0
        min_distances[start] = 0

        #Tracks first nodes to be visited
        first = [None] * self.size

        #Tracks nodes that have been visited
        visited = [False] * self.size

        #Queue which starts the distance and nodes in a list
        queue = [(0, start)]

        #While the queue have began
        while queue:

            #Pops the first value from queue
            current_distance, current_node = heapq.heappop(queue)

            #Skips a node if its been visited
            if visited[current_node]:
                continue
            #Marks node as visited
            visited[current_node] = True

            #For neighbor in range of the graph
            for neighbor in range(self.size):

                #Weight attribute used to keep track of weight
                weight = self.adj_matrix[current_node][neighbor]

                #If weight exists and not visited yet
                if weight and not visited[neighbor]:

                    #New distance calculated
                    new_distance = current_distance + weight

                    #If the new distance is smaller than the current shortest path
                    if new_distance < min_distances[neighbor]:

                        #Updates new distance to the shortest path
                        min_distances[neighbor] = new_distance

                        #Updates the first node up to the current node
                        first[neighbor] = current_node

                        #Pushes new distance and neighbor to queue
                        heapq.heappush(queue, (new_distance, neighbor))

        #Initializes empty path list
        lowest_cost_path = []

        #Sets the current node index to end index
        current_node = end

        #While current node exists
        while current_node is not None:

            #inserts nodes at beginning of the path
            lowest_cost_path.insert(0, self.vertex_data[current_node])

            #Updates current node to first 
            current_node = first[current_node]

        #Returns path and distances
        return lowest_cost_path, min_distances[end]


        

    #Best path function
    def best_path(self, start_node_data):

        #Start node for vertex data
        start_node = self.vertex_data.index(start_node_data)

        #Tracks when a vertex has been visited
        visited = set([start_node])

        #empty minimum spanning tree
        mst = []

        #empty minimum array
        minimum = []

        #initializes best path cost and sets it to 0
        best_path_cost = 0

        #for neighbor in range of the size of graph
        for neighbor in range(self.size):

            #Creates weight attribute
            weight = self.adj_matrix[start_node][neighbor]

            #If weight exists then push the weight, start_node and neighbor to minimum array
            if weight > 0:
                heapq.heappush(minimum, (weight, start_node, neighbor))


        #While minimum
        while minimum:

            #Pops the minimum value from minimum array
            weight, end_vertex, start_vertex = heapq.heappop(minimum)

            #If start vertex is not in visited add it to visited
            if start_vertex not in visited:
                visited.add(start_vertex)

                #Adds the edge weight to the best path cost
                best_path_cost += weight

                #Appends to mst
                mst.append((self.vertex_data[end_vertex], self.vertex_data[start_vertex], weight))

                #for neighbor in range of the graph
                for neighbor in range(self.size):

                    #Initializes an edge weight
                    edge_weight = self.adj_matrix[start_vertex][neighbor]

                    #If the edge weight exists and neighbor not in visited
                    if edge_weight > 0 and neighbor not in visited:

                        #Pushes edge weight, start vertex and neighbor to minimum
                        heapq.heappush(minimum, (edge_weight, start_vertex, neighbor))

        #Returns mst and the cost of best path           
        return mst, best_path_cost
    

    #Dynamic Network changing method
    def network(self):

        #Initializes empty edge list to hold the edges
        edge = []

        #Iterating through vertex_u
        for vertex_u in range(self.size):

            #Iterating through vertex_v finding all vertices after vertex_v
            for vertex_v in range(vertex_u +1, self.size):

                #Initializes edge weight
                weight = self.adj_matrix[vertex_u][vertex_v]

                #If weight exists it pushes weight and both vertices to edge array
                if weight > 0:
                    heapq.heappush(edge, (weight, vertex_u, vertex_v))

        #Initializes parent variable list which tracks the set of each variable
        parent = list(range(self.size))

        #Initializes rank attribute with 0 for all vertices
        rank = [0] * self.size

        #Find function which discovers an element in a particular subset
        def find(parent, i):
            if parent[i] == i:
                return i
            parent[i] = find(parent, parent[i])
            return parent[i]

        #Apply union function which merges 2 sets into 1
        def apply_union(vertex_u, vertex_v):
            root_u = find(parent, vertex_u)
            root_v = find(parent, vertex_v)
            if root_u != root_v:
                    if rank[root_u] > rank[root_v]:
                        parent[root_v] = root_u
                    elif rank[root_u] < rank[root_v]:
                        parent[root_u] = root_v
                    else:
                        parent[root_v] = root_u
                        rank[root_u] += 1

        #Empty mst edges list to store edges
        mst_edges = []

        #Initializes mst weight to 0
        mst_weight = 0

        #For in the range and length of the edge which holds the edges for the graph
        for _ in range(len(edge)):

            #Pops the lowest cost edge
            weight, vertex_u, vertex_v = heapq.heappop(edge)

            #If the vertices are different then the sets will merge
            if find(parent, vertex_u) != find(parent, vertex_v):
                apply_union(vertex_u, vertex_v)

                #edges are appended
                mst_edges.append((vertex_u, vertex_v, weight))

                #Weight is added
                mst_weight += weight

                #Program stops if the mst has been found
                if len(mst_edges) == self.size - 1:
                    break

        return mst_edges, mst_weight

#Function used to help build graphs
def graphb(graph_dict):

    #Initializes nodes and creates a graph based on size
    nodes = list(graph_dict.keys())
    size = len(nodes)
    graph = Graph(size)

    #Places the correct names of nodes into correct order
    for index, names in enumerate(nodes):
        graph.add_node_data(index, names)

    #Dictionary that creates indexes 
    names_index = {names: i for i, names in enumerate(nodes)}

    #Finds the index of the last node
    for last_node, neighbors in graph_dict.items():
        last_index = names_index[last_node]

        #Finds index for the next node
        for next_node, weight in neighbors:
            next_index = names_index[next_node]

            #If the edge doesn't exist then it will add the edge to the graph connecting it to the last index and next index with the correct weight
            if graph.adj_matrix[last_index][next_index] == 0:
                graph.add_edge(last_index, next_index, weight)

    #Returns the graph
    return graph


#Test Cases

#Example Graph 1 for all 3 functions
example_graph1 = {
    "A": [("B", 4), ("C", 2)],
    "B": [("A", 4), ("C", 1), ("D", 5)],
    "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
    "D": [("B", 5), ("C", 8), ("E", 2)],
    "E": [("C", 10), ("D", 2)]
}

#Example Graph 2 for lowest cost function
example_graph_2 = {
    
    "A": [("B", 6), ("C", 4), ("D", 3) ],
    "B": [("A", 1),("C", 7), ("D", 8), ("E", 6)],
    "C": [("A", 6), ("B", 5), ("D", 8)],
    "D": [("B", 5), ("C", 8), ("E", 12)],
    "E": [("C", 10), ("D", 2)]
}

#Example graph 2 for best path function
example_graph_2_bp = {
    "A": [("B", 4), ("C", 2), ("D", 1)],
    "B": [("A", 1), ("C", 6)],
    "C": [("A", 5), ("B", 7), ("D", 3), ("E", 4)],
    "D": [("B", 2), ("C", 8), ("E", 4)],
    "E": [("A", 4),("C", 2), ("D", 10)]
}

#Example graph 3 for best path function
example_graph_3_bp = {
	"A": [("B", 7), ("C", 7), ("D", 7)],
	"B": [("A", 7), ("C", 7)],
	"C": [("A", 7), ("B", 7), ("D", 7), ("E", 7)],
	"D": [("B", 7), ("C", 7), ("E", 7)],
	"E": [("A", 7),("C", 7), ("D", 7)]
}

#Ecample graph 2 for network function
example_graph_2_net = {
	"A": [("B", 3), ("C", 1)],
	"B": [("A", 3),("C", 7), ("D", 5)],
	"C": [("A", 1), ("B", 7), ("D", 2),],
	"D": [("B", 5), ("C", 2), ("E", 7)],
	"E": [("D", 7), ("F", 2)],
	"F":[("E", 2)]
}

#Example graph 3 for network function
example_graph_3_net = {
	"A": [("B", 3)],
	"B": [("A", 3)],
	"C": [("D", 5)],
	"D": [("C", 5)]
}


#Calls on helper function to build graph
g = graphb(example_graph1)
g_2_lc = graphb(example_graph_2)
g_2_bp = graphb(example_graph_2_bp)
g_3_bp = graphb(example_graph_3_bp)
g_2_net = graphb(example_graph_2_net)
g_3_net = graphb(example_graph_3_net)



#Prints the lowest cost and path  
path1, cost_1_lc = g.lowest_cost("A", "E")
print("The Shortest Path from A to E:", " ->".join(path1))
print("The Lowest Cost:", cost_1_lc)

path2, cost_2_lc = g.lowest_cost("A", "B")
print("The Shortest path from A to B:", " ->".join(path2))
print("The Lowest Cost:", cost_2_lc)

path3, cost_3_lc = g_2_lc.lowest_cost("A", "E")
print("The Shortest Path from A to E:", " ->".join(path3))
print("The Lowest Cost:", cost_3_lc)

path4, cost_4_lc = g_2_lc.lowest_cost("A", "A")
print("The Shortest Path from A to A:", " ->".join(path4))
print("The Lowest Cost:", cost_4_lc)






#Prints the mst and the cost for the best path function
mst, cost_1_bp = g.best_path("A")

print("Minimuim Spanning Tree:", mst)
print("Cost:", cost_1_bp)

mst2, cost_2_bp = g_2_bp.best_path("A")

print("Minimuim Spanning Tree:", mst2)
print("Cost:", cost_2_bp)


mst3, cost_3_bp = g_3_bp.best_path("A")

print("Minimuim Spanning Tree:", mst3)
print("Cost:", cost_3_bp)



#Dictionary used to find the index of a node helping with dynamic changes
index_map1 = {name: i for i, name in enumerate(example_graph1.keys())}
index_map2 = {name: i for i, name in enumerate(example_graph_2_net.keys())}



#Adds and removes weighted edges from the graph to dynamically change 
g.adj_matrix[index_map1["C"]][index_map1["E"]] = 0
g.adj_matrix[index_map1["E"]][index_map1["C"]] = 0
g.adj_matrix[index_map1["B"]][index_map1["E"]] = 3

g_2_net.adj_matrix[index_map2["D"]][index_map2["E"]] = 0
g_2_net.adj_matrix[index_map2["B"]][index_map2["F"]] = 4



#Calls on network function
mst_edges, cost_1_net = g.network()

#Gives the names to the nodes to label and follow the path
labeled_mst_edges = [(g.vertex_data[vertex_u], g.vertex_data[vertex_v], weight) for vertex_u, vertex_v, weight in mst_edges]

#Prints mst and the cost
print("Minimuim Spanning Tree:", labeled_mst_edges)
print("Cost:", cost_1_net)
                     

mst_edges2, cost_2_net = g_2_net.network()

labeled_mst_edges2 = [(g_2_net.vertex_data[vertex_u], g_2_net.vertex_data[vertex_v], weight) for vertex_u, vertex_v, weight in mst_edges2]

print("Minimuim Spanning Tree:", labeled_mst_edges2)
print("Cost:", cost_2_net)


mst_edges3, cost_3_net = g_3_net.network()
labeled_mst_edges3 = [(g_3_net.vertex_data[vertex_u], g_3_net.vertex_data[vertex_v], weight) for vertex_u, vertex_v, weight in mst_edges3]

print("Minimuim Spanning Tree:", labeled_mst_edges3)
print("Cost:", cost_3_net)
