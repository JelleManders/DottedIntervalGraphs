from DIG import DottedIntervalGraph as DIG

def c5():
	G = DIG()
	for node, sequence in [(0, (1,1,2)), (1, (2,1,2)), (2, (3,1,2)), (3, (4,1,2)), (4, (1,4,2))]:
		G.add_sequence(node, sequence)
	return G

G = c5();
G.image()
