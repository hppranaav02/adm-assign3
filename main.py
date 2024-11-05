#!/usr/bin/python3

import sys
import time
import csv
from binary_encoding import BinaryEncoder
from run_length_encoding import RunLengthEncoder
from dictionary_encoding import DictionaryEncoder
from frame_of_reference_encoding import FrameOfReferenceEncoder
from differential_encoding import DifferentialEncoder

def invalid_input():
    """Prints usage instructions and exits with an error code."""
    print(f"Usage: {sys.argv[0]} {{en|de}} {{bin|rle|dic|for|dif}} {{int8|int16|int32|int64|string}} <path>.csv", file=sys.stderr)
    exit(-1)

def read_input(filename):
    """Reads input CSV file and returns a list of data items."""
    data = []
    with open(filename, 'r') as f:
        for row in csv.reader(f):
            data.extend(row)  # Assumes single column data
    return [int(item) if item.isdigit() else item for item in data]

def read_bytes(filename):
    """Reads encoded binary data from a file."""
    with open(filename, 'rb') as f:
        return f.read()

def write_bytes(filename, data):
    """Writes binary data to a file."""
    with open(filename, 'wb') as f:
        f.write(data)

def print_decoded_output(data):
    """Prints decoded data to stdout, line by line."""
    for item in data:
        print(item)

def main():
    # Validate command-line arguments
    if len(sys.argv) != 5:
        invalid_input()
    
    action, method, dtype, filepath = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    if action not in {"en", "de"} or method not in {"bin", "rle", "dic", "for", "dif"} or dtype not in {"int8", "int16", "int32", "int64", "string"}:
        invalid_input()

    # Map method argument to the appropriate encoder class
    encoders = {
        "bin": BinaryEncoder(),
        "rle": RunLengthEncoder(),
        "dic": DictionaryEncoder(),
        "for": FrameOfReferenceEncoder(),
        "dif": DifferentialEncoder()
    }

    encoder = encoders[method]

    # Perform encoding or decoding based on action
    if action == "en":
        data = read_input(filepath)
        start_time = time.time()
        encoded_data = encoder.encode(data, dtype)
        print(f"Encoding {filepath} took {time.time() - start_time:.3f} seconds using the {method} algorithm.", file=sys.stderr)
        write_bytes(f"{filepath}.{method}", encoded_data)
    
    elif action == "de":
        encoded_data = read_bytes(filepath)
        start_time = time.time()
        decoded_data = encoder.decode(encoded_data, dtype)
        print(f"Decoding {filepath} took {time.time() - start_time:.3f} seconds using the {method} algorithm.", file=sys.stderr)
        print_decoded_output(decoded_data)

if __name__ == "__main__":
    main()
