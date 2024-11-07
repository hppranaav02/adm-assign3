import os
import time
import subprocess
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Define algorithms and data types
algorithms = ["BIN", "FOR", "DIF", "RLE", "DIC"]
metrics = []

# Provided dictionary of data files for each data type
data_files = {
    "int8": ["l_discount-int8.csv", "l_linenumber-int8.csv", "l_quantity-int8.csv", "l_tax-int8.csv"],
    "int16": ["l_discount-int16.csv", "l_linenumber-int16.csv", "l_quantity-int16.csv", "l_tax-int16.csv", "l_suppkey-int16.csv"],
    "int32": ["l_discount-int32.csv", "l_linenumber-int32.csv", "l_orderkey-int32.csv", "l_partkey-int32.csv", "l_quantity-int32.csv", "l_suppkey-int32.csv", "l_orderkey-int32.csv", "l_partkey-int32.csv"],
    "int64": ["l_discount-int64.csv", "l_linenumber-int64.csv", "l_orderkey-int64.csv", "l_partkey-int64.csv", "l_quantity-int64.csv", "l_suppkey-int64.csv", "l_orderkey-int64.csv", "l_partkey-int64.csv"],
    "string": ["l_comment-string.csv", "l_linestatus-string.csv", "l_commitdate-string.csv", "l_receiptdate-string.csv", "l_returnflag-string.csv", "l_shipdate-string.csv", "l_shipinstruct-string.csv", "l_shipmode-string.csv"]
}

# Valid combinations of algorithms and data types
valid_combinations = {
    "BIN": ["int8", "int16", "int32", "int64"],
    "FOR": ["int8", "int16", "int32", "int64"],
    "DIF": ["int8", "int16", "int32", "int64"],
    "RLE": ["int8", "int16", "int32", "int64", "string"],
    "DIC": ["int8", "int16", "int32", "int64", "string"]
}

# Generate encoded filename according to the observed naming scheme
def generate_encoded_filename(input_file, algorithm):
    extensions = {
        "BIN": ".bin",
        "FOR": ".for",
        "DIF": ".dif",
        "RLE": ".rle",
        "DIC": ".dic"
    }
    return f"{input_file}{extensions[algorithm]}"

# Function to encode using specified script and collect metrics
def encode_process(algorithm, data_type, input_file, encode_script):
    start_time = time.time()
    encoded_file = generate_encoded_filename(input_file, algorithm)
    
    # Run the encoding script, suppressing stdout/stderr
    with open(os.devnull, 'w') as fnull:
        subprocess.run(["python", encode_script, input_file], stdout=fnull, stderr=fnull)
    
    encode_time = time.time() - start_time
    if os.path.exists(encoded_file):
        print(f"Encoded file created: {encoded_file}")
    else:
        print(f"Encoding failed or file not created: {encoded_file}")
    return encoded_file, encode_time

# Function to decode using specified script and command output redirection
def decode_process(algorithm, data_type, encoded_file, decode_script):
    start_time = time.time()
    decoded_file = f"{encoded_file}.csv"
    
    # Check if encoded file exists before attempting to decode
    if not os.path.exists(encoded_file):
        print(f"Encoded file not found, skipping: {encoded_file}")
        return None, None
    
    # Run the decoding script with output redirection
    with open(decoded_file, 'w') as outfile:
        subprocess.run(["python", decode_script, encoded_file], stdout=outfile, stderr=subprocess.DEVNULL)
    
    decode_time = time.time() - start_time
    if os.path.exists(decoded_file):
        print(f"Decoded file created: {decoded_file}")
    else:
        print(f"Decoding failed or file not created: {decoded_file}")
    return decoded_file, decode_time

# Calculate metrics and add them to the metrics list
def calculate_metrics(algorithm, data_type, input_file, encoded_file, decoded_file, encode_time, decode_time):
    input_size = os.path.getsize(input_file)
    encoded_size = os.path.getsize(encoded_file) if os.path.exists(encoded_file) else None
    decoded_size = os.path.getsize(decoded_file) if decoded_file and os.path.exists(decoded_file) else None
    compression_ratio = input_size / encoded_size if encoded_size else None
    accuracy = "Success" if decoded_size == input_size else "Mismatch" if decoded_size is not None else "Not Decoded"
    
    metrics.append({
        "Algorithm": algorithm,
        "Data Type": data_type,
        "Input Size (bytes)": input_size,
        "Encoded Size (bytes)": encoded_size,
        "Decoded Size (bytes)": decoded_size,
        "Compression Ratio": compression_ratio,
        "Encoding Time (s)": encode_time,
        "Decoding Time (s)": decode_time,
        "Accuracy": accuracy
    })

# Main function to run encoding and decoding in parallel phases
def run_all():
    # Encoding phase
    print("Starting Encoding Phase...")
    encode_tasks = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for algorithm in algorithms:
            for data_type, files in data_files.items():
                if data_type not in valid_combinations[algorithm]:
                    continue
                encode_script = f"program-en-{algorithm.lower()}-{data_type}.py"
                for input_file in files:
                    if not os.path.exists(input_file):
                        print(f"Skipping missing file: {input_file}")
                        continue
                    future = executor.submit(encode_process, algorithm, data_type, input_file, encode_script)
                    encode_tasks.append((future, algorithm, data_type, input_file))

    # Collect results from encoding phase
    encoded_files = []
    for future, algorithm, data_type, input_file in encode_tasks:
        encoded_file, encode_time = future.result()
        calculate_metrics(algorithm, data_type, input_file, encoded_file, None, encode_time, None)
        if os.path.exists(encoded_file):
            encoded_files.append((algorithm, data_type, encoded_file))

    # Decoding phase
    print("Starting Decoding Phase...")
    decode_tasks = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for algorithm, data_type, encoded_file in encoded_files:
            decode_script = f"program-de-{algorithm.lower()}-{data_type}.py"
            future = executor.submit(decode_process, algorithm, data_type, encoded_file, decode_script)
            decode_tasks.append((future, algorithm, data_type, encoded_file))

    # Collect results from decoding phase
    for future, algorithm, data_type, encoded_file in decode_tasks:
        decoded_file, decode_time = future.result()
        if decoded_file is not None and os.path.exists(decoded_file):
            print(f"Decoded file saved: {decoded_file}")
            for metric in metrics:
                if metric["Algorithm"] == algorithm and metric["Data Type"] == data_type and metric["Encoded Size (bytes)"] == os.path.getsize(encoded_file):
                    metric["Decoding Time (s)"] = decode_time
                    metric["Decoded File"] = decoded_file
                    break
        else:
            print(f"Skipping decoding for {encoded_file} - decoded file not found.")

    # Save metrics to CSV and LaTeX files
    df = pd.DataFrame(metrics)
    df.to_csv("encoding_decoding_metrics.csv", index=False)
    with open("metrics_table.tex", "w") as tex_file:
        tex_file.write(df.to_latex(index=False))

if __name__ == "__main__":
    run_all()
