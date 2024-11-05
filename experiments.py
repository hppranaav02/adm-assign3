import os
import time
import csv
import sys
from pathlib import Path
from binary_encoding import BinaryEncoder
from run_length_encoding import RunLengthEncoder
from dictionary_encoding import DictionaryEncoder
from frame_of_reference_encoding import FrameOfReferenceEncoder
from differential_encoding import DifferentialEncoder
from main import read_input, write_bytes, read_bytes

# Paths for input and output
INPUT_DIR = "D:\CSE\GitHub\ADM-A3 Data Folder\Input Data"
ENCODED_OUTPUT_DIR = "D:\CSE\GitHub\ADM-A3 Data Folder\Encoded Data"
DECODED_OUTPUT_DIR = "D:\CSE\GitHub\ADM-A3 Data Folder\Decoded Data"
MASTER_CODE_DIR = "MasterCode"

# Ensure output directories exist
Path(ENCODED_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(DECODED_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# List of encoding techniques
encoders = {
    "bin": BinaryEncoder(),
    "rle": RunLengthEncoder(),
    "dic": DictionaryEncoder(),
    "for": FrameOfReferenceEncoder(),
    "dif": DifferentialEncoder()
}

# List of data types supported by the assignment
data_types = ["int8", "int16", "int32", "int64", "string"]

# Metrics output file
metrics_file = os.path.join(ENCODED_OUTPUT_DIR, "metrics.csv")

def save_decoded_output(filename, decoded_data):
    """Saves decoded output to a CSV file in the DECODED_OUTPUT_DIR."""
    decoded_filepath = os.path.join(DECODED_OUTPUT_DIR, filename)
    with open(decoded_filepath, mode='w', newline='') as f:
        writer = csv.writer(f)
        for item in decoded_data:
            writer.writerow([item])

def run_experiments():
    """Runs encoding and decoding experiments on all input files using all encoding techniques."""
    # Prepare metrics file
    with open(metrics_file, mode='w', newline='') as metrics:
        writer = csv.writer(metrics)
        writer.writerow(["Filename", "Technique", "DataType", 
                         "EncodingTime(s)", "DecodingTime(s)", 
                         "OriginalSize(Bytes)", "EncodedSize(Bytes)", 
                         "DecodedCorrect"])

        # Iterate over all files in the input directory
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".csv"):
                filepath = os.path.join(INPUT_DIR, filename)
                data = read_input(filepath)
                original_size = os.path.getsize(filepath)

                # Run each encoding method on the file
                for method, encoder in encoders.items():
                    for dtype in data_types:
                        # Skip incompatible data types for certain encoders
                        if dtype == "string" and method in ["bin", "rle", "for", "dif"]:
                            continue
                        if dtype != "string" and any(not str(item).isdigit() for item in data):
                            continue

                        try:
                            # Encode
                            start_time = time.time()
                            encoded_data = encoder.encode(data, dtype)
                            encoding_time = time.time() - start_time
                            
                            # Save encoded file
                            encoded_filename = f"{filename}.{method}"
                            encoded_filepath = os.path.join(ENCODED_OUTPUT_DIR, encoded_filename)
                            write_bytes(encoded_filepath, encoded_data)
                            encoded_size = os.path.getsize(encoded_filepath)

                            # Decode
                            start_time = time.time()
                            decoded_data = encoder.decode(encoded_data, dtype)
                            decoding_time = time.time() - start_time

                            # Verify decoded data
                            decoded_correct = decoded_data == data

                            # Save decoded data to a separate CSV file
                            decoded_filename = f"{filename}.{method}.decoded.csv"
                            save_decoded_output(decoded_filename, decoded_data)

                            # Write metrics
                            writer.writerow([filename, method, dtype, 
                                             encoding_time, decoding_time, 
                                             original_size, encoded_size, 
                                             decoded_correct])
                            
                        except Exception as e:
                            print(f"Error processing {filename} with {method} encoding and {dtype} dtype: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_experiments()
