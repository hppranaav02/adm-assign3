import sys
import struct

def decode_dif_int16(input_file):
    with open(input_file, 'rb') as infile:
        value = struct.unpack('<h', infile.read(2))[0]  # int16 reference value
        print(value)

        while bytes_ := infile.read(2):
            delta = struct.unpack('<h', bytes_)[0]
            value += delta
            print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-dif-int16.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_dif_int16(input_file)

if __name__ == "__main__":
    main()
