##
#  attribute_data.py
#  Class that generates data on DIGs and other networkx graphs, specifically
#  testing them for a pre-determined set of attributes. It collects the result
#  in a clear figure that is then shown.
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2017-11
##

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random as rn
from DIG import DottedIntervalGraph as DIG
import storage as st

def autolabel(rects):
	"""
	Attach a text label above each bar displaying its height
	"""
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width()/2., 1,
				'%d' % int(height),
				ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.5))

def draw_attr_graph(AD):
	"""
	this function takes the attr_data as its only argument, a dictionary of 
	the form {"attr":{"DIG":[mean, std_dev], "NX":[mean, std_dev]},
	          "attr2":{"DIG":[mean, std_dev], "NX":[mean, std_dev]},
	          etc...}
	and use this data to construct a barchart highlighting the differences
	between networkx and DottedIntervalGraphs
	"""
	N = len(AD)
	DIG_means = tuple([AD[attr]['DIG'][0] for attr in AD])
	DIG_std = tuple([AD[attr]['DIG'][1] for attr in AD])

	ind = np.arange(N)  # the x locations for the groups
	width = 0.45       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, DIG_means, width, color='r', yerr=DIG_std)

	NX_means = tuple([AD[attr]['NX'][0] for attr in AD])
	NX_std = tuple([AD[attr]['NX'][1] for attr in AD])
	rects2 = ax.bar(ind + width, NX_means, width, color='b', yerr=NX_std)

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Value')
	ax.set_title('Average values of different plot attributes')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(tuple([attr for attr in AD]), rotation=-45)

	ax.legend((rects1[0], rects2[0]), ('DIG', 'NX'))

	for rects in [rects1, rects2]:
		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2., height/10.,
					'%.2f' % height,
					ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.5))

	plt.tight_layout()
	plt.show()

def DIGtoNX(graph):
	G = nx.Graph()
	for node in graph:
		G.add_node(node)
	for edge in graph.edges():
		G.add_edge(*edge)
	return G

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

def gen_DIGs(N, iters, nodes):
	"""
	This function will generate <N> new DIG graphs, and for testing purposes
	convert them to standard networkx.Graph()s before returning them.
	"""
	return [DIGtoNX(gen_DIG(nodes, iters)) for _ in range(N)]

def gen_NXs(N, nodes, p_edge):
	"""
	This function generates <N> standard graphs with <nodes> amount of nodes
	and a probability of <p_edge> to have an edge between any two vertices
	"""
	return [nx.fast_gnp_random_graph(nodes, p_edge) for _ in range(N)]

def test_attr(function, graphs):
	"""
	This function takes a function and a list of graphs. It will then store
	the result of this function in a list and return the list.
	"""
	test_results = [function(graph) for graph in graphs]
	# filter any None, these may have slipped in if the function raised an error
	test_results = list(filter(lambda x: x != None, test_results))
	return [np.mean(test_results), np.std(test_results)]

def get_attr_data(AF, test_settings = (1000, 15, 10, 0.5)):
	"""
	This function generates two lists containing randomly generated nx graphs
	and as many DIG_graphs, converted to nx for testing purposes. It will then
	use the attributes and corresponding functions defined in <AF> to construct
	a dictionary containing the mean and standard deviation of the result of the
	functions, which is then returned.
	"""
	N_tests    = test_settings[0]
	iterations = test_settings[1]
	nodes      = test_settings[2]
	p_edge     = test_settings[3]
	# generate the lists of graphs using the settings
	DIG_graphs = gen_DIGs(N_tests, iterations, nodes)
	NX_graphs  = gen_NXs(N_tests, nodes, p_edge)

	attr_data = {}
	for attr in AF:
		attr_func = AF[attr]
		attr_data[attr] = {}
		# fill in the data in the dict
		attr_data[attr]["DIG"] = test_attr(attr_func, DIG_graphs)
		attr_data[attr]["NX"]  = test_attr(attr_func, NX_graphs)
	return attr_data

def diameter(graph):
	"""
	wrapper for the nx.diameter function to prevent errors when the diameter is
	infinitely high since the graph may be disconnected. In this case, return
	None. This value will later be filtered out when calculating the mean.
	"""
	try:
		return nx.diameter(graph)
	except Exception:
		return None

def show_attribute_data(AF, filename):
	attr_data = st.get_data(filename)
	if not attr_data[0]:
		attr_data = get_attr_data(AF)
		st.store_data(attr_data, filename)
	draw_attr_graph(attr_data[1])

AF = {"clique":nx.graph_clique_number,
	"connected components":nx.number_connected_components,
	"diameter*":diameter,
	"node connectivity":nx.node_connectivity,
	"edge connectivity":nx.edge_connectivity,
	}

show_attribute_data(AF, 'attribute_data.pickle')

# get_attr_data({"attr1":"func1","attr2":"func2"}, "DIG_graphs", "NX_graphs")

# test = {"clique_number":{"DIG":[20,3], "NX":[15,5]},
# 		"connectedness":{"DIG":[15,2], "NX":[12,6]},
# 		"something idk":{"DIG":[105,2], "NX":[120,6]}}