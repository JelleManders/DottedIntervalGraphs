from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt

class DottedIntervalGraph():
	"""
	DIG class, implements the Dotted Interval Graph datastructure
	
	@attribute nodedict = <dict>
	"""
	def __init__(self):
		# the dictionary in which the nodes are stored
		self.nodedict = {}

	def __len__(self):
		"""
		returns the amount of nodes in the datastructure
		
		@return int
		"""
		return len(self.nodedict)

	def __iter__(self): 
		"""
		returns an iterator over all nodes in the structure
		
		@return __iter__
		"""
		for node in self.nodedict:
			yield node

	def is_directed(self):
		"""
		networkx calls this function when calling its draw(),
		This function is implemented to prevent AttributeErrors
		
		@return bool
		"""
		return False
		
	def add_sequence(self, name, sequence):
		"""
		adds node to datastructure, with a name and sequence
		
		@var name = int
		@var sequence = tuple(int, int, int)
		"""
		self.nodedict[name] = sequence

	def remove_node(self, name):
		"""
		removes node from datastructure
		
		@var name = int
		"""
		del self.nodedict[name]

	# def nodes(self):
	# 	"""returns an iterator over all nodes in the graph
	#      seems to be unnecessary"""
	# 	return self.nodedict

	def edges(self):
		"""
		returns an iterator over all edges in the graph
		
		@return __iter__
		"""
		graph_edges = []
		for node1, node2 in combinations(self.nodedict.items(), 2):
			name1 = node1[0]
			name2 = node2[0]
			if self.has_edge(name1, name2):
				graph_edges.append((name1, name2))
		for edge in graph_edges:
			yield edge
	
	# def neighbors(self, name):
	# 	"""returns an iterator over all neighbours of node <name>,
	#      seems to be unnecessary"""
	# 	print("I was used", g(c()).lineno)
	# 	neighbours = []
	# 	for node in self.nodedict.items():
	# 		other = node[0]
	# 		if has_edge(name, other):
	# 			neighbours.append(other)
	# 	for node in neighbours:
	# 		yield node
	
	def has_edge(self, name1, name2):
		"""
		returns a bool indicating the presence of an edge between the two nodes
		
		@var name1 = int
		@var name2 = int
		@return bool
		"""
		(offset1, period1, steps1) = self.nodedict[name1]
		(offset2, period2, steps2) = self.nodedict[name2]

		set1 = [offset1 + x * period1 for x in range(0, steps1)]
		set2 = [offset2 + x * period2 for x in range(0, steps2)]
		if set(set1).isdisjoint(set2):
			return False
		return True

	def image(self, filename = "graph.png", circular = True):
		"""
		stores the current graph in an image, default locations is <graph.png>,
		default draw setting is circular

		@var filename = string
		@var circular = bool
		"""
		fig = plt.figure()
		if circular:
			nx.draw_circular(self, ax=fig.add_subplot(111))
		else:
			nx.draw(self, ax=fig.add_subplot(111))
		fig.savefig(filename)
