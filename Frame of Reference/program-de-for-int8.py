import sys
import struct

def decode_for_int8(input_file):
    with open(input_file, 'rb') as infile:
        reference_value = struct.unpack('b', infile.read(1))[0]
        
        while byte := infile.read(1):  # Read each delta as int8
            delta = struct.unpack('b', byte)[0]
            original_value = reference_value + delta
            print(original_value, end='\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-for-int8.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_for_int8(input_file)
