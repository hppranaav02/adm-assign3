import sys
import struct

def decode_dif_int64(input_file):
    with open(input_file, 'rb') as infile:
        value = struct.unpack('<q', infile.read(8))[0]  # int64 reference value
        print(value)

        while bytes_ := infile.read(8):
            delta = struct.unpack('<q', bytes_)[0]
            value += delta
            print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-dif-int64.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_dif_int64(input_file)

if __name__ == "__main__":
    main()
