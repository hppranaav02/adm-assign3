import sys
import struct
import time

def encode_binary(input_file, output_file, data_type):
    """Encodes a CSV file of integers to binary format."""
    # Data type size mapping
    type_format = {
        "int8": 'b',   # 1 byte
        "int16": 'h',  # 2 bytes
        "int32": 'i',  # 4 bytes
        "int64": 'q'   # 8 bytes
    }

    if data_type not in type_format:
        raise ValueError(f"Unsupported data type {data_type} for binary encoding.")

    start_time = time.time()
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        for line in infile:
            number = int(line.strip())  # Read integer from CSV line
            packed_data = struct.pack(type_format[data_type], number)
            outfile.write(packed_data)  # Write binary data to output file
    end_time = time.time()
    print(f"Encoding time for {input_file}: {end_time - start_time:.6f} seconds")

def decode_binary(input_file, output_file, data_type):
    """Decodes a binary file back to its original integer format."""
    type_format = {
        "int8": 'b',   # 1 byte
        "int16": 'h',  # 2 bytes
        "int32": 'i',  # 4 bytes
        "int64": 'q'   # 8 bytes
    }

    if data_type not in type_format:
        raise ValueError(f"Unsupported data type {data_type} for binary decoding.")

    data_size = struct.calcsize(type_format[data_type])

    start_time = time.time()
    with open(input_file, 'rb') as infile, open(output_file, 'w') as outfile:
        while byte := infile.read(data_size):
            number = struct.unpack(type_format[data_type], byte)[0]
            outfile.write(f"{number}\n")
    end_time = time.time()
    print(f"Decoding time for {input_file}: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: binary.py <en|de> <data_type> <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]  # 'en' for encode, 'de' for decode
    data_type = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4]

    if mode == 'en':
        encode_binary(input_file, output_file, data_type)
    elif mode == 'de':
        decode_binary(input_file, output_file, data_type)
    else:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        sys.exit(1)
