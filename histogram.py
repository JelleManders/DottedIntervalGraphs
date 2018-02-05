##
#  Histogram.py
#
#  This file contains a method that generates graphs, tests them for a specific
#  attribute and then plots a histogram reflecting the results. This result
#  is focussed on the difference between DIG and NX graphs.
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2018-01
##

import networkx as nx
import random as rn
import storage as st
import numpy as np
import matplotlib.pyplot as plt
from DIG import DottedIntervalGraph as DIG
from pprint import pprint

def create_graph(DIG_data, NX_empty_data, NX_full_data, attribute, o,d,k, graphs):
	N = len(DIG_data)   # The amount of points on the x-axis

	ind = np.arange(N)  # the x locations for the groups
	width = 0.3       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind-width, tuple(DIG_data[i] for i in DIG_data),           width, color='r')
	rects2 = ax.bar(ind,       tuple(NX_empty_data[i] for i in NX_empty_data), width, color='y')
	rects3 = ax.bar(ind+width, tuple(NX_full_data[i] for i in NX_full_data),   width, color='b')

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Amount')
	ax.set_xlabel(attribute.title())
	ax.set_title('Histogram showing the amount of '+attribute+' values over different graphs,\nOffset, Distance and Steps stored in %s, %s, and %s bits.' % (o,d,k))
	ax.set_xticks(ind)

	ax.legend((rects1[0], rects2[0], rects3[0]), ('DIG', 'NX p='+str(lookup_p(o,d,k,False)), 'NX p='+str(lookup_p(o,d,k,True))))

	plt.tight_layout()

	filename = "images/hists/histogram_"+attribute+"-G="+str(graphs)+"-O="+str(o)+'-D='+str(d)+"-K="+str(k)+".png"
	print("Saved image in", filename)
	plt.savefig(filename)

	plt.close()

def DIGtoNX(graph):
	"""
	Generates a standard networkx graph from a DIG
	"""
	G = nx.Graph()
	for node in graph:
		G.add_node(node)
	for edge in graph.edges():
		G.add_edge(*edge)
	print("Did one...")
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

def gen_hist_data(graphs, function):
	hist_data = {}
	for graph in graphs:
		graph_data = function(graph)
		for elem in graph_data:
			value = elem[1]
			if value in hist_data:
				hist_data[value] += 1
			else:
				hist_data[value] = 1
	return hist_data

def lookup_p(o, d, k, comp):
	i = o*d*k
	table = {16:0.14,24:0.17,32:0.20,36:0.21,
	         48:0.24,64:0.28,72:0.30,96:0.36,
	         108:0.40,128:0.5,  16*2*16:0.005}
	if comp:
		return 1 - table[i]
	return table[i]

def get_complete_hist_data(DIGs, NXs_empty, NXs_full):
	max_key = 0
	min_key = 100000
	for hist in [DIGs, NXs_empty, NXs_full]:
		for key in hist:
			if key > max_key: max_key = key
			if key < min_key: min_key = key

	complete_hist_data = {"DIG":{},"NX_e":{}, "NX_f":{}}
	for key in range(min_key, max_key+1):
		complete_hist_data["DIG"][key] = DIGs[key] if key in DIGs else 0
		complete_hist_data["NX_e"][key] = NXs_empty[key] if key in NXs_empty else 0
		complete_hist_data["NX_f"][key] = NXs_full[key] if key in NXs_full else 0
	return complete_hist_data

nodes = 1000
for o in [16]:
	for d in [2]:
		for k in [16]:
			DIGs = gen_DIGs(o,d,k,nodes,10)
			NXs_empty  = gen_NXs(nodes,lookup_p(o,d,k,False),10)
			NXs_full  = gen_NXs(nodes,lookup_p(o,d,k,True),10)

			DIG_hist_data = gen_hist_data(DIGs, nx.degree)
			NX_empty_hist_data  = gen_hist_data(NXs_empty, nx.degree)
			NX_full_hist_data  = gen_hist_data(NXs_full, nx.degree)

			complete_hist_data = get_complete_hist_data(DIG_hist_data, NX_empty_hist_data, NX_full_hist_data)

			create_graph(complete_hist_data["DIG"], complete_hist_data["NX_e"], complete_hist_data["NX_f"], 'degree', o,d,k, graphs)
