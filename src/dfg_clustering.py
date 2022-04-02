#!/usr/bin/env python
import sys
import os
import os.path
import shutil
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re
#from antlr4 import tree

import numpy as np
import networkx as nx

from sklearn.cluster import SpectralClustering
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
        
def main(dfg_xml, no_clusters, affinity_, no_init,number_of_cluster_rows_in_cgra):
    
    #Create networkx directed graph to represent data flow graph by passing dfg_xml file

    #https://www.datacamp.com/community/tutorials/python-xml-elementtree
   
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(dfg_xml, parser=parser)
    root = tree.getroot()

    
    DFG = nx.DiGraph()
    backedge_list = []

    for nodes in root:
        for nodeelm in nodes:
            if nodeelm.tag == 'Outputs':
                for outputs in nodeelm:
                    DFG.add_edge(nodes.attrib["idx"], outputs.attrib["idx"])
                    if outputs.attrib["nextiter"] == "1":
                        e = (nodes.attrib["idx"], outputs.attrib["idx"])
                        backedge_list.append(e)
            
            if nodeelm.tag == 'RecParents':
                for recparents in nodeelm:
                    e = (nodes.attrib["idx"], recparents.attrib["idx"])
                    backedge_list.append(e)

    np.random.seed(1)

    print(DFG.number_of_nodes())
    
    #Create adjacency matrix of DFG
    adj_mat_dfg = nx.to_numpy_matrix(DFG)

    print('no_clusters affinity no_init')
    print(no_clusters, affinity_, no_init)

    #Spectral clustering from scikit learn
    print('spectral dfg clustering')
    scdfg = SpectralClustering(int(no_clusters), affinity=str(affinity_), n_init=int(no_init), random_state=0)
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
    for c in range(0,int(no_clusters)):
            print(str(c) + ':' + str(cluster_ids.count(c)))
            cluster_id_node_count.insert(c, cluster_ids.count(c))

    #Modify the clustering results 
    #the nodes in recurrence cycle are merged into one cluster

    print('determine recurrence cycles')
    backedge_recset_list = []
             
    for e in backedge_list:
        be_parent = e[0]
        print('Backedge')
        print(e)
        print()
        q = Queue()
        rec_set = set()
        q.put(be_parent)
        rec_set.add(be_parent)
        while (not q.empty()):
            node = q.get()
            for parent in DFG.predecessors(node):
                if not ((parent,node) in backedge_list):#not a backedge
                    #print(parent)
                    q.put(parent)
                    rec_set.add(parent)
        backedge_recset_list.append(rec_set)
        #print(rec_set)
    for recset in backedge_recset_list:
        print(recset)
    print(backedge_recset_list)
    
    #merge the recurrence sets which share common nodes
    G = to_graph(backedge_recset_list)
    cluster_ids = []
    print('Connected components')
    cc = connected_components(G)
    
    print('Modify the cluster id of nodes in recurrence cycles')
    
    #change the cluster of each merged rec set
    for comp in cc:
        print('Connected component: (Merged Rec Sets)')
        print(comp)
        max_count = 0
        max_count_cluster = -1
        cluster_ids = []
        for node in comp:
            cluster_ids.append(nodeid_clusterlabel_dict[node])#
        print('Cluster: Count')
        for c in range(0,int(no_clusters)):
            print(str(c) + ':' + str(cluster_ids.count(c)))
            if max_count < cluster_ids.count(c):
                #if len(comp)+cluster_id_node_count[c] < DFG.number_of_nodes()/int(number_of_cluster_rows_in_cgra):
                max_count =cluster_ids.count(c)
                max_count_cluster = c
        # if max_count_cluster == -1:# number of nodes in merged rec cycles are higher than the number of nodes in row
        #     max_count =0
        #     for c in range(0,int(no_clusters)):
        #         if max_count < cluster_ids.count(c):
        #             max_count =cluster_ids.count(c)
        #             max_count_cluster = c

        print('Max count cluster:'+str(max_count_cluster))
        print('Modify the cluster id of recurrence sets:')
        #for node in comp:
            #nodeid_clusterlabel_dict[node] = max_count_cluster
            #print('Modified Node:'+str(node)+',cls:'+str(max_count_cluster))
            
        
    print()
    #print(cc)
    print()
            


    #Write dfg clustering result
    clustering_outcome = "dfg_clustering_result.txt"
    i=0
    with open(clustering_outcome, "w") as f:
        for i in range(0, DFG.number_of_nodes()):
            #node_id = nodes.attrib["idx"]
            #print(node_list[i],scdfg.labels_[i]) 
            f.write(str(node_list[i]) + '\t' + str(nodeid_clusterlabel_dict[node_list[i]]) + '\n')
            #i=i+1
    f.close()
    
    #Draw dfg clustering result
    #pydot graph
    #https://pypi.org/project/pydot/
    pydot_dfg = pydot.Dot('DFG',graph_type='graph')
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
    #https://graphviz.org/doc/info/attrs.html
    
    #print("adding nodes to colored dot dfg")
    for nodes in DFG.nodes:
        #print(colordict[scdfg.labels_[i]])
        #pydot_dfg.add_node(pydot.Node(nodes, fontcolor="white", style="filled", fillcolor=colordict[scdfg.labels_[i]]))
        pydot_dfg.add_node(pydot.Node(nodes, fontcolor="white", style="filled", fillcolor=colordict[nodeid_clusterlabel_dict[node_list[i]]]))
        i = i+1
    
    
    #print("adding edges to colored dot dfg")    
    for edges in DFG.edges:
        pydot_dfg.add_edge(pydot.Edge(edges[0],edges[1]))
    
    
    pydot_dfg.write_png('dfg_clustering_result.png')
    
    print(nodeid_clusterlabel_dict)

    #Write inter cluster edge list  
    #print("Inter cluster edges:")
    total_edges = 0
    inter_cluster_edges = 0
    with open("inter_cluster_edges.txt", "w") as f:
        for edges in DFG.edges:
            total_edges = total_edges + 1
            if nodeid_clusterlabel_dict[edges[0]] != nodeid_clusterlabel_dict[edges[1]]:
                f.write(str(edges[0]) + '\t' + str(edges[1]) + '\n')
                inter_cluster_edges = inter_cluster_edges + 1
    f.close()
    
    
    with open("all_edges.txt", "w") as f:
        for edges in DFG.edges:
            f.write(str(edges[0]) + '\t' + str(edges[1]) + '\n')
    f.close()


    #Draw cluster dependency graph   
    CLUS_DFG = nx.DiGraph()
    for i in range(0, int(no_clusters)):
        CLUS_DFG.add_node(i, label = 0, color=colordict[i])
        
    for i in range(0, DFG.number_of_nodes()): 
        CLUS_DFG.nodes[nodeid_clusterlabel_dict[node_list[i]]]["label"] = CLUS_DFG.nodes[nodeid_clusterlabel_dict[node_list[i]]]["label"] + 1
    
    #print("Inter cluster edges:")
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
    print("Total nodes:", DFG.number_of_nodes())        
  
    #https://graphviz.org/doc/info/attrs.html
    
    write_dot(CLUS_DFG,'cdfg.dot')
    
    # Number of nodes in each cluster
    print("Number of nodes in each cluster:")    
    with open("number_of_nodes_in_each_cluster.txt", "w") as f:
        for i in range(0,int(no_clusters)): 
            print(i,CLUS_DFG.nodes[i]['label'],(CLUS_DFG.nodes[i]['label']/DFG.number_of_nodes())*100)
            f.write(str(i) + '\t'+ str(CLUS_DFG.nodes[i]['label']) + '\t' +str((CLUS_DFG.nodes[i]['label']/DFG.number_of_nodes())*100) + '\n')
    f.close()
    nx.write_gexf(CLUS_DFG, 'cdfg.gexf')
    #https://www.programcreek.com/python/example/105084/networkx.drawing.nx_agraph.graphviz_layout
    
    
  
def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
    dfg_xml = sys.argv[1]
    no_clusters = sys.argv[2]
    affinity_ = sys.argv[3]
    no_init = sys.argv[4]
    number_of_cluster_rows_in_cgra = sys.argv[5]
    main(dfg_xml, no_clusters, affinity_, no_init,number_of_cluster_rows_in_cgra)
