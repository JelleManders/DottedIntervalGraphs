##
#  New file to store the sequence tests in 
#
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2018-01
##

from pprint import pprint
import matplotlib.pyplot as plt
import storage as st
import networkx as nx
import numpy as np
import random as rn
from tqdm import tqdm as loading
from DIG import DottedIntervalGraph as DIG

def get_title(attr, params, g, D):
	param_lookup = {"O":"Offset", "D":"Step distance", "K":"Amount of steps"}
	attr_lookup = {"clustering":"Local Clustering Coefficient",
					"eccentricity":"Eccentricity",
					"connected":"Number of Connected Components per Node",
					"degree":"Average Degree"}
	param = params[0][:1]
	title = ("D = "+str(D)+": Effect of varying the " + 
			param_lookup[param]+ 
			" parameter on the\n" + 
			attr_lookup[attr]+ 
			" of both types of graph")
	filename = str(g) + "_graphs-attr_"+attr+"-D_"+str(D)+"-"+param
	return [title, filename]

def get_labels(params, probs):
	ret = []
	for i in range(len(params)):
		ret.append(params[i][1:]+'/'+probs[i])
	return tuple(ret)

def autolabel(rects):
	"""
	Attach a text label above each bar displaying its height
	"""
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width()/2., 1,
				'%d' % int(height),
				ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.5))

def draw_attr_graphs(DIG_data, NX_data, params, probs, D, g, comp):
	result_chunk = DIG_data[params[0]]
	for attribute in result_chunk:
		create_graph(DIG_data, NX_data, attribute, params, probs, D, g, comp)

def create_graph(DIG_data, NX_data, attr, params, probs, D, g, comp):
	N = len(DIG_data)
	DIG_means = tuple(DIG_data[param][attr][0] for param in params)
	DIG_std = tuple(DIG_data[param][attr][1] for param in params)

	ind = np.arange(N)  # the x locations for the groups
	width = 0.45       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, DIG_means, width, color='r', yerr=DIG_std)

	NX_means = tuple(NX_data[param][attr][0] for param in params)
	NX_std = tuple(NX_data[param][attr][1] for param in params)
	rects2 = ax.bar(ind + width, NX_means, width, color='b', yerr=NX_std)

	title = get_title(attr, params, g, D)

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Value')
	ax.set_xlabel('Bits used to store parameter/P_edge used to generate NX graphs')
	ax.set_title(title[0])
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(get_labels(params, probs))

	ax.legend((rects1[0], rects2[0]), ('DIG', 'NX'))

	for rects in [rects1, rects2]:
		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2., height/10.,
					'%.2f' % height,
					ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.5))

	plt.tight_layout()

	header = "images/comp-" if comp else "images/"

	filename = "final_"+header+title[1]+".png"
	print("Saved image in", filename)
	plt.savefig(filename)

	plt.close()

def test_attr(function, graphs):
	"""
	This function takes a function and a list of graphs. It will then store
	the result of this function in a list and return the list.
	"""
	test_results = [function(graph) for graph in graphs]
	# filter any None, these may have slipped in if the function raised an error
	test_results = list(filter(lambda x: x != None, test_results))
	if len(test_results) == 0:
		test_results = [0]
	return [np.mean(test_results), np.std(test_results)]

def degree_avg(graph):
	degrees = [x[1] for x in nx.degree(graph)]
	return np.mean(degrees)

def eccentricity(graph):
	"""
	wrapper for the nx.eccentricity function
	"""
	try:
		eccs = nx.eccentricity(graph)
		ecc_list = list(eccs.values())
		# print(ecc_list)
		return np.mean(ecc_list)
	except Exception as e:
		return None

def connected(graph):
	return float(nx.number_connected_components(graph)) / float(len(graph))

def clustering(graph):
	"""
	wrapper for the nx.clustering function
	"""
	try:
		clusters = nx.clustering(graph)
		# print("\nclusters:", list(clusters.values()), end = '\n\n')
		return np.mean(list(clusters.values()))
	except Exception:
		return None

