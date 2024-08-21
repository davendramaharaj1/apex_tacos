# %%
import json
import argparse
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import os
import pprint
import matplotlib.image as mpimg
from networkx.drawing.nx_agraph import to_agraph

def clean_directory(directory):
    # This function removes all files and folders in the specified directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def preprocess_csv(input_file, output_file):
    """
    Processes the CSV file by mapping each of the timestep values to unique integers.

    Parameters:
    input_file (str): The path to the input CSV file. //Might update with systemn
    output_file (str): The path to the output preprocessed CSV file. //Chage this to store the csv somewhere else

    Returns:
    None
    """
    timestep_mapping = {} # Dictionary to map each timestep to a unique integer
    current_timestep = 0 
    
    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file) # Read the CSV file
        rows = list(csv_reader) # Store the rows of the CSV in a list
    
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file) # Write to the output CSV file

        #Iterate through each row in the CSV file
        for row in rows:
            timestep = float(row[0]) # Extract the timestep value from the row
            
            if timestep not in timestep_mapping: # If the timestep is not already mapped
                timestep_mapping[timestep] = current_timestep # Map the timestep to the current current_timestep equal 
                current_timestep += 1  # Increment the current_timestep
            
            row[0] = str(timestep_mapping[timestep]) # Update the timestep value in the row
            csv_writer.writerow(row) 

def pretty_print_node_traffic(data, indent=0):
    for node, edges in data.items():
        print('    ' * indent + str(node) + ':')
        if isinstance(edges, dict):
            pretty_print_node_traffic(edges, indent + 1)
        else:
            print('    ' * (indent + 1) + str(edges))

def visualize_graph(G, GRAPH_DATA_DIR, name, t):
    # print('Inside visual Graph = ',t)
    # Set positions for a 3x3 grid with more spacing
    pos = {
        0: "0,4!",
        1: "2,4!",
        2: "4,4!",
        3: "0,2!",
        4: "2,2!",
        5: "4,2!",
        6: "0,0!",
        7: "2,0!",
        8: "4,0!"
    }

    # Method 2: Visualize using Graphviz with fixed node positions
    A = to_agraph(G)

    # Set the fixed positions for each node
    for node, position in pos.items():
        A.get_node(node).attr['pos'] = position

    A.node_attr['shape'] = 'square'
    A.node_attr['style'] = 'filled'
    A.node_attr['fillcolor'] = 'skyblue'
    A.node_attr['fontcolor'] = 'black'
    A.edge_attr['fontsize'] = '10'
    A.layout(prog='fdp', args='-n')

    # Corrected the graphviz_path as mentioned earlier (#3)
    img =  f'output_{name}.png'
    graph_file = os.path.join(GRAPH_DATA_DIR, img)
    # graphviz_path = f'data/output_{name}.png'  # Make sure to use a valid path where the file can be saved

    A.draw(graph_file)  # Saving to output file for display
        
