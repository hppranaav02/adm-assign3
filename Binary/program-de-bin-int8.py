import sys
import struct

def decode_bin_int8(input_file):
    with open(input_file, 'rb') as infile:
        while byte := infile.read(1):  # Read 1 byte for int8
            value = struct.unpack('b', byte)[0]
            print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-bin-int8.py <input_file>")
        return
    
    input_file = sys.argv[1]
    decode_bin_int8(input_file)

if __name__ == "__main__":
    main()
