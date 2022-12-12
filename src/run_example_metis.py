  #!/usr/bin/env python
import sys
import os
import os.path
import shutil
import time 
import datetime 
############################################


def main(application,no_clusters,C1_init_, C2_init_, cgra_cluster_r, cgra_cluster_c):

  #PANORAMA_HOME = '/home/dmd/Workplace/panorama'	
  #if not 'PANORAMA_HOME' in os.environ:
    #raise Exception('Set PANORAMA_HOME directory as an environment variable (Ex: export PANORAMA_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)')

 
  
  today = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
  dir_name = 'Datetime_%s/' % (today)

  RESULTS_PWD = '../data/results/'+application+'/' + dir_name

  my_mkdir(RESULTS_PWD)




##############################################################################################################################################

  print('\nRunning DFG Clustering\n')
  os.chdir(RESULTS_PWD)
  os.system('python ../../../../src/dfg_clustering_metis.py ../../../morpher_dfgs/%s/*.xml %s %s > dfg_clustering_log.txt' % (application,no_clusters, ('precomputed')))
  os.system('dot -Tpng cdfg.dot -o cdfg_%s_%s.png' % (application,no_clusters))

	
##############################################################################################################################################
  print('\nRunning cluster mapping\n')
  os.system('python ../../../../src/cluster_mapping.py %s %s %s %s > cluster_mapping_log.txt' % (C1_init_,C2_init_,cgra_cluster_r,cgra_cluster_c))




##############################################################################################################################################


  end = time.time() 

  #f.write("\n\nExecution time: %s"% (end - start))   
  #f.close() 


def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
    application = sys.argv[1]
    no_clusters = sys.argv[2]  
    C1_init = sys.argv[3]
    C2_init = sys.argv[4]
    cgra_cluster_r = sys.argv[5]
    cgra_cluster_c = sys.argv[6]  
    main(application,no_clusters,C1_init, C2_init,cgra_cluster_r, cgra_cluster_c)
