import sys
import os
import time
import csv
from pathlib import Path
from binary_encoding import BinaryEncoder
from run_length_encoding import RunLengthEncoder
from dictionary_encoding import DictionaryEncoder
from frame_of_reference_encoding import FrameOfReferenceEncoder
from differential_encoding import DifferentialEncoder

ENCODERS = {
    "bin": BinaryEncoder(),
    "rle": RunLengthEncoder(),
    "dic": DictionaryEncoder(),
    "for": FrameOfReferenceEncoder(),
    "dif": DifferentialEncoder()
}

VALID_DATA_TYPES = ["int8", "int16", "int32", "int64", "string"]


def invalid_input():
    """Prints usage instructions if the input is invalid and exits."""
    print(f"Usage: {sys.argv[0]} en|de <compression_technique> <data_type> <file_path>", file=sys.stderr)
    print("Example: main.py en bin int32 input.csv", file=sys.stderr)
    sys.exit(-1)


def read_input(file_path):
    """Reads data from a CSV file and returns a list of values."""
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.extend(row)  # Extend with values, assuming single column per row
    return data


def read_bytes(file_path):
    """Reads binary data from a file and returns it as a bytearray."""
    with open(file_path, 'rb') as f:
        return bytearray(f.read())


def write_bytes(file_path, data):
    """Writes binary data to a file."""
    with open(file_path, 'wb') as f:
        f.write(data)


def print_decoded_output(data):
    """Prints decoded data in a plain text format."""
    for item in data:
        print(item)


def main():
    # Validate command-line arguments
    if len(sys.argv) != 5:
        invalid_input()

    operation = sys.argv[1]  # en or de
    method = sys.argv[2]  # bin, rle, dic, for, dif
    dtype = sys.argv[3]  # int8, int16, int32, int64, string
    file_path = sys.argv[4]  # Path to the input file

    # Validate operation
    if operation not in ["en", "de"]:
        invalid_input()

    # Validate method and data type
    if method not in ENCODERS:
        invalid_input()
    if dtype not in VALID_DATA_TYPES:
        invalid_input()

    # Check compatibility of method and data type
    if dtype == "string" and method in ["bin", "for", "dif"]:
        print(f"Error: The '{method}' encoder does not support string data type.", file=sys.stderr)
        sys.exit(-1)

    encoder = ENCODERS[method]

    if operation == "en":
        # Encoding
        if not file_path.endswith(".csv"):
            print("Error: Input file for encoding must be a .csv file.", file=sys.stderr)
            sys.exit(-1)

        data = read_input(file_path)
        output_file = f"{file_path}.{method}"  # e.g., input.csv.bin

        start_time = time.time()
        encoded_data = encoder.encode(data, dtype)
        encoding_time = time.time() - start_time

        write_bytes(output_file, encoded_data)
        original_size = os.path.getsize(file_path)
        encoded_size = os.path.getsize(output_file)

        print(f"Encoding complete: {file_path} -> {output_file}")
        print(f"Data Type: {dtype}, Method: {method}")
        print(f"Original Size: {original_size} bytes, Encoded Size: {encoded_size} bytes")
        print(f"Encoding Time: {encoding_time:.4f} seconds")

    elif operation == "de":
        # Decoding
        if file_path.endswith(".csv"):
            print("Error: Input file for decoding must not end with .csv.", file=sys.stderr)
            sys.exit(-1)

        encoded_data = read_bytes(file_path)

        start_time = time.time()
        decoded_data = encoder.decode(encoded_data, dtype)
        decoding_time = time.time() - start_time

        print(f"Decoding complete: {file_path}")
        print(f"Data Type: {dtype}, Method: {method}")
        print(f"Decoding Time: {decoding_time:.4f} seconds")

        # Output decoded data as plain text to console
        print_decoded_output(decoded_data)


if __name__ == "__main__":
    main()
