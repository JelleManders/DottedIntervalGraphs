# import networkx as nx
# import matplotlib.pyplot as plt
from DIG import DottedIntervalGraph as DIG

G = DIG()

G.construct_nodes(5)

G.print_graph()

# G = nx.petersen_graph()

# nx.draw(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

# plt.savefig("test.png")