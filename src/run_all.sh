# arguments: application,target_function,cluster_algo,no_clusters,C1_init, C2_init,cgra_cluster_r, cgra_cluster_c,arch_desc, maxIter,skip_inter_or_intra, open_set_limit, entry_id,summary_log, initII,maxIterTime
python -u run_panorama_with_morpher.py edn jpegdct metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 101 pano_results.csv 0 6
python -u run_panorama_with_morpher.py idctcols idctCols metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py idctrows idctRows metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py conv2D convolution2d metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py matched_filter corrFilter_1 metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py matrix_multiply matrix_multiply metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py cordic cordic metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py kmeans kmeans_01 metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py fir fir_filter metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py jpegfdct jpeg_fdct_islow metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6
python -u run_panorama_with_morpher.py invertmat invert_matrix_general metis 9 2 2 3 3 stdnoc_3x3tiles_3x3PEs_8REGS_4PORTS_NW1.json 30 NO 0 201 pano_results.csv 0 6

