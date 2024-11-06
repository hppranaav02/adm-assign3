import sys
import struct

def decode_bin_int8(input_file):
    with open(input_file, 'rb') as infile:
        while byte := infile.read(1):  # Read 1 byte at a time
            value = struct.unpack('b', byte)[0]
            # Print directly to stdout with a Unix-compatible newline
            print(value, end='\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-bin-int8.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_bin_int8(input_file)

