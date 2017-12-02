##
#  data.py
#  Class that generates data on DIGs and other networkx graphs
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2017-11
##

from DIG import DottedIntervalGraph as DIG
import random as rn
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import numpy as np
import pickle

def gen_DIG(nodes, iterations):
	G = DIG()
	for n in range(nodes):
		sequence = gen_seq(iterations)
		G.add_sequence(n, sequence)
	return G

def gen_seq(iterations):
	o = rn.randint(0,50)
	k = 2**(rn.randint(2,5))+1
	return (o,k,iterations)

def gen_data(nodes, iterations):
	edge_count_list = []
	for i in range(1000):
		g = gen_DIG(nodes, iterations)
		edge_count_list.append(len(g.graph_edges()))
	return edge_count_list

def gen_data_array(node_range, iter_range):
	test_results = {}
	print("generating data...")
	for n in node_range:
		for i in iter_range:
			print(n,i,"...")
			test_results["n="+str(n)+",i="+str(i)] = gen_data(n, i)
	with open('edgecountlists.pickle', 'wb')as f:
		pickle.dump(test_results, f, pickle.HIGHEST_PROTOCOL)
	print("generated data...")

def make_figure(node_range, iter_range):
	try:
		with open('edgecountlists.pickle', 'rb') as f:
			test_results = pickle.load(f)
		print("pickled file found")
	except Exception:
		print("pickled file not found")
		raise OSError
	fig = plt.figure()
	plt.title("Likelihood of edge over amount of nodes and number of iterations")
	plt.xlabel("number of iterations in all sequences")
	plt.ylabel("likelihood of edge between any pair of vertices (%)")
	plt.grid(True)
	colors = {5:'bo',10:'go',15:'ro',20:'yo',25:'co'}
	blue = mpatch.Patch(color='blue', label='nodes = 5')
	green = mpatch.Patch(color='green', label='nodes = 10')
	red = mpatch.Patch(color='red', label='nodes = 15')
	yellow = mpatch.Patch(color='yellow', label='nodes = 20')
	cyan = mpatch.Patch(color='cyan', label='nodes = 25')
	plt.legend(handles=[blue,green,red,yellow,cyan], loc=4)
	for nodes in node_range:
		for iterations in iter_range:
			this_result = test_results["n="+str(nodes)+",i="+str(iterations)]
			c = colors[nodes]
			x = iterations
			y = 100 * np.mean(this_result) / (nodes*(nodes-1)/2)
			yerror = np.std(this_result)
			plt.plot(x, y, c, markersize=(30-nodes)/2)
			plt.errorbar(x, y, yerr=yerror, color=c[0], capsize=5)
			# print("plotting", nodes, iterations, y)
	fig.savefig("plot.png")
	plt.show()

def test_edge_likelihood(gen):
	node_range = range(5,26,5)
	iter_range = range(4,41,4)
	if gen:
		gen_data_array(node_range,iter_range)
	make_figure(node_range,iter_range)

test_edge_likelihood(False)


# def test_p():
# 	for n in range(5,26,5):
# 		for p in [0.3,0.5,0.7,0.9]:
# 			total = 0
# 			for i in range(1,10001):
# 				g = gen_DIG(n, p)
# 				total += len(g.graph_edges())
# 			print("n:", n, "p_given:", p, "p_actual:", total / (i*(n*(n-1)/2)))

# def generate_stats(graph, iterations=1000):
# 	"""
# 	This function takes a graph and generates different statistics
# 	about the graph. The statistics currently included are:
# 	- 

# 	@param graph = nx.Graph | DIG
# 	@param iterations = int
# 	"""
# 	for _ in xrange(iterations):
