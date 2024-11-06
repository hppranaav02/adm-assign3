import sys
import struct

def decode_rle_int8(input_file):
    with open(input_file, 'rb') as infile:
        while byte := infile.read(1):  # Read value as int8
            value = struct.unpack('b', byte)[0]
            count = struct.unpack('B', infile.read(1))[0]  # Unsigned int8 for count
            for _ in range(count):
                print(value, end='\n')  # Print each value `count` times

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-rle-int8.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_rle_int8(input_file)
