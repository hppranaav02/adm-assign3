import sys
import struct

def decode_dif_int8(input_file):
    with open(input_file, 'rb') as infile:

        value = struct.unpack('b', infile.read(1))[0]
        print(value)

        while byte := infile.read(1):
            delta = struct.unpack('b', byte)[0]
            value += delta
            print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-dif-int8.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_dif_int8(input_file)

if __name__ == "__main__":
    main()
