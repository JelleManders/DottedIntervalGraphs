##
#  DIG.py
#  Class that implements the Dotted Interval Graph datastructure
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2017-11
##

from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx

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
		return iter(self.nodedict)

	def __getitem__(self, key):
		try:
			return self.nodedict[key]
		except KeyError:
			raise KeyError

	def is_multigraph(self):
		"""
		networkx calls this function in nx.graph_clique_number(),
		This function is implemented to prevent AttributeErrors
		
		@return bool
		"""
		return False

	def is_directed(self):
		"""
		networkx calls this function when calling its draw(),
		This function is implemented to prevent AttributeErrors
		
		@return bool
		"""
		return False

	def order(self):
		"""
		networkx calls this function when calling nx.diameter(),
		This function is implemented to prevent AttributeErrors

		@return int
		"""
		return len(self)
		
	def add_sequence(self, name, sequence):
		"""
		adds node to datastructure, with a name and sequence
		
		@param name = int
		@param sequence = tuple(int, int, int)
		"""
		self.nodedict[name] = sequence

	def remove_node(self, name):
		"""
		removes node from datastructure
		
		@param name = int
		"""
		del self.nodedict[name]

	def graph_edges(self):
		graph_edges = []
		for node1, node2 in combinations(self.nodedict.items(), 2):
			name1 = node1[0]
			name2 = node2[0]
			if self.has_edge(name1, name2):
				graph_edges.append((name1, name2))
		return graph_edges

	def edges(self):
		"""
		returns an iterator over all edges in the graph
		
		@return __iter__
		"""
		graph_edges = self.graph_edges()
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
		
		@param name1 = int
		@param name2 = int
		@return bool
		"""
		(offset1, period1, steps1) = self.nodedict[name1]
		(offset2, period2, steps2) = self.nodedict[name2]
		# construct set, check for item in other set if in first set
		dotlist = [offset1 + x * period1 for x in range(0, steps1)]
		for dot in [offset2 + x * period2 for x in range(0, steps2)]:
			if dot in dotlist:
				return True
		return False

	def image(self, filename = "graph.png", circular = True):
		"""
		stores the current graph in an image, default locations is <graph.png>,
		default draw setting is circular

		@param filename = string
		@param circular = bool
		"""
		fig = plt.figure()
		if circular:
			nx.draw_circular(self, ax=fig.add_subplot(111))
		else:
			nx.draw(self, ax=fig.add_subplot(111))
		fig.savefig(filename)
