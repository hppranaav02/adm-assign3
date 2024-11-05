import sys
import csv
import os
import time
from Binary import BinaryDataCompressor
from Dictionary import DictionaryCompressor
from Differential import DifferentialCompressor
from FrameofReference import FrameOfReferenceCompressor
from RunLength import RunLengthCompressor
import pickle

def print_usage():
    print("Usage: program.py <en|de> <bin|rle|dic|for|dif> <int8|int16|int32|int64|string> <file_path>")
    sys.exit(1)

def read_csv_data(file_path):
    """Reads a single-column CSV file and returns a list of values."""
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = [row[0] for row in reader]
    return data

def write_encoded_data(file_path, data):
    """Writes binary encoded data to a file."""
    with open(file_path, 'wb') as file:
        file.write(data)

def read_encoded_data(file_path):
    """Reads binary encoded data from a file."""
    with open(file_path, 'rb') as file:
        return file.read()

def print_decoded_data(data):
    """Outputs decoded data to the console (stdout) in plain text."""
    for item in data:
        print(item)

def main():
    if len(sys.argv) != 5:
        print("Error: Incorrect number of arguments.")
        print_usage()

    operation, method, data_type, file_path = sys.argv[1:]

    # Verify arguments
    if operation not in ["en", "de"]:
        print("Error: Operation must be 'en' or 'de'.")
        print_usage()
    if method not in ["bin", "rle", "dic", "for", "dif"]:
        print("Error: Compression method must be one of 'bin', 'rle', 'dic', 'for', or 'dif'.")
        print_usage()
    if data_type not in ["int8", "int16", "int32", "int64", "string"]:
        print("Error: Data type must be one of 'int8', 'int16', 'int32', 'int64', or 'string'.")
        print_usage()

    # Select the appropriate compressor based on the method
    if method == "bin":
        compressor = BinaryDataCompressor()
    elif method == "rle":
        compressor = RunLengthCompressor()
    elif method == "dic":
        compressor = DictionaryCompressor()
    elif method == "for":
        compressor = FrameOfReferenceCompressor()
    elif method == "dif":
        compressor = DifferentialCompressor()
    else:
        raise ValueError("Unsupported compression method.")

    # Perform encoding or decoding
    if operation == "en":
        # Read data and encode
        data = read_csv_data(file_path)
        
        # Convert data to appropriate type if integer
        if data_type != "string":
            data = list(map(int, data))

        start_time = time.time()
        
        # Compress based on selected method
        if method == "dic":
            dictionary, encoded_data = compressor.compress(data)
            output_data = (dictionary, encoded_data)
        elif method in ["for", "dif"]:
            reference, adjusted_values = compressor.compress(data)
            output_data = (reference, adjusted_values)
        else:
            output_data = compressor.compress(data, data_type)

        elapsed_time = time.time() - start_time
        print(f"Encoding completed in {elapsed_time:.4f} seconds")

        # Write encoded data to file with appropriate suffix
        encoded_file_path = f"{file_path}.{method}"
        if method in ["dic", "for", "dif"]:
            with open(encoded_file_path, 'wb') as f:
                pickle.dump(output_data, f)
        else:
            write_encoded_data(encoded_file_path, output_data)

        print(f"Encoded data written to {encoded_file_path}")
        print(f"Original file size: {os.path.getsize(file_path)} bytes")
        print(f"Encoded file size: {os.path.getsize(encoded_file_path)} bytes")

    elif operation == "de":
        # Read encoded data and decode
        start_time = time.time()

        if method in ["dic", "for", "dif"]:
            with open(file_path, 'rb') as f:
                encoded_data = pickle.load(f)
            if method == "dic":
                decoded_data = compressor.decompress(*encoded_data)
            else:
                decoded_data = compressor.decompress(encoded_data[0], encoded_data[1])
        else:
            encoded_data = read_encoded_data(file_path)
            decoded_data = compressor.decompress(encoded_data, data_type)

        elapsed_time = time.time() - start_time
        print(f"Decoding completed in {elapsed_time:.4f} seconds")

        # Output decoded data to stdout in plain text format
        print_decoded_data(decoded_data)

        # Report sizes
        print(f"Encoded file size: {os.path.getsize(file_path)} bytes")
        print(f"Decoded output (original format): displayed on stdout")

if __name__ == "__main__":
    main()
