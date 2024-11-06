import sys
import struct

def decode_bin_int16(input_file):
    with open(input_file, 'rb') as infile:
        while bytes_ := infile.read(2):  # Read 2 bytes for int16
            value = struct.unpack('<h', bytes_)[0]
            print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-bin-int16.py <input_file>")
        return
    
    input_file = sys.argv[1]
    decode_bin_int16(input_file)

if __name__ == "__main__":
    main()
