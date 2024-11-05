import os
import sys
import time
import csv

from binary import BinaryEncoder
from dictionary import DictionaryEncoder
from differential import DifferentialEncoder
from frameofreference import FrameOfReferenceEncoder
from runlength import RunLengthEncoder

output_directory = "output_files"
os.makedirs(output_directory, exist_ok=True)

def read_input_data(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def read_encoded_data(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_encoded_data(file_path, encoded_data):
    with open(file_path, 'wb') as file:
        file.write(encoded_data)

def print_decoded_data(decoded_data):
    for item in decoded_data:
        print(item)

def main():
    if len(sys.argv) != 5:
        print("Error: Incorrect number of arguments.")
        print("Usage: program.py <en|de> <bin|rle|dic|for|dif> <int8|int16|int32|int64|string> <file_path>")
        sys.exit(1)

    mode, method, data_type, file_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    # Map of encoders based on method
    encoders = {
        'bin': BinaryEncoder(),
        'rle': RunLengthEncoder(),
        'dic': DictionaryEncoder(),
        'for': FrameOfReferenceEncoder(),
        'dif': DifferentialEncoder()
    }

    if method not in encoders:
        print("Error: Unsupported encoding method.")
        sys.exit(1)

    encoder = encoders[method]
    input_filename = os.path.basename(file_path)
    output_path = os.path.join(output_directory, f"{input_filename}.{method}")

    if mode == "en":
        # Encoding
        data = read_input_data(file_path)
        start_time = time.time()
        encoded_data = encoder.encode(data, data_type)
        encoding_time = time.time() - start_time
        write_encoded_data(output_path, encoded_data)
        print(f"Encoding completed in {encoding_time:.4f} seconds")
        print(f"Encoded data written to {output_path}")
        print(f"Original file size: {os.path.getsize(file_path)} bytes")
        print(f"Encoded file size: {os.path.getsize(output_path)} bytes")

    elif mode == "de":
        # Decoding
        if not os.path.exists(output_path):
            print(f"Error: Encoded file {output_path} does not exist.")
            sys.exit(1)
        
        encoded_data = read_encoded_data(output_path)
        start_time = time.time()
        decoded_data = encoder.decode(encoded_data, data_type)
        decoding_time = time.time() - start_time
        print(f"Decoding completed in {decoding_time:.4f} seconds")
        print_decoded_data(decoded_data)
    else:
        print("Error: Mode must be 'en' for encode or 'de' for decode.")
        sys.exit(1)

if __name__ == "__main__":
    main()
