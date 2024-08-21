import os
import yaml
import subprocess
import numpy as np
from itertools import product
import concurrent.futures

# Function to clean directories
def clean_directory(directory):
    import shutil
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Function to perform analysis
def run_analysis(K, link_lat, bw, chunk_size, chunk_per_collective):
    
    # add path to TACOS binary
    TACOS_SRC = '/home/davendra/project/APEX_HML_Project/build/bin/TACOS'
    ROOT_DIR = './apex_outputs'
    OUTPUT_DIR = f'gpu_{K}_link_{link_lat}_bw_{bw}_chunk_{chunk_size}_chunk_coll_{chunk_per_collective}'
    OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_DIR)

    # Ensure the output directory is clean and exists
    if os.path.exists(OUTPUT_PATH):
        clean_directory(OUTPUT_PATH)
    else:
        os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Create the YAML file
    original_yaml_path = './inputs/network/Mesh2D.yml'

    # Load the original YAML file
    with open(original_yaml_path, 'r') as file:
        original_data = yaml.safe_load(file)

    # Update the data with the new values
    original_data['topology'] = ['Mesh2D']
    original_data['npus_count'] = [int(K*K)]
    original_data['bandwidth'] = [float(bw)]
    original_data['latency'] = [float(link_lat)]
    
    # Define a new file name based on the bandwidth and latency
    new_yaml_file_name = f'Mesh2D_bw_{bw}_lat_{link_lat}.yml'
    new_yaml_file = os.path.join(OUTPUT_PATH, new_yaml_file_name)
    
    # Write the modified data to a new YAML file
    with open(new_yaml_file, 'w') as new_file:
        yaml.safe_dump(original_data, new_file)

    command = f"./run_dse.sh {TACOS_SRC} {OUTPUT_PATH} {K} {link_lat} {bw} {chunk_size} {chunk_per_collective} {new_yaml_file_name}"
    subprocess.run(command, shell=True, check=True)

# Parameters for the product

# k = 2, 4, 6, 8, 10
K = [10] # to be changed for different team members
link_latency = [500]
bandwidths = list(range(0, 1100, 100))  # GB/s
chunk_size = list(range(0, 10500, 500))  # MB
chunks_per_collective = [1, 2, 3, 4]

bandwidths[0] = 1
chunk_size[0] = 1

param_combinations = list(product(K, link_latency, bandwidths, chunk_size, chunks_per_collective))

# Running the tasks in parallel
def main():
    # Determine the number of cores to use
    total_cores = os.cpu_count()
    number_of_workers = max(8, 18)  # Use all but one core

    # Using ProcessPoolExecutor with a specific number of workers
    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        # Submit all tasks to the executor
        futures = [executor.submit(run_analysis, *params) for params in param_combinations]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Get the result of the task
            except Exception as exc:
                print(f'Generated an exception: {exc}')

if __name__ == '__main__':
    main()
    print('DONE SIMULATION!')

# run_analysis(3, 500, 50, 2048, 1)

# print(f'Length of combinations: {len(param_combinations)}')