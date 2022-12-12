  #!/usr/bin/env python
import sys
import os
import os.path
import shutil
import time 
import datetime 
############################################


def main(application,target_function, cluster_algo, no_clusters,C1_init_, C2_init_, cgra_cluster_r, cgra_cluster_c, arch_desc, maxIter,skip_inter_or_intra, open_set_limit, entry_id,summary_log,initII,maxIterTime):

  PANORAMA_HOME =  os.getcwd()	  
  DFG_GEN_HOME = PANORAMA_HOME + '/panorama_with_morpher/Morpher_DFG_Generator'
  # DFG_CLUSTRNG_HOME = PANORAMA_HOME + '/HiMap2_Cluster_Mapping'
  MAPPER_HOME = PANORAMA_HOME + '/panorama_with_morpher/Morpher_CGRA_Mapper'
  #SIMULATOR_HOME = HIMAP2_HOME + '/hycube_simulator'
  
  # today = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
  # dir_name = 'SPR_Entry_%s_Datetime_%s/' % (entry_id,today)
  #sum_log_name = '_entry_%s_Datetime_%s_clusters_%s_Init_%s_C1_%s_C2_%s_r_%s_c_%s_arch_%s_maxIter_%s_skip_%s_oslimit_%s' % (entry_id,today)

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/'+ application +'/'
  # DFG_CLUSTRNG_KERNEL = DFG_CLUSTRNG_HOME + '/applications/edn/' + dir_name
  # MAPPER_KERNEL = MAPPER_HOME + '/applications/clustered_arch/'+ application +'/'+ dir_name
  # EXECTIME_SUMMARY = HIMAP2_HOME + '/HiMap2_Scripts/exec_time/'+ application +'/' 
  #SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/'

  my_mkdir(DFG_GEN_KERNEL)
  # my_mkdir(DFG_CLUSTRNG_KERNEL)
  # my_mkdir(MAPPER_KERNEL)
  # my_mkdir(EXECTIME_SUMMARY)
  
  today = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
  dir_name = 'Datetime_%s/' % (today)

  RESULTS_PWD = PANORAMA_HOME+ '/../data/results/'+application+'/' + dir_name



  my_mkdir(RESULTS_PWD)  

##############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  if application =='idctrows' or application =='idctcols' or application =='kmeans' or application =='cordic' :#manually edited for removing a false dependency
    pass
  else:
    os.system('./run_pass.sh %s' % target_function)
  # os.system('dot -Tpdf *_PartPredDFG.dot -o PartPredDFG.pdf')
  os.system('cp DFG_forclustering.xml '+RESULTS_PWD)
  os.system('cp DFG.xml '+ RESULTS_PWD)


##############################################################################################################################################

  print('\nRunning DFG Clustering\n')
  os.chdir(RESULTS_PWD)
  if cluster_algo=='metis':
    os.system('python %s/dfg_clustering_metis.py DFG_forclustering.xml %s %s > dfg_clustering_log.txt' % (PANORAMA_HOME,no_clusters, ('precomputed')))
  else: # spectral
    os.system('python %s/dfg_clustering.py DFG_forclustering.xml %s %s > dfg_clustering_log.txt' % (PANORAMA_HOME,no_clusters, ('precomputed')))

  os.system('dot -Tpng cdfg.dot -o cdfg_%s_%s.png' % (application,no_clusters))
##############################################################################################################################################
  print('\nRunning cluster mapping\n')
  os.system('python %s/cluster_mapping.py %s %s %s %s > cluster_mapping_log.txt' % (PANORAMA_HOME,C1_init_,C2_init_,cgra_cluster_r,cgra_cluster_c))

##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(RESULTS_PWD)
  start = time.time()

  os.system(MAPPER_HOME+'/build_hierarchical_spr/src/cgra_xml_mapper -m %s -d DFG.xml -j %s -s %s -l %s -u %s -a %s -i %s -w %s -v %s > log.txt &' % (maxIter,MAPPER_HOME+'/json_arch/clustered_archs/'+arch_desc, skip_inter_or_intra, open_set_limit,RESULTS_PWD+'../'+summary_log, entry_id, initII, maxIterTime, RESULTS_PWD+'compact_summary.log'))
  os.system('neato -Tpdf arch_allconnections.dot -o %s.pdf' % (arch_desc))
  os.system('neato -Tpdf arch_interclusterconnections.dot -o %s_interclusterconnections.pdf' % (arch_desc))


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
    target_function = sys.argv[2]
    cluster_algo = sys.argv[3]
    no_clusters = sys.argv[4]  
    C1_init = sys.argv[5]
    C2_init = sys.argv[6]
    cgra_cluster_r = sys.argv[7]
    cgra_cluster_c = sys.argv[8]
    arch_desc = sys.argv[9]
    maxIter = sys.argv[10]
    skip_inter_or_intra = sys.argv[11]    
    open_set_limit = sys.argv[12]  
    entry_id = sys.argv[13]
    summary_log = sys.argv[14]
    initII = sys.argv[15]
    maxIterTime = sys.argv[16]  
    main(application,target_function,cluster_algo,no_clusters,C1_init, C2_init,cgra_cluster_r, cgra_cluster_c,arch_desc, maxIter,skip_inter_or_intra, open_set_limit, entry_id,summary_log, initII,maxIterTime)
