##
#  data.py
#  Class that generates data on DIGs and other networkx graphs
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2017-11
##

def generate_stats(graph, iterations=1000):
	"""
	This function takes a graph and generates different statistics
	about the graph. The statistics currently included are:
	- 

	@param graph = nx.Graph | DIG
	@param iterations = int
	"""
	for _ in xrange(iterations):
