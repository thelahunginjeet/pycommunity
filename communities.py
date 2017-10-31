#!/usr/bin/env python
# encoding: utf-8
"""
communitydet.py

Algorithms and classes for community detection (both weighted and unweighted) in graphs.

Created by brown on 2011-08-16.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys,os,unittest,copy
import numpy as np
from numpy import real_if_close,zeros,max,diag
from numpy.linalg import eig
import networkx as nx

def modularity_weighted(G,comm_assign,edec):
    pass


def modularity_unweighted(G,comm_assign):
    '''
    Computes Newman's modularity Q for a given assignment of nodes to communities.
    Defined for unweighted graphs.

    INPUT
    -------
    G : networkx graph, required

    comm_assign: dict, required
        a dictionary keyed on node mapped to community assignments in the range
        0,...,c-1
    '''
    # figure out the number of communities
    c = max(comm_assign.values()) + 1
    e_ij = zeros((c,c))
    # compute edge fractions
    for e in G.edges():
        ci = comm_assign[e[0]]
        cj = comm_assign[e[1]]
        e_ij[ci,cj] += 1.0
    # normalize
    e_ij = e_ij/len(G.edges())
    # compute a_i by summing over columns
    a_i = e_ij.sum(axis=1)
    # compute and return Q
    return diag(e_ij - a_i**2).sum()


def modularity_matrix(G,edec=None):
    '''
    Computes the 'master' modularity matrix, without subgraph corrections.  The
    modularity matrix is defined as

                    Q(i,j) = A(i,j) - (k_i*k_j)/sum(k_i)

    where A is the adjacency matrix (weighted) of G and k_i are the (weighted)
    node degrees.

    INPUT
    -------

    G: networkx graph, required
        input graph for which modularity matrix is desired

    edec : string, optional
        edge decorator (name for weights) in weighted graphs

    OUTPUT:

    Q : numpy array
        Q will be of size len(G.nodes()) X len(G.nodes())
    '''
    # adjacency matrix piece (ordered according to G.nodes())
    Q = nx.adj_matrix(G,weight=edec)
    # degree-product portion (same order as adj_matrix!)
    nodes = G.nodes()
    ki = G.degree(weight=edec)
    kvec = np.zeros((len(nodes),1))
    for i in xrange(0,len(nodes)):
        kvec[i] = ki[nodes[i]]
    return Q - np.dot(kvec,kvec.T)/sum(ki.values())


def spectral_subgraph_decomposition(g,Q,nodes,ki,edec=None,flip=False,eps=1.0e-12):
    '''
    Attempts to split a subgraph g of a larger graph G (g can also equal G) into two
    parts that maximizes modularity.

    INPUT
    ------
    g : networkx graph, required
        subgraph to decompose

    Q : numpy array, required
        master modularity matrix for the larger graph G, NOT g (unless g = G)

    nodes : list, required
        list of nodes from the original graph (used to determine node-position mapping
        in mater matrix)

    ki : dictionary, required
        node degrees for larger graph G, NOT g (unless g = G)

    edec : string, optional
        edge decorator; string giving the edge decorator corresponding to weight for
        weighted graphs

    flip: boolean, optional
        set to true to perform a heuristic reassignment step of each node (swapping the
        spectral community assignment) to attempt to improve the modularity

    eps: float, optional
        if splitting g into two communities results in a modularity change < eps, the
        split is rejected

    OUTPUT
    ------
    gList : list
        list of graphs after split performed
            -if len(gList) == 1, the modularity cannot be improved by splitting g, and the
                single element of the list will be the input g
            -if len(gList) == 2, the list contains two graphs which are the subgraphs g1,g2
                obtained by spectral decomposition + optional heuristic reassignment

    '''
    # will store new subgraphs after decomposition
    gList = []
    # need a node name -> integer mapping for the parent graph
    # make this a function?
    counter = 0
    nodeDict = {}
    for x in nodes:
        nodeDict[x] = counter
        counter += 1
    # parent graph degree sum
    kisum = 1.0*sum(ki.values())
    # subgraph nodes and degrees
    sgNodes = g.nodes()
    sgki = g.degree(weight=edec)
    # indexing into master modularity matrix
    sgNodeIndices = [nodeDict[x] for x in sgNodes]
    BsubG = Q[np.ix_(sgNodeIndices,sgNodeIndices)]
    # ratio of degree sums for subgraph nodes to all nodes
    ndr = sum([ki[x] for x in sgNodes])/kisum
    # subgraph correction to BsubG
    for i in xrange(0,len(sgNodes)):
        BsubG[i,i] = BsubG[i,i] - (sgki[sgNodes[i]] - ndr*ki[sgNodes[i]])
    # decomposition of BsubG
    evals,evecs = eig(BsubG)
    # small imaginary parts sometime crop up due to numerical instability
    evals = real_if_close(evals)
    evecs = real_if_close(evecs)
    # find index of leading eigenvalue
    leadIndx = np.argmax(evals)
    if evals[leadIndx] < 0:
        # nothing to be gained by subdivision; append the input graph
        gList.append(g)
    else:
	s = np.sign(evecs[:,leadIndx])
        # change in modularity
        dQ = (1.0/(2.0*kisum))*np.dot(np.dot(s.T,BsubG),s)[0,0]
        if dQ > eps:
            # subdivision worthwhile; perform heuristic split
	    if flip:
	    	sprime = copy.copy(s)
                for i in xrange(len(sprime)):
                    # flip node from community 1 -> 2
	    	    sprime[i] = -1*sprime[i]
                    # compute modularity change
                    dQs = (1.0/(2.0*kisum))*np.dot(np.dot(sprime.T,BsubG),sprime)[0,0]
                    # reject small modularity changes
                    if (dQs - dQ) < eps:
	    		sprime[i] = -1*sprime[i]
	    	s = sprime
            # determine the community split
            spinU = []
            spinD = []
            for i in xrange(len(sgNodes)):
                if s[i] < 0:
                    spinD.append(sgNodes[i])
                else:
                    spinU.append(sgNodes[i])
            # add to gList
            gList.append(g.subgraph(spinU))
            gList.append(g.subgraph(spinD))
	else:
            # no point in subdividing, just return the input graph
	    gList.append(g)
    return gList


def find_communities_spectral(G,edec=None,eps=1.0e-12,flip=False):
    '''
    Performs successive splits of the input graph G into community subgraphs.  Terminates
    when further subdivision increases Newman's modularity (Q) less than eps.

    Set flip=True to try a heuristic reassignment at each binary split (each node is swapped
    into the other community and any modularity increasing moves are retained).


    INPUT
    -------
    G : networkx graph, required
        graph to subdivide into communities

    edec : string or None, optional
        name of the edge weights, if the graph is weighted

    eps : float, optional
        criterion to decide if Q improves enough to make subdivision worthwhile

    flip : boolean, optional
        set to True to try heuristic reassignment at each subgraph split


    OUTPUT
    -------
    clist : list of tuples of nodes; each tuple is a community
        (community numbers are aribtrary)

    '''
    # original graph statistics - used repeatedly
    Gnodes = G.nodes()
    Gki = G.degree(weight=edec)
    GQ = modularity_matrix(G,edec)
    # begin with one graph (single community), which we assume will be splittable
    #   value means indivisible = False (so binary community assignment is worthwhile)
    oldCDict = { G : False }
    # repeat until ALL subgraphs are indivisible (so nothing can be futher split)
    while True:
        newCDict = {}
	for g,indiv in oldCDict.items():
	    if indiv == True:
                # graph is not divisible - just copy it on
		newCDict[g] = indiv
		continue
	    else:
                # try to decompose the graph
                gList = spectral_subgraph_decomposition(g,GQ,Gnodes,Gki,edec,flip,eps)
		if len(gList) == 1:
		    # division did not improve the modularity; subgraph is now known to
                    #   be indivisible
		    newCDict[gList[0]] = True
		else:
		    # split was successful, assume child graphs are also divisible
		    newCDict[gList[0]] = False
		    newCDict[gList[1]] = False
        # make sure there is a divisible subgraph; otherwise we are done
        if len(newCDict) == sum(newCDict.values()):
	    break
	else:
	    oldCDict = newCDict
    # construct and return the communities list
    clist = []
    for g in newCDict:
       clist.append(tuple(np.sort(g.nodes())))
    return clist


'''
class CommunityDetector(object):
	def __init__(self):
		# translate node names into integers (and back again)
		self.nodeToInt = dict()
		self.intToNode = dict()

	def detect_community_structure(self,G,**kwargs):
		"""Overload this method in derived classes to implement particular methods."""
		pass


class DegreeBasedCommunityDetector(CommunityDetector):
	def __init__(self):
		super(DegreeBasedCommunityDetector,self).__init__()


	def detect_community_structure(self,G):
		"""Probably will not work well.  Procedure:
			[1] sort the nodes by degree
			[2] start the first community with the highest degree node
			[3] for each addl node, in order of degree, figure out how many connections
				it shares with the existing communities (call this c_i)
			[4] if c_i > 0 for some i, assign the node to community argmax(c_i)
			[5] if all c_i's are zero, put the node in a new community
			[6] repeat until there are no remaining nodes
		"""
		commDict = {}
		cCounter = 0
		# easier to work with the adjacency matrix
		nD,revND,A = gutil.adj_matrix(G)
		indxOrder = np.argsort(A.sum(axis=0))[-1::-1]
		# first community is the highest degree node
		commDict[cCounter] = [revND[indxOrder[0]]]
		cCounter += 1
		for i in xrange(1,len(indxOrder)):
			# connections from the current node to current communities
			nConn = []
			for k in sorted(commDict.keys()):
				nodesToCheck = [nD[x] for x in commDict[k]]
				nConn.append(sum(map(lambda x : A.item(indxOrder[i],x),nodesToCheck)))
			# now figure out where to put it
			if sum(nConn) == 0:
				# start a new community
				commDict[cCounter] = [revND[indxOrder[i]]]
				cCounter += 1
			else:
				# winner take all
				commDict[np.argmax(nConn)] += [revND[indxOrder[i]]]
		return commDict

'''
