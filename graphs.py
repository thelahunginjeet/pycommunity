import networkx as nx

def two_triangles_integers():
	"""
        Trivial unweighted graph, integer node names.
        """
	G = nx.Graph()
	G.add_nodes_from([1,2,3,4,5,6])
	G.add_edge(1,2)
	G.add_edge(1,4)
	G.add_edge(2,4)
	G.add_edge(3,4)
	G.add_edge(3,5)
	G.add_edge(3,6)
	G.add_edge(5,6)
	return G

def two_triangles_letters():
	"""
        Same as the graph returned by two_triangles_integers, with letters for the node names.
        """
	G = nx.Graph()
	G.add_nodes_from(['A','B','C','D','E','F'])
	G.add_edge('A','B')
	G.add_edge('A','D')
	G.add_edge('B','D')
	G.add_edge('C','D')
	G.add_edge('C','E')
	G.add_edge('C','F')
	G.add_edge('E','F')
	return G

def simple_graph():
	"""
        Another simple graph used for test purposes.
        """
	G = nx.Graph()
	G.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
	G.add_edge(1,2)
	G.add_edge(1,3)
	G.add_edge(2,3)
	G.add_edge(2,10)
	G.add_edge(9,10)
	G.add_edge(2,7)
	G.add_edge(3,4)
	G.add_edge(7,6)
	G.add_edge(8,9)
	G.add_edge(7,8)
	G.add_edge(7,10)
	G.add_edge(7,9)
	G.add_edge(4,6)
	G.add_edge(4,5)
	G.add_edge(5,6)
	return G

def monkey_grooming_graph():
	"""
        Monkey grooming network; this network is weighted and has strings for node names.
        """
	G = nx.Graph()
	G.add_nodes_from(['066','R006','CN','ER','CY','EC','EZ','004','065','022','076','AC','EK','DL','KD','KE'])
	n2i = {1:'066',2:'R006',3:'CN',4:'ER',5:'CY',6:'EC',7:'EZ',8:'004',9:'065',10:'022',\
			11:'076',12:'AC',13:'EK',14:'DL',15:'KD',16:'KE'}
	G.add_edge(n2i[1],n2i[4],weight=17.0)
	G.add_edge(n2i[1],n2i[8],weight=52.0)
	G.add_edge(n2i[1],n2i[9],weight=29.0)
	G.add_edge(n2i[1],n2i[11],weight=1.0)
	G.add_edge(n2i[1],n2i[12],weight=5.0)
	G.add_edge(n2i[1],n2i[15],weight=1.0)
	G.add_edge(n2i[2],n2i[8],weight=4.0)
	G.add_edge(n2i[2],n2i[14],weight=1.0)
	G.add_edge(n2i[2],n2i[16],weight=3.0)
	G.add_edge(n2i[3],n2i[4],weight=20.0)
	G.add_edge(n2i[3],n2i[5],weight=13.0)
	G.add_edge(n2i[3],n2i[7],weight=2.0)
	G.add_edge(n2i[3],n2i[9],weight=2.0)
	G.add_edge(n2i[3],n2i[10],weight=1.0)
	G.add_edge(n2i[3],n2i[11],weight=14.0)
	G.add_edge(n2i[3],n2i[12],weight=4.0)
	G.add_edge(n2i[3],n2i[13],weight=3.0)
	G.add_edge(n2i[3],n2i[15],weight=6.0)
	G.add_edge(n2i[3],n2i[16],weight=2.0)
	G.add_edge(n2i[4],n2i[7],weight=19.0)
	G.add_edge(n2i[4],n2i[9],weight=1.0)
	G.add_edge(n2i[4],n2i[11],weight=7.0)
	G.add_edge(n2i[4],n2i[13],weight=4.0)
	G.add_edge(n2i[4],n2i[14],weight=1.0)
	G.add_edge(n2i[5],n2i[7],weight=3.0)
	G.add_edge(n2i[5],n2i[8],weight=1.0)
	G.add_edge(n2i[5],n2i[10],weight=2.0)
	G.add_edge(n2i[5],n2i[16],weight=12.0)
	G.add_edge(n2i[6],n2i[8],weight=3.0)
	G.add_edge(n2i[6],n2i[9],weight=2.0)
	G.add_edge(n2i[6],n2i[10],weight=1.0)
	G.add_edge(n2i[6],n2i[12],weight=8.0)
	G.add_edge(n2i[6],n2i[13],weight=1.0)
	G.add_edge(n2i[6],n2i[14],weight=7.0)
	G.add_edge(n2i[7],n2i[13],weight=3.0)
	G.add_edge(n2i[7],n2i[16],weight=1.0)
	G.add_edge(n2i[8],n2i[9],weight=49.0)
	G.add_edge(n2i[8],n2i[10],weight=7.0)
	G.add_edge(n2i[8],n2i[11],weight=6.0)
	G.add_edge(n2i[8],n2i[12],weight=10.0)
	G.add_edge(n2i[8],n2i[13],weight=9.0)
	G.add_edge(n2i[8],n2i[14],weight=15.0)
	G.add_edge(n2i[8],n2i[16],weight=1.0)
	G.add_edge(n2i[9],n2i[10],weight=11.0)
	G.add_edge(n2i[9],n2i[11],weight=5.0)
	G.add_edge(n2i[9],n2i[12],weight=16.0)
	G.add_edge(n2i[9],n2i[13],weight=26.0)
	G.add_edge(n2i[9],n2i[14],weight=44.0)
	G.add_edge(n2i[9],n2i[15],weight=11.0)
	G.add_edge(n2i[9],n2i[16],weight=1.0)
	G.add_edge(n2i[10],n2i[11],weight=2.0)
	G.add_edge(n2i[10],n2i[12],weight=8.0)
	G.add_edge(n2i[10],n2i[14],weight=1.0)
	G.add_edge(n2i[10],n2i[15],weight=4.0)
	G.add_edge(n2i[10],n2i[16],weight=14.0)
	G.add_edge(n2i[11],n2i[12],weight=9.0)
	G.add_edge(n2i[11],n2i[13],weight=9.0)
	G.add_edge(n2i[11],n2i[14],weight=15.0)
	G.add_edge(n2i[11],n2i[15],weight=37.0)
	G.add_edge(n2i[11],n2i[16],weight=1.0)
	G.add_edge(n2i[12],n2i[13],weight=5.0)
	G.add_edge(n2i[12],n2i[14],weight=23.0)
	G.add_edge(n2i[12],n2i[15],weight=4.0)
	G.add_edge(n2i[13],n2i[14],weight=27.0)
	G.add_edge(n2i[13],n2i[15],weight=6.0)
	G.add_edge(n2i[13],n2i[16],weight=6.0)
	G.add_edge(n2i[14],n2i[15],weight=5.0)
	G.add_edge(n2i[14],n2i[16],weight=3.0)
	G.add_edge(n2i[15],n2i[16],weight=1.0)
	return G

