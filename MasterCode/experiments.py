import os
import subprocess
import csv
import time

# Define paths and configurations
input_directory = "D:/Cloud/OneDrive - Vishwaniketan Trust/Leiden University Workspace/Advanced Data Management for Data Analysis/ADM-A3/ADM-2023-Assignment-3-data-TPCH-SF-1"
output_directory = "output_files"
os.makedirs(output_directory, exist_ok=True)

# Define encoding methods and data types
methods = ["bin", "rle", "dic", "for", "dif"]
data_types = ["int8", "int16", "int32", "int64", "string"]

# Define all 34 files by their data type
files = {
    "int8": [
        "l_discount-int8.csv", "l_extendedprice-int8.csv", "l_linenumber-int8.csv", 
        "l_orderkey-int8.csv", "l_partkey-int8.csv", "l_quantity-int8.csv", 
        "l_suppkey-int8.csv", "l_tax-int8.csv"
    ],
    "int16": [
        "l_discount-int16.csv", "l_extendedprice-int16.csv", "l_linenumber-int16.csv", 
        "l_orderkey-int16.csv", "l_partkey-int16.csv", "l_quantity-int16.csv", 
        "l_suppkey-int16.csv", "l_tax-int16.csv"
    ],
    "int32": [
        "l_discount-int32.csv", "l_extendedprice-int32.csv", "l_linenumber-int32.csv", 
        "l_orderkey-int32.csv", "l_partkey-int32.csv", "l_quantity-int32.csv", 
        "l_suppkey-int32.csv", "l_tax-int32.csv"
    ],
    "int64": [
        "l_discount-int64.csv", "l_extendedprice-int64.csv", "l_linenumber-int64.csv", 
        "l_orderkey-int64.csv", "l_partkey-int64.csv", "l_quantity-int64.csv", 
        "l_suppkey-int64.csv", "l_tax-int64.csv"
    ],
    "string": [
        "l_comment-string.csv", "l_commitdate-string.csv", "l_linestatus-string.csv", 
        "l_receiptdate-string.csv", "l_returnflag-string.csv", "l_shipdate-string.csv", 
        "l_shipinstruct-string.csv", "l_shipmode-string.csv"
    ]
}

# Metrics output file
metrics_file = os.path.join(output_directory, "metrics.csv")

# Helper function to run command and capture time and file sizes
def run_command(command):
    start_time = time.time()
    subprocess.run(command, shell=True)
    elapsed_time = time.time() - start_time
    return elapsed_time

# Write header to metrics CSV
with open(metrics_file, mode="w", newline="") as metrics_csv:
    metrics_writer = csv.writer(metrics_csv)
    metrics_writer.writerow(["File", "Method", "Data Type", "Operation", "Encoding Time (s)", "Decoding Time (s)", 
                             "Original Size (bytes)", "Encoded Size (bytes)", "Decoded Size (bytes)"])

    # Run all combinations
    for data_type, filenames in files.items():
        for filename in filenames:
            input_file = os.path.join(input_directory, filename)

            # Ensure the input file exists
            if not os.path.isfile(input_file):
                print(f"Warning: {input_file} does not exist. Skipping.")
                continue

            # Record original file size
            original_size = os.path.getsize(input_file)

            for method in methods:
                # Encode
                encoded_file = os.path.join(output_directory, f"{filename}.{method}")
                encode_command = f"python main.py en {method} {data_type} \"{input_file}\""

                print(f"Encoding {filename} with {method} for data type {data_type}")
                encoding_time = run_command(encode_command)

                # Check if encoded file was created
                encoded_size = os.path.getsize(encoded_file) if os.path.isfile(encoded_file) else 0

                # Decode
                decoded_output = os.path.join(output_directory, f"{filename}.{method}.decoded.csv")
                decode_command = f"python main.py de {method} {data_type} \"{encoded_file}\" > \"{decoded_output}\""

                print(f"Decoding {encoded_file}")
                decoding_time = run_command(decode_command)

                # Check decoded file size (captured from output redirection)
                decoded_size = os.path.getsize(decoded_output) if os.path.isfile(decoded_output) else 0

                # Write metrics to CSV
                metrics_writer.writerow([
                    filename, method, data_type, "encode/decode", 
                    round(encoding_time, 4), round(decoding_time, 4), 
                    original_size, encoded_size, decoded_size
                ])

print(f"Experiment completed. Metrics saved to {metrics_file}")
