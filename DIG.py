import random as rn

class DottedIntervalGraph:
	"""docstring for DottedIntervalGraph"""
	nodes = []
	def __init__(self, N):
		for i in xrange(0,N):
			self.nodes.append(Node(i))
		return None

	def print_graph(self):
		print nodes, len(nodes)

class Node:
	"""docstring for Node"""
	MAX_O = 100
	MIN_O = 2
	MAX_K = 50
	MIN_K = 5
	def __init__(self, i):
		o = rn.randint(self.MIN_O, self.MAX_O) # offset
		k = rn.randint(self.MIN_K, self.MAX_K) # step
		return (o, k, i) # return node element
