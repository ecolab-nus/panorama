cd panorama_with_morpher/Morpher_DFG_Generator
mkdir build
cd build
cmake ..
make  -j 2
cd ../../Morpher_CGRA_Mapper
mkdir build_hierarchical_spr
cd build_hierarchical_spr
cmake ..
make CXX_FLAGS="-DHIERARCHICAL -DSIM_ANNEAL" -j