
#!/bin/zsh

# Get the Arguments:

SRC_TACOS=$1
DEST_DIR=$2
DIM=$3
LINK=$4
BW=$5
CHUNK=$6
CHUNK_PER_COLL=$7
YAML_FILE=$8

# Go into DEST DIR
cd $DEST_DIR

#path to chakra folder
export PYTHONPATH="/home/davendra/project/chakra:$PYTHONPATH"

# <---------------------------------------------------------- CALL 1: TACOS --------------------------------------------------------->
# echo "<------------------------------------------------------Calling TACOS ---------------------------------------------------------->"

TACOS_FILENAME=$(basename "$SRC_TACOS")

cp "$SRC_TACOS" "./$TACOS_FILENAME"

# Set execute permission for the binary file
chmod +x "./$TACOS_FILENAME"

# Now run the binary with the arguments and redirect the output to output.txt
./"$TACOS_FILENAME" "$DIM" "$LINK" "$BW" "$CHUNK" "$CHUNK_PER_COLL" > output.txt


# <---------------------------------------------------------- CALL 2: XML ---------------------------------------------------------->

python3 ../../analyze_network.py --K $DIM --link_lat $LINK --bw $BW --chunk_size $CHUNK --chunk_per_collective $CHUNK_PER_COLL --debug 0


# <---------------------------------------------------------- CALL 3: CHAKRA -------------------------------------------------------->

# Construct the input filename
INPUT_XML_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}.xml"
OUTPUT_ET_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}"

# make a directory for chakra outputs if it doesn't already exist
# mkdir -p chakra_et

# Call the et_converter.py with the dynamically constructed filenames
python3 -m et_converter.et_converter \
  --input_type msccl \
  --input_filename "$INPUT_XML_FILENAME" \
  --output_filename "$OUTPUT_ET_FILENAME" \
  --num_dims 2

# <---------------------------------------------------------- CALL 4: ASTRASIM ------------------------------------------------------>

#path to ASTRA-SIM binary
BINARY=/home/davendra/project/astra-sim/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware

SCRIPT_DIR=../../

WORKLOAD=$OUTPUT_ET_FILENAME
# echo $WORKLOAD

#WORKLOAD=./inputs/workload/test/one_comm_coll_node_allgather

SYSTEM="${SCRIPT_DIR:?}"inputs/system/Ring.json
# echo $SYSTEM

#to do : update the yml file before running
# NETWORK="${SCRIPT_DIR:?}"inputs/network/Mesh2D.yml

NETWORK=$YAML_FILE
# echo $NETWORK

# NETWORK=/home/davendra/project/APEX_HML_Project/inputs/network/Mesh2D.yml

MEMORY="${SCRIPT_DIR:?}"inputs/remote_memory/no_memory_expansion.json

# echo $MEMORY

"${BINARY}" \
  --workload-configuration="${WORKLOAD}" \
  --system-configuration="${SYSTEM}" \
  --network-configuration="${NETWORK}"\
  --remote-memory-configuration="${MEMORY}" > "${OUTPUT_ET_FILENAME}_astrasim.txt"


# <----------------------------------------------------------  delete ET files ------------------------------------------------------>
# rm -rf *et
# rm -rf ./$TACOS_FILENAME