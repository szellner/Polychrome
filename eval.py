import polychrome
import re
import struct
import utils
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import gridspec
from multiprocessing import Pool
import itertools
import webcolors
import pygraphviz as pgv
from sklearn.cluster import KMeans
import argparse
import cv2


class PolychromeEval():

    def __init__(self):
        global poly
        poly = polychrome.Polychrome()
        self.swm_count = 0
        self.swm_correlate = []
        self.nbs_count = 0
        self.nbs_correlate = []
        self.total = 0
        self.nodecolors = {}

# how closely are two color names related? 

#look at named colors & relate


#look at rgb spectrum and use closestcolor 
    

    def intraMap(self, mapType, graph):
        test_map = poly.getMap(mapType)
        for rgb,name in test_map.colors.iteritems():
            name = ', '.join(name)
            graph.add_node(name, style='filled',fillcolor=utils.rgb2hex(rgb),fontcolor=utils.contrast(rgb),shape='rectangle')
            cc = poly.closestColor(rgb, test_map, intra=True)
            ccname = ', '.join(cc[2])
            # graph.add_node(ccname, style='filled',fillcolor=cc[1][1],fontcolor=utils.contrast(cc[1][0]),shape='rectangle')
            graph.add_edge(name,ccname)
        graph.layout()
        graph.draw('file.png')

    # def scatter(self, mapType):
    #     scatterMap = poly.getMap(mapType)

    #     colors = np.random.rand(N)
    #     area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses

    #     plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    #     plt.show()

    def kmeans(self):
        poly = polychrome.Polychrome()
        colormaps =  poly.getMaps()
        l = len(colormaps)
        gs = gridspec.GridSpec(l*2, 1)
        for n in range(0,l*2,2):
            ax = plt.subplot(gs[n, :])
            plt.axis('off')
            clt = KMeans(n_clusters=10)
            clt.fit(colormaps[n/2].colors.keys())
            hist = utils.centroid_histogram(clt)
            bar = utils.plot_colors(hist, clt.cluster_centers_)
            ax.set_title(colormaps[n/2].mapType,fontsize="small",)
            ax.imshow(bar)
            # plt.tight_layout()
        plt.show()      


    def specWebAndMagickEquivalence(self, test_color, graph):
        magick = poly.closestColor(test_color, poly.getMap("magick"))
        specweb = poly.closestColor(test_color, poly.getMap("specweb"))
        resene = poly.closestColor(test_color, poly.getMap("resene"))


        # mColor = magick[1][0]
        # sColor = specweb[1][0]

        # # Add the nodes with their respective rgb triplets as the node color
        # graph.add_node(mColor, {"node_color": mColor})
        # graph.add_node(sColor, {"node_color": sColor})
        # self.nodecolors[mColor] = mColor
        # self.nodecolors[sColor] = sColor
        # # # Weight the edges appropriately
        # utils.weight(graph, mColor, sColor)
        # for m in magick[2]:


        # if not graph.has_edge(node0, node1):
        # graph.add_edge(node0, node1, {"weight": 1})
        # else:
        # graph[node0][node1]["weight"] += 1
        mName = ', '.join(magick[2])
        sName = ', '.join(specweb[2])
        rName = ', '.join(resene[2])

        graph.add_node(mName, style='filled',fillcolor=magick[1][1],fontcolor=utils.contrast(magick[1][0]),shape='rectangle')
        graph.add_node(sName, style='filled',fillcolor=specweb[1][1],fontcolor=utils.contrast(specweb[1][0]),shape='circle')
        # graph.add_node(rName, style='filled',fillcolor=resene[1][1], fontcolor=utils.contrast(resene[1][0]),shape='rectangle')
        # graph.add_edge(sName,rName)
        # graph.add_edge(mName,rName)
        graph.layout()
        # graph.draw('file.png',prog='circo')
        graph.draw('file.png',prog="neato")

        # print graph.number_of_nodes()
        # if s == m:
        # if magick == specweb:
        #     self.swm_count += 1
        #     # print self.sameNameDiffHex(specweb,magick)
        #     # print s, sColor
        #     # print m, mColor

        #     print "%s and %s are the SAME" % (magick, specweb)

        #     # nx.draw_networkx_nodes(graph,graph.pos, nodelist=[s,m],node_color=[specweb[1],magick[1]])
        #     # self.swm_correlate.append(((s,specweb[1]),(m,magick[1])))
        # self.total += 1
        # weighthisshit()
        return magick, specweb

    # def nbsAndImprovedEquivalence(self, test_color):
    #   nbs = self.poly.getNbsIsccName(test_color)
    #   nbs_improved = self.poly.getImprovedNbsIsccName(test_color)
    #   if nbs[0] == nbs_improved[0]:
    #       self.nbs_count += 1
    #       if self.sameNameDiffHex(nbs, nbs_improved):
    #           print "SNDHX: ", nbs, nbs_improved
    #   else:
    #       if (nbs[0],nbs_improved[0]) not in self.nbs_correlate and (nbs[0], nbs_improved[0]) not in self.nbs_correlate:
    #           self.nbs_correlate.append(((nbs[0],nbs[1]), (nbs_improved[0],nbs_improved[1])))
    #   self.total += 1

    def graphviz(self):
        H=pgv.AGraph()
        H.add_node('a', style='filled',fillcolor='#120235')
        H.layout()
        H.draw('file.png')

        # g1 = gv.Graph(format='svg')

        # g1.node('A')

        # g1.node('B')
        # g1.edge('A', 'B')
        # print(g1.source)
        # filename = g1.render(filename='img/g1', view=True)
        # print filename

    def sameNameDiffHex(self, test_color_0, test_color_1):
        return test_color_0 != test_color_1

    # def weight(self, nodeList):
        G = nx.Graph()
        # for nodes in nodeList:
        #     print "node0", nodes[0]
        #     print "node1", nodes[1]
        #     n0 = nodes[0]
        #     # G.add_node(n0[0],{'color':n0[1]})
        #     n1 = nodes[1]
        # G.add_node(n1[0],{'color':n1[1]})
        # if G.has_edge(n0,n1):
        #    G[n0][n1]['weight'] += 1
        # else:
        #    G.add_edge(n0,n1, weight=1)
        print "nodes: ", G.number_of_nodes()
        # print G.nodes()
        print "edges: ", G.number_of_edges()
        # print G.edges()
        nx.draw(G)
        plt.show()
        nx.spring_layout(G)
        plt.show()

    # def equiv(self, flags):
    #   maps = []
    #   if "magick" in flags:
    #       maps.append(self.poly.getMagickName(test_color)[0])
    #   if s
    #   map0 = self.poly.getNbsIsccName(test_color)[0]
    #   nbs_improved = self.poly.getImprovedNbsIsccName(test_color)[0]
    #   if nbs == nbs_improved:
    #       self.nbs_count += 1
    #   else:
    #       if (nbs,nbs_improved) not in self.nbs_correlate and (nbs, nbs_improved) not in self.nbs_correlate:
    #           self.nbs_correlate.append((nbs, nbs_improved))
    #   self.total += 1

    # def eval(self, action, map0_flag, map1_flag, end=65, interval=10):
    #   self.poly = scd.Polychrome()
    #   map0 = self.poly.createMap(map0_flag)
    #   map1 = self.poly.createMap(map1_flag)
    #   for r in range(1,end,interval):
    #       for g in range(1,end,interval):
    #           for b in range(1,end,interval):
    #               if action == "name_equiv":

        # if action == "shade":
        # if action == "allnames":
        # if action == "hex_duplicates":


if __name__ == "__main__":
    pEval = PolychromeEval()
    # nodeList = []
    G = nx.Graph()
    H=pgv.AGraph()
    # print G.edges
    # for r in range(240, 256, 5):
    #     for g in range(240, 256, 5):
    #         for b in range(240, 256, 5):
    # #             # for r in range(1,256,10):
    # #             #   for g in range(1,256,10):
    # #             #       for b in range(1,256,10):
    #             rgb = (r, g, b)
    #             print pEval.specWebAndMagickEquivalence(rgb, H)
                # nodeList.append(pEval.specWebAndMagickEquivalence(rgb, G))
    #     # pEval.nbsAndImprovedEquivalence(rgb)
    # print utils.getEdgeWeights(G)
    # # print plt.cm.Blues
    # nx.draw(G, node_color=(0.4, 0.2, 0.7))
    pEval.kmeans()
    # plt.show()
    # pEval.intraMap("resene",H)
    # for item in pEval.nbs_correlate:
    #   print item
    # pEval.weight(pEval.swm_correlate)
