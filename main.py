from DIG import DottedIntervalGraph as DIG
import networkx as nx
import matplotlib.pyplot as plt

complete5 = nx.complete_graph(5)

def c5():
	G = DIG()
	for node, sequence in [(0, (1,1,2)), (1, (2,1,2)), (2, (3,1,2)), (3, (4,1,2)), (4, (1,4,2))]:
		G.add_sequence(node, sequence)
	return G

def DIGtoNX(graph):
	G = nx.Graph()
	for node in graph:
		G.add_node(node)
	for edge in graph.edges():
		G.add_edge(*edge)
	return G

# G = nx.dodecahedral_graph()
G = c5();
# G.image()

# print(set(complete5), set(G))

print("Clique complete:", nx.graph_clique_number(complete5))
print("Clique c5:", nx.graph_clique_number(DIGtoNX(G)))
