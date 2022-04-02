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
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_pydot import to_pydot
from sklearn.cluster._agglomerative import AgglomerativeClustering
import pydot
from _ast import If, Assign

import pygraphviz as gz
#from pygraphviz import Digraph
import graphviz
import math
############################################

import gurobipy as gp
from gurobipy import GRB
from networkx.classes.function import neighbors


def main(C1_init_, C2_init_, cgra_cluster_r, cgra_cluster_c):
    try:
        clus_dfg = nx.read_gexf('cdfg.gexf')
        
        num_of_columns = int(cgra_cluster_c)
        num_of_rows = int(cgra_cluster_r)
        row  = 0
        number_of_cgra_clusters = num_of_columns*num_of_rows
        num_cluster_nodes =  clus_dfg.number_of_nodes()
        print(clus_dfg.number_of_nodes())
        print(clus_dfg.number_of_edges())
        
            
        num_of_dfg_nodes = 0
        
        
        num_cluster_nodes =  clus_dfg.number_of_nodes()
        print("Number of cluster nodes:",clus_dfg.number_of_nodes())
        print("Number of cluster edges:",clus_dfg.number_of_edges())
        
    
        cluster_node_to_dfg_nodes = []
        i = 0
        min_dfg_nodes = 1000000
        print("DFG nodes in each cluster:")
        for nodes in clus_dfg.nodes:
            #print(clus_dfg.nodes[nodes]["label"])
            num_of_dfg_nodes = num_of_dfg_nodes + int(clus_dfg.nodes[nodes]["label"])
            cluster_node_to_dfg_nodes.insert(i,int(clus_dfg.nodes[nodes]["label"]))
            print(i,int(clus_dfg.nodes[nodes]["label"]))
            if min_dfg_nodes > int(clus_dfg.nodes[nodes]["label"]):
                min_dfg_nodes = int(clus_dfg.nodes[nodes]["label"])
            i = i+1
            
            #num_of_dfg_nodes = num_of_dfg_nodes + int(clus_dfg.nodes[i]['label'])
            
        num_of_dfg_nodes_per_cgra_cluster = int(num_of_dfg_nodes/number_of_cgra_clusters)
        print("Number of dfg nodes:",num_of_dfg_nodes)
        print("Number of cgra clusters:",number_of_cgra_clusters)
        print("Number of dfg nodes per cgra cluster:",num_of_dfg_nodes_per_cgra_cluster)
        
    
    
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
        #Column wise scattering
        C1_init = int(C1_init_)
        C2_init = int(C2_init_)
        assigned_row = []
        while(True):
            for i in range(0,num_cluster_nodes):
                assigned_row.insert(i, -1)
            while (row < num_of_rows):
                C1 = C1_init;
                n = 100000;
                C2 = C2_init;
            
                # Create a new model
                m = gp.Model("mip1"+str(C1_init)+str(C2_init))
                
                v =[]
                cl_dfg = []
                for i in range(0,num_cluster_nodes):
                    if assigned_row[i] == -1 :
                        v.insert(i,m.addVar(vtype=GRB.BINARY, name="v%d" % (i)))
                        cl_dfg.insert(i,cluster_node_to_dfg_nodes[i])
                m.update()
                
                
                #Epsilon = num_cluster_nodes/num_of_rows;
                Epsilon = int(num_of_dfg_nodes/num_of_rows)
                
                expr1= gp.LinExpr()
                #expr1 = gp.quicksum(v) - Epsilon
                for i in range(0,len(v)):
                    expr1 = expr1 + v[i]*cl_dfg[i]
                expr1 = expr1 - Epsilon
                print("Objective 9:",expr1)
                
                #gurobi doesn't support abs in objective. How to convert abs to supported format? Follow the link
                #http://lpsolve.sourceforge.net/5.1/absolute.htm
                #https://support.gurobi.com/hc/en-us/community/posts/360074428532-How-to-handle-absolute-value-in-objective-function-
                x_ = m.addVar(name = 'x_')
                
                m.setObjective(x_ , GRB.MINIMIZE)
                m.addConstr(expr1 <= x_)
                m.addConstr(-expr1 <= x_)
                #m.setObjective(gp.abs_(sum(Vik1[i] for i in range(0,num_cluster_nodes)) - Epsilon) , GRB.MINIMIZE)
                
                found_solution = False
                print("initial constr")
                print(m.getConstrs())
                num_of_constr = 2;
                
                while (found_solution!= True):
                    num_of_constr = 2;
                    for nodes in clus_dfg.nodes:
                        #print(nodes)
                        node_id = int(nodes)
                        print("Node ID:",node_id)
                        if assigned_row[node_id] == -1:
                            index_list = []
                            #index_list.append(nodes)
                            degree = 0
                            for neighbors in clus_dfg.neighbors(nodes):
                                #print(neighbors)
                                neighbor_id = int(neighbors)
                                if assigned_row[neighbor_id] == -1 :
                                    index_list.append(neighbors)
                                    index_list.append(nodes)
                                    degree = degree + 1
                            #print(index_list)
                            for i in range(0,len(index_list)):
                                index_list[i] = int(index_list[i])
                        
                        #print(v[0])
                            print(index_list)
                            print(v)
                            #print(v[0])
                            #print(m.getVarByName("v6"))
                            #print(m.getVarByName("v9"))
                            if degree > 1:
                                print("Constraint 12:", sum(m.getVarByName(str("v"+str(i))) for i in index_list) <= C1 + n*m.getVarByName(str("v"+str(node_id))) )
                                m.addConstr(sum(m.getVarByName(str("v"+str(i))) for i in index_list) <= C1 + n*m.getVarByName(str("v"+str(node_id))) )
                                print("Constraint 13:", sum(m.getVarByName(str("v"+str(i))) for i in index_list) >= 2*degree - C2 - n*(1-m.getVarByName(str("v"+str(node_id)))  ))
                                m.addConstr(sum(m.getVarByName(str("v"+str(i))) for i in index_list) >= 2*degree - C2 - n*(1-m.getVarByName(str("v"+str(node_id)))  ))
                                num_of_constr = num_of_constr+2
                                print("")
                    
                    m.optimize()
                
                    #print(clus_dfg.neighbors(nodes))
                    
                    #print("V0",v[0])
                    for var in m.getVars():
                        #print('%s %g' % (var.varName, var.x))
                        if var.x == 1 :
                            found_solution = True
                            
                    if found_solution == True:
                        print("Found a solution at C1,C2  : ", C1,C2)
                        for var in m.getVars():
                            print('%s %g' % (var.varName, var.x))
                            if str(var.varName[0]) =='v':
                                if var.x == 1:
                                    print(int(var.varName[1:]))
                                    assigned_row[int(var.varName[1:])] = row
                        row = row + 1
                    print('Obj: %g' % m.objVal)
                    print("Constraint List:",m.getConstrs())
                    print("Number of Constraints:",num_of_constr)
                    m.remove(m.getConstrs()[2:(num_of_constr)])
                    m.update()
                    #print(m.getConstrs())
                    C1 = C1+1
                    C2 = C2+1
            
            for i in range(0,num_cluster_nodes):
                print("node,row",i,assigned_row[i])
                if (assigned_row[i]==-1):
                    assigned_row[i]= num_of_rows-1
                
            #row wise scattering
            
            m = gp.Model("mip2"+str(C1_init)+str(C2_init))
            
            v =[]
            cid = []
            j=0
            for i in range(0,num_cluster_nodes):
                for c in range(1,num_of_columns+1):
                    v.insert(j,m.addVar(vtype=GRB.BINARY, name="v%d%d" % (i,c)))
                    cid.insert(j,cid)
                    j=j+1
            m.update()
            #print(v)
            #for i in range(0,num_cluster_nodes*num_of_columns):
            #    print((i%num_of_columns+1)) 
            #    print(v[i])
            
            #14 maximize number of unexecuted column
            #objective = gp.quicksum([v[i]*(i%num_of_columns+1) for i in range(0,num_cluster_nodes*num_of_columns)]) 
            #print(objective)
            #m.setObjective(objective , GRB.MINIMIZE)
            
            # objective to minimize edge distance
            objective = gp.LinExpr()
            for edges in clus_dfg.edges:
                weight = int(clus_dfg[edges[0]][edges[1]]["label"])
                for c in range(1,num_of_columns+1):
                    #print(m.getVarByName(str("v"+str(edges[0])+str(c))) == m.getVarByName(str("v"+str(edges[1])+str(c))))
                    objective = objective + weight*c*(m.getVarByName(str("v"+str(edges[0])+str(c))) - m.getVarByName(str("v"+str(edges[1])+str(c))))
            
            print("Objective 14:",objective)
            #m.setObjective(objective , GRB.MINIMIZE)
            x_ = m.addVar(name = 'x_')
                
            m.setObjective(x_ , GRB.MINIMIZE)
            m.addConstr(objective <= x_)
            m.addConstr(-objective <= x_)
            
            #15 
            print("how many cgra clusters one node should map?")
            constr15 = gp.LinExpr()
            #m.addConstr()
            for i in range(0,num_cluster_nodes):
                #if int(round(cluster_node_to_dfg_nodes[i]/num_of_dfg_nodes_per_cgra_cluster)) > num_of_columns:
                    #constr15 = sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) == num_of_columns 
                #else:
                    #constr15 = sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) == int(round(cluster_node_to_dfg_nodes[i]/num_of_dfg_nodes_per_cgra_cluster)) 
                
                
                if int(math.ceil(cluster_node_to_dfg_nodes[i]/num_of_dfg_nodes_per_cgra_cluster)) > num_of_columns:
                    constr15 = sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) == num_of_columns 
                else:
                    constr15 = sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) == int(math.ceil(cluster_node_to_dfg_nodes[i]/num_of_dfg_nodes_per_cgra_cluster)) 
                m.addConstr(constr15)
                print("Constraint 15:",constr15)#1)
                #print("Constraint 15:",sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) >= 1)#1)
                #m.addConstr(sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) >= 1 )
            #16 
            print("how many nodes one cgra cluster can have?")
            constr16 = gp.LinExpr()
            for c in range(1,num_of_columns+1):
                for r in range(0,num_of_rows):
                    index_list=[]
                    for i in range(0,num_cluster_nodes):
                        if assigned_row[i]==r:
                            index_list.append(i)
                    #m.addConstr(sum(m.getVarByName(str("v"+str(k)+str(c))) for k in index_list) <= 2)
                    constr16=sum(m.getVarByName(str("v"+str(k)+str(c))) for k in index_list) >= 1
                    m.addConstr(constr16)
                    print("Constraint 16:",constr16)
            #17       
            for edges in clus_dfg.edges:
                #print(clus_dfg[edges[0]][edges[1]]["label"])
                #print(edges[0],edges[1])
                weight = int(clus_dfg[edges[0]][edges[1]]["label"])
                if weight > 4:
                    for c in range(1,num_of_columns+1):
                        pass
                        #print(m.getVarByName(str("v"+str(edges[0])+str(c))) == m.getVarByName(str("v"+str(edges[1])+str(c))))
                        #m.addConstr(m.getVarByName(str("v"+str(edges[0])+str(c))) == m.getVarByName(str("v"+str(edges[1])+str(c))))
                #print(sum( gp.abs_(c*m.getVarByName(str("v"+str(edges[0])+str(c))) - c*m.getVarByName(str("v"+str(edges[1])+str(c)))) for c in range(1,(num_of_columns+1) )) == 0)
            # Optimize model
            m.optimize()
            status = m.status
            print("m.status:",m.status)
            if status == GRB.INFEASIBLE:
                print("Model Infeasible")
                print("(C1_init,C2_init):",C1_init,C2_init)
                #break
                C1_init = C1_init + 1
                C2_init = C2_init + 1
                
                #m.remove(m.getConstrs()[0::])
                #m.update()
                break
                if C1_init > 3:
                    break
                continue
            if status == GRB.OPTIMAL:
                break
            
        assigned_col = []
        for i in range(0,num_cluster_nodes):
            assigned_col.insert(i, -1)
            

        cluster_result = []
        for i in range(0,number_of_cgra_clusters):
            cluster_result.insert(i,[])
            
        print('Obj: %g' % m.objVal)
        for i in range(0,num_cluster_nodes):
            for c in range(1,num_of_columns+1):
                print(m.getVarByName(str("v"+str(i)+str(c))), m.getVarByName(str("v"+str(i)+str(c))).x)
                if m.getVarByName(str("v"+str(i)+str(c))).x == 1:
                    assigned_col[i] = c
                    #node_list = []
                    #print("node list:",node_list)
                    index = num_of_columns*assigned_row[i]+(c-1)
                    node_list = cluster_result[index]
                    node_list.append(i)
                    #cluster_result.insert(int(index), node_list)
                    cluster_result[index]=node_list
            
        
        for i in range(0,num_cluster_nodes):
            print("node: (row,col)",i,assigned_row[i],assigned_col[i])
            
        #g = graphviz.Digraph('G', engine="neato", filename='cluster_map.gv', format='png')
        
        #for i in range(0,num_cluster_nodes):
            #posit = str("'"+str(assigned_row[i])+","+str(assigned_col[i])+"!'")
            #posit = str(""+str(assigned_col[i])+","+str(assigned_row[i])+"!")
            #print(posit)
            #g.node(str(i),pos=posit,color=colordict[i])
        
        #for edges in clus_dfg.edges:
            #g.edge(str(edges[0]),str(edges[1]))

        #g.render()
        
        for r in range(0,num_of_rows):
            for c in range(0,num_of_columns):
                index = num_of_columns*r+c
                print(cluster_result[index], end ="\t")
            print()
            
        print("DFG nodes in each cluster:")
        i=0
        for nodes in clus_dfg.nodes:
            print(i,int(clus_dfg.nodes[nodes]["label"]))
            i=i+1
    
        print("(C1_init,C2_init):",C1_init,C2_init)
        
        with open("cluster_mapping.txt", "w") as f:
            for r in range(0,num_of_rows):
                for c in range(0,num_of_columns):
                    index = num_of_columns*r+c
                    f.write(str(cluster_result[index]) + '\t')
                f.write('\n')
            i=0
            for nodes in clus_dfg.nodes:
                f.write(str(i)+'\t'+str(clus_dfg.nodes[nodes]["label"])+'\n')
                i=i+1
        f.close()
        
        dfg_to_cgra_cluster_mapping_outcome_r = []
        dfg_to_cgra_cluster_mapping_outcome_c = []
        for i in range(0,num_cluster_nodes):
            dfg_to_cgra_cluster_mapping_outcome_r.insert(i,[])
            dfg_to_cgra_cluster_mapping_outcome_c.insert(i,[])
            
        for i in range(0,num_cluster_nodes):
            for r in range(0,num_of_rows):
                for c in range(0,num_of_columns):
                    index = num_of_columns*r+c
                    for node in cluster_result[index]:
                        if node == i:
                            node_list = dfg_to_cgra_cluster_mapping_outcome_r[i]
                            node_list.append(r)
                            dfg_to_cgra_cluster_mapping_outcome_r[i]=node_list
                            node_list = dfg_to_cgra_cluster_mapping_outcome_c[i]
                            node_list.append(c)
                            dfg_to_cgra_cluster_mapping_outcome_c[i]=node_list
            
        cgra_clustering_outcome = "cluster_mapping_result.txt"
        i=0
        print("DFG cluster to CGRA cluster Mapping:")
        print("Cluster ID\t[Rows]\t[Cols]")
        with open(cgra_clustering_outcome, "w") as f:
            for i in range(0, num_cluster_nodes):
                f.write(str(i) + '\t' + str(dfg_to_cgra_cluster_mapping_outcome_r[i]) + '\t' + str(dfg_to_cgra_cluster_mapping_outcome_c[i]) + '\n')
                print(str(i) + '\t' + str(dfg_to_cgra_cluster_mapping_outcome_r[i]) + '\t'  + str(dfg_to_cgra_cluster_mapping_outcome_c[i]) )
        f.close()
    

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
    
    except AttributeError:
        print('Encountered an attribute error')
if __name__ == '__main__':
    C1_init = sys.argv[1]
    C2_init = sys.argv[2]
    cgra_cluster_r = sys.argv[3]
    cgra_cluster_c = sys.argv[4]
    main(C1_init, C2_init,cgra_cluster_r, cgra_cluster_c)
