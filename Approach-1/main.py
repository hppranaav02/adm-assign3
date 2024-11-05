import sys
import os
import time
from pathlib import Path
from binary_encoding import BinaryEncoder
from run_length_encoding import RunLengthEncoder
from dictionary_encoding import DictionaryEncoder
from frame_of_reference_encoding import FrameOfReferenceEncoder
from differential_encoding import DifferentialEncoder
from experiments import read_input, write_bytes, read_bytes

# Dictionary of encoders
encoders = {
    "bin": BinaryEncoder(),
    "rle": RunLengthEncoder(),
    "dic": DictionaryEncoder(),
    "for": FrameOfReferenceEncoder(),
    "dif": DifferentialEncoder()
}

def invalid_input():
    """Prints usage instructions if input is invalid and exits."""
    print("Usage: main.py {en|de} {bin|rle|dic|for|dif} {int8|int16|int32|int64|string} <input_file>")
    sys.exit(-1)

def save_decoded_output(filename, decoded_data):
    """Saves decoded data to a CSV file."""
    output_path = filename + ".csv"
    with open(output_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        for item in decoded_data:
            writer.writerow([item])

def main():
    # Check if program is called with correct arguments
    if len(sys.argv) != 5:
        invalid_input()
    
    # Parse command-line arguments
    mode = sys.argv[1]  # "en" for encode, "de" for decode
    technique = sys.argv[2]  # Encoding technique (e.g., "bin", "rle")
    dtype = sys.argv[3]  # Data type (e.g., "int8", "string")
    input_file = sys.argv[4]  # Path to the input file
    
    # Validate mode
    if mode not in {"en", "de"}:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        invalid_input()
    
    # Validate technique
    if technique not in encoders:
        print("Invalid technique. Choose from 'bin', 'rle', 'dic', 'for', 'dif'.")
        invalid_input()
    
    # Validate data type
    valid_dtypes = {"int8", "int16", "int32", "int64", "string"}
    if dtype not in valid_dtypes:
        print("Invalid data type. Choose from 'int8', 'int16', 'int32', 'int64', 'string'.")
        invalid_input()
    
    # Select the encoder based on the technique
    encoder = encoders[technique]

    # Encoding
    if mode == "en":
        data = read_input(input_file)
        start_time = time.time()
        
        # Perform encoding
        encoded_data = encoder.encode(data, dtype)
        encoding_time = time.time() - start_time

        # Save encoded data
        output_file = input_file + f".{technique}"
        write_bytes(output_file, encoded_data)

        print(f"Encoding completed in {encoding_time:.3f} seconds.")
        print(f"Encoded file saved as: {output_file}")

    # Decoding
    elif mode == "de":
        # Ensure encoded file exists
        if not os.path.exists(input_file):
            print(f"Encoded file '{input_file}' does not exist.")
            sys.exit(-1)

        # Perform decoding
        encoded_data = read_bytes(input_file)
        start_time = time.time()
        decoded_data = encoder.decode(encoded_data, dtype)
        decoding_time = time.time() - start_time

        # Save decoded data to a CSV file
        output_file = input_file + ".csv"
        save_decoded_output(output_file, decoded_data)

        print(f"Decoding completed in {decoding_time:.3f} seconds.")
        print(f"Decoded file saved as: {output_file}")

if __name__ == "__main__":
    main()
