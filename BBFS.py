# class AdjacentNode:

# 	def __init__(self, vertex):

# 		self.vertex = vertex
# 		self.next = None

# # BidirectionalSearch implementation
# class BidirectionalSearch:

# 	def __init__(self, vertices):

# 		# Initialize vertices and
# 		# graph with vertices
# 		self.vertices = vertices
# 		self.graph = [None] * self.vertices

# 		# Initializing queue for forward
# 		# and backward search
# 		self.src_queue = list()
# 		self.dest_queue = list()

# 		# Initializing source and
# 		# destination visited nodes as False
# 		self.src_visited = [False] * self.vertices
# 		self.dest_visited = [False] * self.vertices

# 		# Initializing source and destination
# 		# parent nodes
# 		self.src_parent = [None] * self.vertices
# 		self.dest_parent = [None] * self.vertices

# 	# Function for adding undirected edge
# 	def add_edge(self, src, dest):

# 		# Add edges to graph

# 		# Add source to destination
# 		node = AdjacentNode(dest)
# 		node.next = self.graph[src]
# 		self.graph[src] = node

# 		# Since graph is undirected add
# 		# destination to source
# 		node = AdjacentNode(src)
# 		node.next = self.graph[dest]
# 		self.graph[dest] = node

# 	# Function for Breadth First Search
# 	def bfs(self, direction = 'forward'):

# 		if direction == 'forward':

# 			# BFS in forward direction
# 			current = self.src_queue.pop(0)
# 			connected_node = self.graph[current]

# 			while connected_node:
# 				vertex = connected_node.vertex

# 				if not self.src_visited[vertex]:
# 					self.src_queue.append(vertex)
# 					self.src_visited[vertex] = True
# 					self.src_parent[vertex] = current

# 				connected_node = connected_node.next
# 		else:

# 			# BFS in backward direction
# 			current = self.dest_queue.pop(0)
# 			connected_node = self.graph[current]

# 			while connected_node:
# 				vertex = connected_node.vertex

# 				if not self.dest_visited[vertex]:
# 					self.dest_queue.append(vertex)
# 					self.dest_visited[vertex] = True
# 					self.dest_parent[vertex] = current

# 				connected_node = connected_node.next

# 	# Check for intersecting vertex
# 	def is_intersecting(self):

# 		# Returns intersecting node
# 		# if present else -1
# 		for i in range(self.vertices):
# 			if (self.src_visited[i] and
# 				self.dest_visited[i]):
# 				return i

# 		return -1

# 	# Print the path from source to target
# 	def print_path(self, intersecting_node,
# 				src, dest):

# 		# Print final path from
# 		# source to destination
# 		path = list()
# 		path.append(intersecting_node)
# 		i = intersecting_node

# 		while i != src:
# 			path.append(self.src_parent[i])
# 			i = self.src_parent[i]

# 		path = path[::-1]
# 		i = intersecting_node

# 		while i != dest:
# 			path.append(self.dest_parent[i])
# 			i = self.dest_parent[i]

# 		print("*****Path*****")
# 		path = list(map(str, path))

# 		print(' '.join(path))

# 	# Function for bidirectional searching
# 	def bidirectional_search(self, src, dest):

# 		# Add source to queue and mark
# 		# visited as True and add its
# 		# parent as -1
# 		self.src_queue.append(src)
# 		self.src_visited[src] = True
# 		self.src_parent[src] = -1

# 		# Add destination to queue and
# 		# mark visited as True and add
# 		# its parent as -1
# 		self.dest_queue.append(dest)
# 		self.dest_visited[dest] = True
# 		self.dest_parent[dest] = -1

# 		while self.src_queue and self.dest_queue:

# 			# BFS in forward direction from
# 			# Source Vertex
# 			self.bfs(direction = 'forward')

# 			# BFS in reverse direction
# 			# from Destination Vertex
# 			self.bfs(direction = 'backward')

# 			# Check for intersecting vertex
# 			intersecting_node = self.is_intersecting()

# 			# If intersecting vertex exists
# 			# then path from source to
# 			# destination exists
# 			if intersecting_node != -1:
# 				print(f"Path exists between {src} and {dest}")
# 				print(f"Intersection at : {intersecting_node}")
# 				self.print_path(intersecting_node,
# 								src, dest)
# 				exit(0)
# 		return -1

# if __name__ == '__main__':

# 	# Number of Vertices in graph
# 	n = 15

# 	# Source Vertex
# 	src = 0

# 	# Destination Vertex
# 	dest = 14

# 	# Create a graph
# 	graph = BidirectionalSearch(n)
# 	graph.add_edge(0, 4)
# 	graph.add_edge(1, 4)
# 	graph.add_edge(2, 5)
# 	graph.add_edge(3, 5)
# 	graph.add_edge(4, 6)
# 	graph.add_edge(5, 6)
# 	graph.add_edge(6, 7)
# 	graph.add_edge(7, 8)
# 	graph.add_edge(8, 9)
# 	graph.add_edge(8, 10)
# 	graph.add_edge(9, 11)
# 	graph.add_edge(9, 12)
# 	graph.add_edge(10, 13)
# 	graph.add_edge(10, 14)

# 	out = graph.bidirectional_search(src, dest)

# 	if out == -1:
# 		print(f"Path does not exist between {src} and {dest}")

from AdditionalFunctions import *
from IDS import Node

def print_frontier(frontier):
    for f in frontier:
        print('r in frontier: ', f.robot_coordinates)


# this function checks whether we reach the end of the BBFS Algorithm or not. 
# if two exact environments in forward frontier and backward frontier are found then it's finished.
def end_checker(forward_frontier, backward_frontier):
    for forward_node in forward_frontier:
        for backward_node in backward_frontier:
            if forward_node.environment == backward_node.environment:
                return True, forward_node
    return False, forward_node  # this node is not important.


# creating children in BFS is not the same with IDS. in BFS children are added at the end of the frontier queue
def bfs_forward(node, frontier):
    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    print('*****************')
    print('curr env: \n', node.environment)
    print('curr robot coor \n', node.robot_coordinates)
    all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    print('all permited movements: ', all_permitted_movements)

    for movement in all_permitted_movements:
        # print('loop curr env is: ', node.environment)
        new_environment, new_robot_coordinates = update_environment(node.environment, node.robot_coordinates, movement)
        # print('for movement ', movement, 'robot coor is: ',new_robot_coordinates, 'environment is: ', new_environment)
        # print('new env: ', new_environment)
        # print('curr env: ', node.environment)
        # new states should be checked. they should not be repetetive states.
        if new_environment != node.parent.environment:
            child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement)
            frontier.append(child_node)

    print('frontier len is:', len(frontier))
    print_frontier(frontier)
    print('*****************')

    return frontier


def BBFS(environment, robot_coordinates):

    forward_frontier, backward_frontier = [], []
    # initialize robot coordinates to initial node
    initial_node = Node(environment, robot_coordinates, 0, ' ')
    forward_frontier.insert(0, initial_node)


    # create childern of initial node and then create childern in a loop until we reach Goal state
    for i in range(100):
    # while True:
        if len(forward_frontier) > 0:
            forward_frontier = bfs_forward(forward_frontier.pop(0), forward_frontier)

        # backward dfs should be called here
        if len(backward_frontier) > 0:
            backward_frontier = bfs_backward()

        is_end, intersected_node = end_checker(forward_frontier, backward_frontier)
        if is_end:
            break

    # find and print final path

    return "finish"


if __name__ == '__main__':
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        "test1.txt")
    print('environment without cost: \n', environment_without_cost)
    s = BBFS(environment_without_cost, robot_coordinates)
    print(s)
