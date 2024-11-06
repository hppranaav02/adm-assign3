
import subprocess
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# Original files dictionary (assuming without .rle extensions)
data_files = {
    "int8": ["l_discount-int8.csv", "l_linenumber-int8.csv", "l_quantity-int8.csv", "l_tax-int8.csv"],
    "int16": ["l_discount-int16.csv", "l_linenumber-int16.csv", "l_quantity-int16.csv", "l_tax-int16.csv", "l_suppkey-int16.csv"],
    "int32": ["l_discount-int32.csv", "l_linenumber-int32.csv", "l_orderkey-int32.csv", "l_partkey-int32.csv", "l_quantity-int32.csv", "l_suppkey-int32.csv","l_orderkey-int32.csv","l_partkey-int32.csv"],
    "int64": ["l_discount-int64.csv", "l_linenumber-int64.csv", "l_orderkey-int64.csv", "l_partkey-int64.csv", "l_quantity-int64.csv", "l_suppkey-int64.csv","l_orderkey-int64.csv","l_partkey-int64.csv"],
    "string": ["l_comment-string.csv", "l_linestatus-string.csv", "l_commitdate-string.csv", "l_receiptdate-string.csv","l_returnflag-string.csv","l_shipdate-string.csv","l_shipinstrc-string.csv","l_shipmode-string.csv"]
}

# Compression techniques to be tested
compression_techniques = ["bin", "rle", "dic", "dif", "for"]

# Function to measure file size
def get_file_size(file_path):
    return os.path.getsize(file_path) if os.path.exists(file_path) else 0

# Function to execute encoding and decoding dynamically based on technique and collect results
def process_file(technique, data_type, original_file):
    encoded_file = f"{original_file}.{technique}"
    decoded_file = f"{encoded_file}.csv"

    # Construct dynamic filenames for encoding and decoding
    if technique == "dif":
        # C++ encoding and decoding commands for DIF
        # Python encoding and decoding scripts for DIF (previously in C++)
        encode_script = f"program-en-{technique}-{data_type}.py"
        decode_script = f"program-de-{technique}-{data_type}.py"

        encode_command = ["python", encode_script, original_file]
        decode_command = ["python", decode_script, encoded_file]
    else:
        # Python encoding and decoding scripts for other techniques
        encode_script = f"program-en-{technique}-{data_type}.py"
        decode_script = f"program-de-{technique}-{data_type}.py"

        encode_command = ["python", encode_script, original_file]
        decode_command = ["python", decode_script, encoded_file]

    # Encoding step
    start_time = time.time()
    subprocess.run(encode_command, check=True)
    encode_time = time.time() - start_time
    encoded_size = get_file_size(encoded_file)

    # Original file size and compression ratio
    original_size = get_file_size(original_file)
    compression_ratio = original_size / encoded_size if encoded_size > 0 else 0

    # Decoding step
    start_time = time.time()
    subprocess.run(decode_command, check=True)
    decode_time = time.time() - start_time
    decoded_size = get_file_size(decoded_file)

    # Return result
    return [technique, data_type, original_file, encoded_file, encoded_size, encode_time, decoded_file, decoded_size, decode_time, compression_ratio]


if __name__ == "__main__":
    print("Starting dynamic multi-core script...")
# List to store results
    results = []

    # Run tasks in parallel
    with ProcessPoolExecutor() as executor:
        futures = []
        for technique in compression_techniques:
            for data_type, files in data_files.items():
                for original_file in files:
                    futures.append(executor.submit(process_file, technique, data_type, original_file))

        for future in as_completed(futures):
            results.append(future.result())

    # Generate LaTeX table for results
    with open("comparison_table.tex", "w") as tex_file:
        tex_file.write("\\begin{table}[h!]\n")
        tex_file.write("\\centering\n")
        tex_file.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}\n")
        tex_file.write("\\hline\n")
        tex_file.write("Technique & Data Type & Original File & Encoded File & Encoded Size (bytes) & Encoding Time (s) & Compression Ratio & Decoded File & Decoding Time (s) \\\\\n")
        tex_file.write("\\hline\n")

        for row in results:
            technique, data_type, original_file, encoded_file, encoded_size, encode_time, decoded_file, decoded_size, decode_time, compression_ratio = row
            tex_file.write(f"{technique} & {data_type} & {original_file} & {encoded_file} & {encoded_size} & {encode_time:.4f} & {compression_ratio:.2f} & {decoded_file} & {decode_time:.4f} \\\\\n")
            tex_file.write("\\hline\n")

        tex_file.write("\\end{tabular}\n")
        tex_file.write("\\caption{Comparison of encoding and decoding times, sizes, and compression ratios for different compression techniques and data types}\n")
        tex_file.write("\\end{table}\n")

    print("Comparison table generated in 'comparison_table.tex'.")
