import scd
import re
import struct
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool
import itertools
import webcolors


class PolychromeEval():
	
	def __init__(self):
		self.polychrome = scd.Polychrome()
		self.magickMap = self.polychrome.createMap("magick")
		# self.xkcdMap = self.createMap("xkcd")
		# self.reseneMap = self.createMap("resene")
		# self.bangMap = self.createMap("bang")
		# self.hollaschMap = self.createMap("hollasch", extras=True)
		# self.ralMap = self.createMap("ral", extras=True)
		self.nbsIsccMap = self.polychrome.createMap("nbsiscc")
		self.improvedNbsIsccMap = self.polychrome.createMap("nbsiscc_improved", extras=True)
		# self.wikiMap = self.createMap("wiki")
		# self.coatedPantoneMap = self.createMap("coatedpantone")
		# self.ntcMap = self.createMap("ntc")
		self.swm_count = 0
		self.swm_correlate = []
		self.nbs_count = 0
		self.nbs_correlate = []
		self.total = 0
	
	def hex2rgb(self, hexVal):	
		if hexVal.startswith('#'):
			hexVal = hexVal[1:]
		return tuple([int(hexVal[i:i + 2], 16) for i in xrange(0, len(hexVal), 2)])

		
	def specWebAndMagickEquivalence(self, test_color, graph):
		magick = self.polychrome.getMagickName(test_color)
		m = ''.join([x.lower() for x in magick[0].split()])
		specweb = self.polychrome.getWebName(test_color,"specific")
		s = specweb[0].lower()
		mColor = self.hex2rgb(magick[1])
		sColor = self.hex2rgb(specweb[1])
		print magick, m, mColor
		print specweb, s, sColor
		graph.add_node(m, {"node_color":mColor})
		graph.add_node(s, {"node_color":sColor})
		print graph.number_of_nodes()
		if s == m:
			self.swm_count += 1
			print self.sameNameDiffHex(specweb,magick)
			print s, sColor
			print m, mColor

			# nx.draw_networkx_nodes(graph,graph.pos, nodelist=[s,m],node_color=[specweb[1],magick[1]])
			# self.swm_correlate.append(((s,specweb[1]),(m,magick[1])))
		self.total += 1
		return ((s, sColor), (m, mColor))
			

	# def nbsAndImprovedEquivalence(self, test_color):
	# 	nbs = self.polychrome.getNbsIsccName(test_color)
	# 	nbs_improved = self.polychrome.getImprovedNbsIsccName(test_color)
	# 	if nbs[0] == nbs_improved[0]:
	# 		self.nbs_count += 1
	# 		if self.sameNameDiffHex(nbs, nbs_improved):
	# 			print "SNDHX: ", nbs, nbs_improved
	# 	else:
	# 		if (nbs[0],nbs_improved[0]) not in self.nbs_correlate and (nbs[0], nbs_improved[0]) not in self.nbs_correlate:
	# 			self.nbs_correlate.append(((nbs[0],nbs[1]), (nbs_improved[0],nbs_improved[1])))
	# 	self.total += 1
		
	def sameNameDiffHex(self, test_color_0, test_color_1):
		return test_color_0!=test_color_1

	def weight(self, nodeList):
		G = nx.Graph()
		for nodes in nodeList:
			print "node0", nodes[0]
			print "node1", nodes[1]
			n0 = nodes[0]
			# G.add_node(n0[0],{'color':n0[1]})
			n1 = nodes[1]
			# G.add_node(n1[0],{'color':n1[1]})
		    # if G.has_edge(n0,n1):   
		    #    G[n0][n1]['weight'] += 1
		    # else:
		    #    G.add_edge(n0,n1, weight=1)
		print "nodes: ", G.number_of_nodes()
		print G.nodes()
		print "edges: ", G.number_of_edges()
		print G.edges()
		nx.draw(G)
		plt.show()
		# nx.spring_layout(G)
		# plt.show()

	# def equiv(self, flags):
	# 	maps = []
	# 	if "magick" in flags:
	# 		maps.append(self.polychrome.getMagickName(test_color)[0])
	# 	if s
	# 	map0 = self.polychrome.getNbsIsccName(test_color)[0]
	# 	nbs_improved = self.polychrome.getImprovedNbsIsccName(test_color)[0]
	# 	if nbs == nbs_improved:
	# 		self.nbs_count += 1
	# 	else:
	# 		if (nbs,nbs_improved) not in self.nbs_correlate and (nbs, nbs_improved) not in self.nbs_correlate:
	# 			self.nbs_correlate.append((nbs, nbs_improved))
	# 	self.total += 1

	# def eval(self, action, map0_flag, map1_flag, end=65, interval=10):
	# 	self.polychrome = scd.Polychrome()
	# 	map0 = self.polychrome.createMap(map0_flag)
	# 	map1 = self.polychrome.createMap(map1_flag)
	# 	for r in range(1,end,interval):
	# 		for g in range(1,end,interval):
	# 			for b in range(1,end,interval):
	# 				if action == "name_equiv":

					# if action == "shade":
					# if action == "allnames":
					# if action == "hex_duplicates":
			




if __name__ == "__main__":
	pEval = PolychromeEval()
	nodeList = []
	G = nx.Graph()
	for r in range(1,65,10):
		for g in range(1,65,10):
			for b in range(1,65,10):
	# for r in range(1,256,10):
	# 	for g in range(1,256,10):
	# 		for b in range(1,256,10):
				rgb = (r, g, b)
				nodeList.append(pEval.specWebAndMagickEquivalence(rgb,G))
				# pEval.nbsAndImprovedEquivalence(rgb)
	for nodes in nodeList:
			n0 = nodes[0]
			n1 = nodes[1]
			# print n0,n1
			if G.has_edge(n0,n1):
				# print "has edge"
				# print G[n0]
				# print G[n0][n1]
				# print G[n0][n1]['weight']
				G[n0][n1]['weight'] += 1
			else:
			  	G.add_edge(n0, n1, {"weight":1})

	nx.draw(G)
	plt.show()
	
	# for item in pEval.nbs_correlate:
	# 	print item
	# pEval.weight(pEval.swm_correlate)