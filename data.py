##
#  data.py
#  Class that generates data on DIGs and other networkx graphs
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2017-11
##

from DIG import DottedIntervalGraph as DIG
import random as rn

def gen_DIG(nodes, p = 0.5):
	G = DIG()
	for n in range(nodes):
		sequence = gen_seq(p)
		G.add_sequence(n, sequence)
	return G

def gen_seq(p):
	o = rn.randint(0,50)
	k = 2**(rn.randint(2,5))+1
	n = rn.randint(0,int(p*40))
	return (o,k,n)

def test_p():
	for n in range(5,26,5):
		for p in [0.3,0.5,0.7,0.9]:
			total = 0
			for i in range(1,10001):
				g = gen_DIG(n, p)
				total += len(g.graph_edges())
			print("n:", n, "p_given:", p, "p_actual:", total / (i*(n*(n-1)/2)))


test_p()

# def generate_stats(graph, iterations=1000):
# 	"""
# 	This function takes a graph and generates different statistics
# 	about the graph. The statistics currently included are:
# 	- 

# 	@param graph = nx.Graph | DIG
# 	@param iterations = int
# 	"""
# 	for _ in xrange(iterations):
