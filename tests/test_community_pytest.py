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
        edges = G.edges()
        for i in xrange(0,100):
            accept += rewiring.move_random_edge(G)
        assert len(G.edges()) == len(edges), "Number of edges should not have changed!"
        
    def test_swap_node_degrees(self):
        accept = 0.0
        G = graphs.simple_graph()
        deg = G.degree()
        for i in xrange(0,100):
            accept += rewiring.swap_random_edges(G)
        assert accept > 0.0, "No swaps were performed!"
        for k in G.degree():
            assert G.degree()[k] == deg[k], "Node degrees should not have changed!"

    def test_unweighted_modularity_matrix(self):
        G = graphs.simple_graph()
        Q = communities.modularity_matrix(G)
        assert Q.shape == (len(G.nodes()),len(G.nodes())),"Q matrix is the wrong shape!"
    
    def test_weighted_modularity_matrix(self):
        G = graphs.monkey_grooming_graph()
        Q1 = communities.modularity_matrix(G,edec=None)
        Q2 = communities.modularity_matrix(G,edec='weight')
        assert (Q1 != Q2).any(),"Weighted and unweighted Q matrices should not be identical!"

    def test_unweighted_spectral_decomp_noflip(self):
        G = graphs.simple_graph()
        Q = communities.modularity_matrix(G,edec=None)
        gList = communities.spectral_subgraph_decomposition(G,Q,G.nodes(),G.degree(weight=None))
        assert len(gList) == 2,"Graph should have been split!"

    def test_weighted_spectral_decomp_noflip(self):
        G = graphs.monkey_grooming_graph()
        Q = communities.modularity_matrix(G,edec='weight')
        gList = communities.spectral_subgraph_decomposition(G,Q,G.nodes(),G.degree(weight='weight'),edec='weight')
        assert len(gList) == 2,"Graph should have been split!"

    def test_find_communities_spectral_unweighted(self):
        G = graphs.simple_graph()
        clist = communities.find_communities_spectral(G)
        assert len(clist) == 3,"Three communities should have been found!"

    def test_find_communities_spectral_weighted(self):
        G = graphs.monkey_grooming_graph()
        clist = communities.find_communities_spectral(G,edec='weight')
        assert len(clist) == 3,"Three communities should have been found!"


        
