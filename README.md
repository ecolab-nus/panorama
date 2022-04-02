# Panorama

Panorama is a fast and scalable CGRA compiler for mapping complex loop kernels on CGRA. It is a hierarchical mapping approach where higher-level mapping partitions the dataflow graph onto CGRA clusters and guide the lower level mapping. Panorama is a portable solution that can be combined with existing low-level CGRA mappers. Please find the [paper](https://www.comp.nus.edu.sg/~tulika/publications.htm) for more details.


## Framework

Thi picture shows the whole frameowork:

<img src="overview.jpg" alt="drawing" width="700"/> \



### Directory Structure

```
panorama
│   README.md  
│   overview.jpg
└───src  
│   │   dfg_clustering.py (DFG clustering using Scikit Learn spectral clustering)
│   │   cluster_mapping.py (Graph drawing based cluster mapping)
│   │   find_cluster_size.py (Find optimal cluster size based on imbalance factor)
│   │   run_example.py (script to run dfg clustering and cluster mapping on example DFGs)
│   │───panorama_with_morpher (use panorama high-level-mapping result on morpher low-level-mapper)
│   │   │─── Morpher_DFG_Generator
│   │   │─── Morpher_CGRA_Mapper
│   │   │─── Cluster_Mapping
│   │   │─── Scripts
│   │   │   │─── run_dse.py (Invoke all tools for low-level mapping)
│   │   │   │─── config_v2.csv (Configurations for high-level and low-level mapping)  
└───data 
│   │───morpher_dfgs (example DFGs generated from Morpher_DFG_Generator)
│   │───results (dfg clustering and cluster mapping results)
│   │   │─── application_kernel-<run datetime> 
│   │   │   │─── dfg_clustering_result.txt 
│   │   │   │─── cluster_mapping_result.txt 
│   │   │   │─── cdfg_<application_kernel>_<cluster_size>.png (Cluster dependency graph)
│   │   │   │─── other log files


```
### API and scripts
* run_example.py: This script invoke dfg_clustering.py and cluster_mapping.py to generate high level mapping result on a given DFG and given CGRA cluster size. It takes six input arguments: dfg name, number of clusters, C1,C2 (control number of diagonal edges) and cgra cluster dimension (row,column). For  example: ``python run_example.py edn 10 1 1 4 4``
* dfg_clustering.py: This python file has three arguments: dfg file path, number of dfg clusters, and affinity matrix type (default:'precomputed'). 
* cluster_mapping.py: This python file has four arguments: C1, C2 to control diagonal edges and cgra cluster dimensions (row, col). 
* find_cluster_size.py: This python file list down optimal cluster size based on imbalance factor. It takes three arguments: dfg name, min and max number of clusters. 
* run_dse.py (in panorama_with_morpher): This file invoke 1) morpher_dfg_generator to generate the DFGs from annotated C source code, 2) run the dfg clustering and cluster mapping using the parameters in the config file 3) run morpher_cgra_mapper guided by the cluster_mapping result



# Getting started
## Requirement: 
* Ubuntu (we have tested Ubuntu 16.04 and 18.04)
* We provide two ways to install Panorama: 
  1) Build on your machine. You need to install .
  
## How to install

### Build on your machine
* Download source code: ``$ git clone --recurse-submodules  https://github.com/ecolab-nus/panorama.git``. 
* 

  

## Running Example:
We provide an example to map DFG using LISA. 


### Map DFG using Panorama:



# Portability: workflow to use Panorama for a new mapper



# Citation

```
@inproceedings{wijerathne2022panorama,
  title={PANORAMA: Divide-and-Conquer Approach for Mapping Complex Loop Kernels on CGRA
},
  author={Dhananjaya Wijerathne, Zhaoying Li, Thilini Kaushalya Bandara, Tulika Mitra},
  booktitle={59th ACM/IEEE Design Automation Conference (DAC), 2022},
  year={2022},
  organization={ACM/IEEE}
}
```
