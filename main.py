import networkx as nx
import matplotlib.pyplot as plt
from DIG import DottedIntervalGraph as DIG

G = DIG()

for node, sequence in [("node1",(20,7,5)),("node2",(25,11,7)),("node3",(36,135,11))]:
	G.add_sequence(node, sequence)

network = nx.Graph(G)
print network.adj
