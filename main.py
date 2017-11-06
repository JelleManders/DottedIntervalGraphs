from fractions import gcd

# def xgcd(b, n):
# 	x0, x1, y0, y1 = 1, 0, 0, 1
# 	while n != 0:
# 		q, b, n = b // n, n, b % n
# 		x0, x1 = x1, x0 - q * x1
# 		y0, y1 = y1, y0 - q * y1
# 	return  b, x0, y0
	
class DottedIntervalGraph(object):
	"""docstring for DottedIntervalGraph"""
	def __init__(self):
		self.nodes = {}
		
	# adds node to datastructure, with a name and sequence
	def add_sequence(self, name, (offset, interval)):
		self.nodes[name] = (offset, interval)

	# removes node from datastructure
	def remove_node(self, name):
		del self.nodes[name]

	# returns an iterator over all edges in the graph
	def edges(self):
		nodes_list = self.nodes.items()
		nodes_amount = len(nodes_list)
		graph_edges = []
		print nodes_list
		for i in range(0, nodes_amount):
			name1 = nodes_list[i][0]
			for j in range (i+1, nodes_amount):
				name2 = nodes_list[j][0]
				print "has_edge?", name1, name2
				if self.has_edge(name1, name2):
					graph_edges.append((name1, name2))
		return graph_edges
	
	# returns an iterator over all neighbours of node <name>
	def neighbours(self, name):
		nodes_list = self.nodes.items()
		nodes_amount = len(nodes_list)
		neighbours = []
		for i in range(0, nodes_amount):
			other = nodes_list[i][0]
			if has_edge(name, other):
				neighbours.append(other)
		return neighbours
	
	# returns a bool indicating the presence of an edge between the two nodes
	def has_edge(self, name1, name2):
		if name1 == name2:
			return False
		(offset1, period1) = self.nodes[name1]
		(offset2, period2) = self.nodes[name2]
		print offset1-offset2, gcd(period2, period1)
		return 0 == ((offset1 - offset2) % gcd(period1, period2))

test_graph = DottedIntervalGraph()

print test_graph.edges()

# import random as rn

# class DottedIntervalGraph:
# 	"""docstring for DottedIntervalGraph"""
# 	def __init__(self):
# 		self.nodes = []
# 		return None
		
# 	def construct_nodes(self, N):
# 		for i in xrange(0,N):
# 			self.nodes.append(Node(i))
# 		return None

# 	def print_graph(self):
# 		print self.nodes, "\n", len(self.nodes)

# class Node:
# 	"""docstring for Node"""
# 	MAX_O = 100
# 	MIN_O = 2
# 	MAX_K = 50
# 	MIN_K = 5
# 	def __init__(self, i):
# 		o = rn.randint(self.MIN_O, self.MAX_O) # offset
# 		k = rn.randint(self.MIN_K, self.MAX_K) # step
# 		return (o, k, i) # return node element
