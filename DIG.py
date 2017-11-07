from itertools import combinations

class DottedIntervalGraph(object):
	"""docstring for DottedIntervalGraph"""
	def __init__(self):
		self.nodes = {}
		self.current = None
		self.list = None

	def __len__(self):
		"""returns the amount of nodes in the datastructure"""
		return len(self.nodes)

	def __iter__(self): 
		return self

	def next(self):
		if self.current == None:
			self.list = self.nodes.items()
			self.current = 0
			return self.list[0]
		if self.current < len(self)-1:
			self.current += 1
			return self.list[self.current]
		else:
			raise StopIteration

	def is_directed(self):
		return False
		
	def add_sequence(self, name, (offset, interval, steps)):
		"""adds node to datastructure, with a name and sequence"""
		self.nodes[name] = (offset, interval, steps)

	def remove_node(self, name):
		"""removes node from datastructure"""
		del self.nodes[name]

	def edges(self):
		"""returns an iterator over all edges in the graph"""
		graph_edges = []
		for node1, node2 in combinations(self.nodes.items(), 2):
			name1 = node1[0]
			name2 = node2[0]
			if self.has_edge(name1, name2):
				graph_edges.append((name1, name2))
		return graph_edges
	
	def neighbours(self, name):
		"""returns an iterator over all neighbours of node <name>"""
		neighbours = []
		for node in self.nodes.items():
			other = node[0]
			if has_edge(name, other):
				neighbours.append(other)
		return neighbours
	
	def has_edge(self, name1, name2):
		"""returns a bool indicating the presence of an edge between the two nodes"""
		(offset1, period1, steps1) = self.nodes[name1]
		(offset2, period2, steps2) = self.nodes[name2]

		set1 = [offset1 + x * period1 for x in range(0, steps1)]
		set2 = [offset2 + x * period2 for x in range(0, steps2)]
		if set(set1).isdisjoint(set2):
			return False
		return True
