#!/usr/bin/env python
import sys
import os
import os.path
import shutil
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re
import glob
#from antlr4 import tree

import numpy as np
import networkx as nx
import metis

from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
# from sklearn.cluster import BisectingKMeans
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
from networkx.algorithms.components.connected import connected_components
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_pydot import to_pydot
from sklearn.cluster._agglomerative import AgglomerativeClustering
import pydot
from queue import Queue
from _ast import If
from networkx.algorithms.components.connected import connected_components
############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script


#https://stackoverflow.com/questions/4842613/merge-lists-that-share-common-elements
def to_graph(l):
    G = nx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        G.add_nodes_from(part)
        # it also imlies a number of edges:
        G.add_edges_from(to_edges(part))
    return G

def to_edges(l):
    """ 
        treat `l` as a Graph and returns it's edges 
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current  
        
def main(application, clus_algo, min_no_clusters, max_no_clusters):

    
    dfg_xml = glob.glob('../data/morpher_dfgs/'+application+'/*.xml')[0]
    #https://www.datacamp.com/community/tutorials/python-xml-elementtree
    #tree = ET.fromstring(xml_name)
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(dfg_xml, parser=parser)
    root = tree.getroot()
    #print(root.tag)
    #print(root.attrib)
    
    DFG = nx.DiGraph()
    backedge_list = []

    for nodes in root:
        #print(nodes.tag, nodes.attrib)
        #print(nodes.attrib["idx"])
        for nodeelm in nodes:
            #print(nodeelm.tag, nodeelm.attrib)
            if nodeelm.tag == 'Outputs':
                for outputs in nodeelm:
                    #print(outputs.tag, outputs.attrib)
                    DFG.add_edge(nodes.attrib["idx"], outputs.attrib["idx"])
                    if outputs.attrib["nextiter"] == "1":
                        e = (nodes.attrib["idx"], outputs.attrib["idx"])
                        backedge_list.append(e)
            
            if nodeelm.tag == 'RecParents':
                for recparents in nodeelm:
                    # print('backedge rec')
                    # print(nodes.attrib["idx"], recparents.attrib["idx"])
                    e = (nodes.attrib["idx"], recparents.attrib["idx"])
                    backedge_list.append(e)

    np.random.seed(1)

    print(DFG.number_of_nodes())
    
    adj_mat_dfg = nx.to_numpy_matrix(DFG)
    numclusters_max_percentage = {}
    numclusters_interclusedges = {}
    numclusters_imbalance_factor = {}
    # Cluster
    for n in range(int(min_no_clusters),int(max_no_clusters)):
        if int(n)!=9 and int(n)!=16 :
            continue
        #print('no_clusters affinity no_init')
        #print(n, affinity_, no_init)
        if clus_algo == 'spectral':
            print('spectral dfg clustering')
            #scdfg = SpectralClustering(int(n), affinity=str(affinity_), n_init=int(no_init), random_state=0)
            scdfg = SpectralClustering(int(n), affinity='precomputed', n_init=100, random_state=0)
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)#madgwick
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)//aes
            #scdfg = AgglomerativeClustering(7, affinity='precomputed', linkage='average')
            #https://stackoverflow.com/questions/46258657/spectral-clustering-a-graph-in-python
            #https://ptrckprry.com/course/ssd/lecture/community.html
            scdfg.fit(adj_mat_dfg)
            node_list = list(DFG)
            nodeid_clusterlabel_dict = {}
            cluster_ids = []
            cluster_id_node_count = []
            for i in range(0, DFG.number_of_nodes()):
                nodeid_clusterlabel_dict[node_list[i]] = scdfg.labels_[i]
                cluster_ids.append(scdfg.labels_[i])
            for c in range(0,int(n)):
                cluster_id_node_count.insert(c, cluster_ids.count(c))
        if clus_algo == 'agglo':
            print('Agglomerative dfg clustering')
            #scdfg = SpectralClustering(int(n), affinity=str(affinity_), n_init=int(no_init), random_state=0)
            # scdfg = SpectralClustering(int(n), affinity='precomputed', n_init=100, random_state=0)
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)#madgwick
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)//aes
            scdfg = AgglomerativeClustering(int(n), affinity='precomputed', linkage='average')
            #https://stackoverflow.com/questions/46258657/spectral-clustering-a-graph-in-python
            #https://ptrckprry.com/course/ssd/lecture/community.html
            scdfg.fit(adj_mat_dfg)
            node_list = list(DFG)
            nodeid_clusterlabel_dict = {}
            cluster_ids = []
            cluster_id_node_count = []
            for i in range(0, DFG.number_of_nodes()):
                nodeid_clusterlabel_dict[node_list[i]] = scdfg.labels_[i]
                cluster_ids.append(scdfg.labels_[i])
            for c in range(0,int(n)):
                cluster_id_node_count.insert(c, cluster_ids.count(c))
        if clus_algo == 'dbscan':
            print('dbscan dfg clustering')
            #scdfg = SpectralClustering(int(n), affinity=str(affinity_), n_init=int(no_init), random_state=0)
            # scdfg = SpectralClustering(int(n), affinity='precomputed', n_init=100, random_state=0)
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)#madgwick
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)//aes
            scdfg = AgglomerativeClustering(int(n), affinity='precomputed', linkage='average')
            db = DBSCAN(eps=0.3, min_samples=10).fit(adj_mat_dfg)# Number of clusters in labels, ignoring noise if present.
            n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
            n_noise_ = list(db.labels_).count(-1)
            
            print("Estimated number of clusters: %d" % n_clusters_)
            print("Estimated number of noise points: %d" % n_noise_)
            exit()
            #https://stackoverflow.com/questions/46258657/spectral-clustering-a-graph-in-python
            #https://ptrckprry.com/course/ssd/lecture/community.html
            scdfg.fit(adj_mat_dfg)
            node_list = list(DFG)
            nodeid_clusterlabel_dict = {}
            cluster_ids = []
            cluster_id_node_count = []
            for i in range(0, DFG.number_of_nodes()):
                nodeid_clusterlabel_dict[node_list[i]] = db.labels_[i]
                cluster_ids.append(db.labels_[i])
            for c in range(0,int(n)):
                cluster_id_node_count.insert(c, cluster_ids.count(c))
        elif clus_algo == 'kmeans':
            print('kmeans dfg clustering')
            #scdfg = SpectralClustering(int(n), affinity=str(affinity_), n_init=int(no_init), random_state=0)
            # scdfg = SpectralClustering(int(n), affinity='precomputed', n_init=100, random_state=0)
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)#madgwick
            #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)//aes
            kmeans = KMeans(int(n), random_state=0).fit(nx.to_numpy_array(DFG))
            #https://stackoverflow.com/questions/46258657/spectral-clustering-a-graph-in-python
            #https://ptrckprry.com/course/ssd/lecture/community.html
            # scdfg.fit(adj_mat_dfg)
            node_list = list(DFG)
            nodeid_clusterlabel_dict = {}
            cluster_ids = []
            cluster_id_node_count = []
            for i in range(0, DFG.number_of_nodes()):
                nodeid_clusterlabel_dict[node_list[i]] = kmeans.labels_[i]
                cluster_ids.append(kmeans.labels_[i])
            for c in range(0,int(n)):
                cluster_id_node_count.insert(c, cluster_ids.count(c))         
        elif clus_algo == 'metis':
           print('metis dfg clustering')
           (edgecuts, parts) = metis.part_graph(DFG, int(n) , objtype = 'vol')#, recursive = False, contig = False)
           # for i, p in enumerate(parts):
           #     print(i,p)
           # for i in parts:
           #     print(i)
           # exit()
           node_list = list(DFG)
           nodeid_clusterlabel_dict = {}
           cluster_ids = []
           cluster_id_node_count = []
           for i in range(0, DFG.number_of_nodes()):
               nodeid_clusterlabel_dict[node_list[i]] = parts[i]
               cluster_ids.append(parts[i])
           for c in range(0,int(n)):
                   # print(str(c) + ':' + str(cluster_ids.count(c)))
                   cluster_id_node_count.insert(c, cluster_ids.count(c))
    
        cluster_ids = []

    
            

    
    
    #pydot graph
    #https://pypi.org/project/pydot/
    #pydot_dfg = pydot.Dot('DFG',graph_type='graph')
        colordict = {
        0:'red',
        1:'green',
        2:'blue',
        3:'yellow',
        4:'cyan',
        5:'purple',
        6:'orange',
        7:'brown',
        8:'magenta',
        9:'turquoise',
        10:'azure',
        11:'black',
        12:'sienna',
        13:'silver',
        14:'gold',
        15:'lightgray',
        16:'orange',
        17:'brown',
        18:'magenta',
        19:'turquoise',
        20:'azure',
        21:'black',
        22:'sienna',
        23:'silver',
        24:'gold',
        25:'lightgray',
        26:'orange',
        27:'brown',
        28:'magenta',
        29:'turquoise',
        30:'azure',
        31:'black',
        32:'sienna',
        33:'silver',
        34:'gold',
        35:'lightgray'
    
        }
        i=0
    
        total_edges = 0
        inter_cluster_edges = 0

        for edges in DFG.edges:
            total_edges = total_edges + 1
            if nodeid_clusterlabel_dict[edges[0]] != nodeid_clusterlabel_dict[edges[1]]:
            #print(edges[0],edges[1])
            #f.write(str(edges[0]) + '\t' + str(edges[1]) + '\n')
                inter_cluster_edges = inter_cluster_edges + 1
   
    
        CLUS_DFG = nx.DiGraph()
        for i in range(0, int(n)):
            CLUS_DFG.add_node(i, label = 0, color=colordict[i])
        
        for i in range(0, DFG.number_of_nodes()): 
            CLUS_DFG.nodes[nodeid_clusterlabel_dict[node_list[i]]]["label"] = CLUS_DFG.nodes[nodeid_clusterlabel_dict[node_list[i]]]["label"] + 1
    

        total_edges = 0
        inter_cluster_edges = 0
        for edges in DFG.edges:
            total_edges = total_edges + 1
            if nodeid_clusterlabel_dict[edges[0]] != nodeid_clusterlabel_dict[edges[1]]:
                if CLUS_DFG.has_edge(nodeid_clusterlabel_dict[edges[0]], nodeid_clusterlabel_dict[edges[1]]):
                    CLUS_DFG[nodeid_clusterlabel_dict[edges[0]]][nodeid_clusterlabel_dict[edges[1]]]['label'] = CLUS_DFG[nodeid_clusterlabel_dict[edges[0]]][nodeid_clusterlabel_dict[edges[1]]]['label'] + 1
                    inter_cluster_edges = inter_cluster_edges + 1
                else:
                    CLUS_DFG.add_edge(nodeid_clusterlabel_dict[edges[0]], nodeid_clusterlabel_dict[edges[1]], label=1)
                    #print(nodeid_clusterlabel_dict[edges[0]], nodeid_clusterlabel_dict[edges[1]])
                    inter_cluster_edges = inter_cluster_edges + 1
                
        print("Total edges:",total_edges)       
        print("Inter cluster edges:",inter_cluster_edges)
        numclusters_interclusedges[n] = inter_cluster_edges
        print("Total nodes:", DFG.number_of_nodes())        
  
   
        print("Number of nodes in each cluster:")    
        max_percentage = 0;
        for i in range(0,int(n)): 
            percentage = CLUS_DFG.nodes[i]['label']/DFG.number_of_nodes()
            print(i,CLUS_DFG.nodes[i]['label'],(CLUS_DFG.nodes[i]['label']/DFG.number_of_nodes())*100)
            if max_percentage <  percentage:
                max_percentage = percentage
        numclusters_max_percentage[n] = max_percentage
        print("max percentage:", max_percentage)
        print()
        imbalance_factor = 0;
        min_cluster_size = 1000;
        max_cluster_size = 0;
        for i in range(0,int(n)): 
            if min_cluster_size >  CLUS_DFG.nodes[i]['label']:
                min_cluster_size = CLUS_DFG.nodes[i]['label']
            if max_cluster_size <  CLUS_DFG.nodes[i]['label']:
                max_cluster_size = CLUS_DFG.nodes[i]['label']
        imbalance_factor = (max_cluster_size-min_cluster_size)/DFG.number_of_nodes()
        numclusters_imbalance_factor[n] = imbalance_factor
        print("min cluster size:", min_cluster_size)
        print("max cluster size:", max_cluster_size)
        print("imbalance_factor:", imbalance_factor)
        print()
    
    print("numclusters_max_percentage:")
    print(numclusters_max_percentage)
    sorted_numclusters_max_percentage = sorted(numclusters_max_percentage.items(), key = lambda x:x[1])
    print()

    print("sorted_numclusters_max_percentage:")
    print(sorted_numclusters_max_percentage)
    print()
    
    sorted_numclusters_interclusedges = sorted(numclusters_interclusedges.items(), key = lambda x:x[1])
    print("sorted_numclusters_interclusedges:")
    print(sorted_numclusters_interclusedges)
    print()
    
    sorted_numclusters_imbalancefactor = sorted(numclusters_imbalance_factor.items(), key = lambda x:x[1])
    print("sorted_numclusters_imbalancefactor:")
    print(sorted_numclusters_imbalancefactor)
    print()

    
    
  
def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
    application = sys.argv[1]
    clus_algo = sys.argv[2]
    min_no_clusters = sys.argv[3]
    max_no_clusters = sys.argv[4]
    main(application, clus_algo, min_no_clusters, max_no_clusters)