# Function to generate and save XML in a pretty format
def generate_and_save_xml_pretty(node_traffic, filename, chunks_per_collective, num_npus):

    root = ET.Element("algo", name = "allgather_ring_1channelsperring", proto="LL128", nchannels="1", nchunksperloop=str(chunks_per_collective), ngpus=str(num_npus), coll="allgather", inplace="1", maxcount="1", nthreadblocks="1")

    # Create <gpu> tags for each node
    for node, edges in sorted(node_traffic.items()):
        gpu_elem = ET.SubElement(root, "gpu", id=str(node), i_chunks="0", o_chunks=str(num_npus), s_chunks="0")

        # Create <tb> tags for each connected edge
        for (source, destination), edge_info in edges.items():
            tb_elem = ET.SubElement(gpu_elem, "tb", id=str(edge_info['threadID']),
                                    send=str(destination if edge_info['records'][0]['type'] == 's' else '-1'),
                                    recv=str(source if edge_info['records'][0]['type'] == 'r' else '-1'),
                                    chan="0")

            # step_counter = 0

            # create <step> tags for each time step
            for record in edge_info['records']:
                
                if record['type'] == '-1':
                    continue
                
                # record['timestep'] = step_counter

                # Check for matching chunkID between 's' and 'r' records

                # Check other threadblocks
                for (source_other, destination_other), edge_info_other in edges.items():
                    
                    # for the other threadblocks, check the step
                    for record_other in edge_info_other['records']:
                        
                        # # ------------------------------------DEBUG------------------------------------
                        # if debug:
                        #     if (record['type'] == record_other['type']) and (record['chunkID'] == record_other['chunkID']) \
                        #         and (record['timestep'] != record_other['timestep']):

                        #         print(f'record_type: {record['type']}, record_chunkID: {record['chunkID']}, record_timestep: {record['timestep']}, record_other_timestep: {record_other['timestep']}, gpuID": {node}')
                        #  # ------------------------------------DEBUG------------------------------------

                        if(record['type'] == 's' and record_other['type'] == 'r'):
                            if(record['chunkID'] == record_other['chunkID']):
                                
                                record['hasdep'] = 1
                                record['depid'] = edge_info_other["threadID"]
                                record['deps'] = record_other['timestep']
                
                # if record['type'] != '-1':
                ET.SubElement(tb_elem, "step", s=str(record['timestep']), type=record['type'], srcbuf="o",
                              srcoff=str(record['chunkID']), dstbuf="o", dstoff=str(record['chunkID']),
                              cnt=str(chunks_per_collective), depid=str(record['depid']), deps=str(record['deps']),
                              hasdep=str(record['hasdep']))

                # step_counter += 1


                
    # Convert to string using ElementTree and parse with minidom for pretty printing
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    # Write to file
    with open(filename, 'w') as file:
        file.write(pretty_xml_as_string)

def setup_parser():
    parser = argparse.ArgumentParser(description="Run experiments with specified parameters.")
    parser.add_argument('--K', type=int, default=3, help='Parameter K')
    parser.add_argument('--link_lat', type=int, default=500, help='Link latency')
    parser.add_argument('--bw', type=int, default=50, help='Bandwidth')
    parser.add_argument('--chunk_size', type=int, default=1024, help='Chunk size')
    parser.add_argument('--chunk_per_collective', default=1, type=int, help='Chunks per collective')
    parser.add_argument('--debug', default=False, type=int, help='DEBUG MODE')
    return parser
    

