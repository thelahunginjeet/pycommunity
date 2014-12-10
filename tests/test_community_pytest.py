from pycommunity import *

class TestCommunity:

    def setup(self):
        pass

    def test_add_edge(self):
        G = graphs.simple_graph()
        nEdges = len(G.edges())
        edges = G.edges()
        flag = rewiring.add_random_edge(G)
        if flag:
            assert len(G.edges()) == nEdges + 1, "Edge should have been added!"
        else:
            assert G.edges() == edges, "Addition should have failed!"

    def test_remove_edge(self):
        G = graphs.simple_graph()
        nEdges = len(G.edges())
        edges = G.edges()
        flag = rewiring.remove_random_edge(G)
        if flag:
            assert len(G.edges()) == nEdges - 1, "Edge should have been removed!"
        else:
            assert G.edges() == edges, "Edges should not have changed!"

    def test_move_edge(self):
        G = graphs.simple_graph()
        nEdges = len(G.edges())
        edges = G.edges()
        flag = rewiring.move_random_edge(G)
        if flag:
            assert len(G.edges()) == nEdges, "Number of edges should not have changed!"
        else:
            assert G.edges() == edges, "Edges should not have changed!"


    def test_swap_edges(self):
        G = graphs.simple_graph()
        nEdges = len(G.edges())
        edges = G.edges()
        flag = rewiring.swap_random_edges(G)
        if flag:
            assert len(G.edges()) == nEdges, "Number of edges should not have changed!"
        else:
            assert G.edges() == edges, "Edges should not have changed!"


    def test_move_degree_dist(self):
        from numpy import sort
        accept = 0.0
        G = graphs.simple_graph()
        deg = sort(G.degree().values())
        for i in xrange(0,100):
            accept += rewiring.move_random_edge(G)
        assert sort(G.degree().values()).all() == deg.all(), "Degree distribution should not have changed!"
        

    def test_swap_node_degrees(self):
        accept = 0.0
        G = graphs.simple_graph()
        deg = G.degree()
        for i in xrange(0,100):
            accept += rewiring.swap_random_edges(G)
        assert accept > 0.0, "No swaps were performed!"
        for k in G.degree():
            assert G.degree()[k] == deg[k], "Node degrees should not have changed!"
        
