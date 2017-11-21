import networkx as nx
import matplotlib.pyplot as plt
from DIG import DottedIntervalGraph as DIG

def a123():
	G = DIG()
	for node, sequence in [("node1",(20,7,5)),("node2",(25,11,7)),("node3",(36,135,11))]:
		G.add_sequence(node, sequence)
	return G

def c5():
	G = DIG()
	for node, sequence in [(0, (1,1,2)), (1, (2,1,2)), (2, (3,1,2)), (3, (4,1,2)), (4, (1,4,2))]:
		G.add_sequence(node, sequence)
	return G

print("\n#####  nx.dodecahedral_graph:  #####\n")
G = nx.dodecahedral_graph()
nx.draw(G)


print("\n#####  DIG.c5:  #####\n")
G = c5();
G.gen_adj()
print(list(G.edges()))
	# print(e)
# print(G._adj['node2']['node3'].get(1, 1))
nx.draw(G)