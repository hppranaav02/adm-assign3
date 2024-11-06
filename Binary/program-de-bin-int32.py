import sys
import struct

def decode_bin_int32(input_file):
    with open(input_file, 'rb') as infile:
        while bytes_ := infile.read(4):  # Read 4 bytes at a time
            value = struct.unpack('>i', bytes_)[0]  # 'i' for int32
            print(value, end='\n')  # Unix-compatible newline

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-bin-int32.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_bin_int32(input_file)