def DIGtoNX(graph):
	"""
	Generates a standard networkx graph from a DIG
	"""
	G = nx.Graph()
	for node in graph:
		G.add_node(node)
	for edge in graph.edges():
		G.add_edge(*edge)
	return G

def gen_DIG(o, d, k, v):
	"""
	Gnerates a random DIG with n <nodes>
	"""
	G = DIG()
	for v in range(v):
		o_c = rn.randint(0,2**o-1)
		d_c = rn.randint(1,2**d)
		k_c = rn.randint(0,2**k-1)
		sequence = (o_c,d_c,k_c)
		G.add_sequence(v, sequence)
	return G

def gen_DIGs(o,d,k,v,g):
	path = "data/DIGs_o"+str(o)+"_d"+str(d)+"_k"+str(k)+"_v"+str(v)+"_g"+str(g)+".pkl"
	data = st.get_data(path)
	if data[0]:
		return data[1]
	else:
		DIGs = [DIGtoNX(gen_DIG(o,d,k,v)) for _ in range(g)]
		st.store_data(DIGs, path)
		return DIGs

def gen_NXs(v,p,g):
	path = "data/NXs_v"+str(v)+"_p"+str(p)+"_g"+str(g)+".pkl"
	data = st.get_data(path)
	if data[0]:
		return data[1]
	else:
		NXs = [nx.fast_gnp_random_graph(v, p) for _ in range(g)]
		st.store_data(NXs, path)
		return NXs

def gen_data(graphs, AF):
	attr_data = {}
	for setting in graphs:
		attr_data[setting] = {}
		for attr in AF:
			function = AF[attr]
			attr_data[setting][attr] = test_attr(function, graphs[setting])
	return attr_data

def lookup_p(o, d, k, comp):
	i = o*d*k
	table = {16:0.14,24:0.17,32:0.20,48:0.24,64:0.28,72:0.30,96:0.36,128:0.5}
	if comp:
		return 1 - table[i]
	return table[i]


def exec_test(graphs, param, D, values, comp):
	settings = [{"V":15, "P":0.80, "O":4,  "D":D, "K":4, "G":graphs},
				{"V":15, "P":0.80, "O":4,  "D":D, "K":4, "G":graphs},
				{"V":15, "P":0.80, "O":4,  "D":D, "K":4, "G":graphs},
				{"V":15, "P":0.80, "O":4,  "D":D, "K":4, "G":graphs}]
	for x in range(0,len(values)):
		settings[x][param] = values[x]
		settings[x]["P"] = lookup_p(settings[x]["O"],settings[x]["D"],settings[x]["K"], comp)

	params = [param + str(setting[param]) for setting in settings]
	probs = [str(setting["P"]) for setting in settings]

	DIGs = {}
	NXs = {}
	# print("Generating graphs...")
	for s in settings:
		DIGs[param+str(s[param])] = gen_DIGs(s["O"], s["D"], s["K"], s["V"], s["G"])
		NXs[param+str(s[param])] = gen_NXs(s["V"], s["P"], s["G"])

	# print("Done generating graphs!")

	AF = {
		"eccentricity": eccentricity,
		"clustering": clustering,
		"degree": degree_avg,
		"connected":connected
	}

	# print("Generating DIG data...")
	DIG_data = gen_data(DIGs, AF)

	# print("Generating NX data...")
	NX_data = gen_data(NXs, AF)

	# print("Done generating, starting graphs...")

	draw_attr_graphs(DIG_data, NX_data, params, probs, D, graphs, comp)

def run():

	OK_values = [2,4,6,8]
	D_values = [2,3,4]
	n = 1

	print("Starting....")
	for param in ["O", "K"]:
		for D_val in D_values:
			print(str(n) + ' -> ', end='')
			n += 1
			# print(param,D_val,OK_values,False)
			exec_test(1000, param, D_val, OK_values, False)

			print(str(n) + ' -> ', end='')
			n += 1
			# print(param,D_val,OK_values,True)
			exec_test(1000, param, D_val, OK_values, True)
	print('DONE!')

run()