def main():

    parser = setup_parser()
    args = parser.parse_args()

    mesh_dim = args.K
    link_lat = args.link_lat
    bw = args.bw
    chunk_size = args.chunk_size
    chunks_per_collective = args.chunk_per_collective
    debug = args.debug

    num_npus = int(mesh_dim * mesh_dim)
    npu_ids = range(num_npus)

    if debug:
        print(f'NPU IDs: {npu_ids}')

    # input and output CSV file paths
    tacos_input_file = 'output.csv'
    file_name_prefix = f'gpu_{mesh_dim}_link_{link_lat}_bw_{bw}_chunk_{chunk_size}_chunk_coll_{chunks_per_collective}'
    tacos_preprocessed_output_file = f'{file_name_prefix}.csv'

    # <---------------------------------------------------------- STEP 1: PREPROCESS OUTPUT.CSV --------------------------------------------------------->

    # Preprocess the CSV file
    preprocess_csv(tacos_input_file, tacos_preprocessed_output_file)
    # print(f"Preprocessed CSV file created: {tacos_preprocessed_output_file}")

    # <---------------------------------------------------------- STEP 2: CREATE GRAPHS --------------------------------------------------------->


    df = pd.read_csv(tacos_preprocessed_output_file, header=None) #Header row doesnt exists
    df.columns = ['Timestep', 'chunkID', 'source', 'destination']

    # print(f'List of GPUS: {npu_ids}')
    # print(f'Number of time steps: {len(np.unique(df['Timestep']))}')

    # Create graphs per timestep
    graphs = {t: nx.DiGraph() for t in df['Timestep'].unique()}

    # add all gpu_ids to graph
    for t, graph in graphs.items():
        graph.add_nodes_from(npu_ids)

    # Populate each graph
    for _, row in df.iterrows():
        graphs[row['Timestep']].add_edge(row['source'], row['destination'], label=row['chunkID'])

    # DEBUG: VISUALIZATION
    if debug:
        GRAPH_DATA_DIR = 'data/'

        # Ensure the output directory is clean
        if os.path.exists(GRAPH_DATA_DIR):
            # print(f'Directory: {GRAPH_DATA_DIR} alreadY exists!')
            # print(f'Cleaning {GRAPH_DATA_DIR}...\n')
            clean_directory(GRAPH_DATA_DIR)
            # print(f'Done cleaning {GRAPH_DATA_DIR}\n')
        else:
            try: 
                os.makedirs(GRAPH_DATA_DIR) 
            # print("Directory '%s' created successfully" % OUTPUT_PATH) 
            except OSError as error: 
                print("Directory '%s' can not be created" % GRAPH_DATA_DIR)

        for t, graph in graphs.items():
            print(f'Graph No: {t}')
            name = f'graph_{t}'
            visualize_graph(graph, GRAPH_DATA_DIR, name=name, t=t)

    # <---------------------------------------------------------- STEP 3: CREATE DATA STRUCTURE --------------------------------------------------------->

    # Initialize node_traffic from all possible edges in the first graph
    node_traffic = {}

    first_graph = graphs[0]  # Assuming the first timestep graph is fully representative
    for node in first_graph.nodes():
        
        node_traffic[node] = {}
        edge_counter = 0  # Reset counter for each node

        # Add thread blocks for all outgoing edges
        for target in first_graph.successors(node):
            node_traffic[node][(node, target)] = {
                'threadID': edge_counter,
                'records': [{'timestep': t, 'chunkID': -1, 'type': '-1', 'depid': -1, 'deps': -1, 'hasdep': 0} for t in graphs.keys()]
            }
            edge_counter += 1

        # Add thread blocks for all incoming edges if not already added
        for source in first_graph.predecessors(node):
            if (source, node) not in node_traffic[node]:
                node_traffic[node][(source, node)] = {
                    'threadID': edge_counter,
                    'records': [{'timestep': t, 'chunkID': -1, 'type': '-1', 'depid': -1, 'deps': -1, 'hasdep': 0} for t in graphs.keys()]
                }
                edge_counter += 1

    # Populate the node_traffic with actual data from all timestep graphs
    for t_index, graph in graphs.items():
        for source, destination, data in graph.edges(data=True):
            node_traffic[source][(source, destination)]['records'][t_index]['chunkID'] = data['label']
            node_traffic[source][(source, destination)]['records'][t_index]['type'] = 's'
            node_traffic[destination][(source, destination)]['records'][t_index]['chunkID'] = data['label']
            node_traffic[destination][(source, destination)]['records'][t_index]['type'] = 'r'

    if debug:
        with open('node_traffic_before.log', 'w') as f:
            # Use pprint and direct the output to the file
            pprint.pprint(node_traffic, stream=f)


    # Reassign Timesteps ------> Ignore negatives
    for gpu, threadblocks in sorted(node_traffic.items()):
        # Create <tb> tags for each connected edge
        for (source, destination), timesteps in threadblocks.items():

            step_counter = 0
            
            # iterate over the list of timesteps

            for step in timesteps['records']:
                
                if step['type'] == '-1':
                    step['timestep'] = "-1"
                    continue
                
                step['timestep'] = step_counter
                step_counter += 1


    # <---------------------------------------------------------- STEP 4: GENERATE XML FILE --------------------------------------------------------->

    # #### Step 1.4 Generate XML from data structure node_traffic & dump in XML file
    filename = f'{file_name_prefix}.xml'
    generate_and_save_xml_pretty(node_traffic, filename, chunks_per_collective, num_npus)
    # print(f"XML file saved as {filename}")


    # input_file = "network_flow_pretty.xml"
    # output_file = "network_flow_pretty.xml"
    
    # Read the content of the input XML file
    with open(filename, "r") as file:
        xml_content = file.read()
    
    # Remove the XML declaration
    modified_xml_content = xml_content.replace('<?xml version="1.0" ?>', '').lstrip()
    
    # Write the modified content back to the output file
    with open(filename, "w") as file:
        file.write(modified_xml_content)

    if debug:
        with open('node_traffic_after.log', 'w') as f:
            # Use pprint and direct the output to the file
            pprint.pprint(node_traffic, stream=f)


if __name__ == "__main__":
    main()