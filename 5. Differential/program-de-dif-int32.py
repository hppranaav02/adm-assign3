import sys
import struct

def decode_dif_int32(input_file):
    with open(input_file, 'rb') as infile:
        value = struct.unpack('<i', infile.read(4))[0]  
        print(value)

        while bytes_ := infile.read(4):
            delta = struct.unpack('<i', bytes_)[0]
            value += delta
            print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-dif-int32.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_dif_int32(input_file)

if __name__ == "__main__":
    main()
