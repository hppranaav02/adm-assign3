import sys
import struct

def decode_for_int8(input_file):
    with open(input_file, 'rb') as infile:
        reference_value = struct.unpack('b', infile.read(1))[0]

        while byte := infile.read(1):
            delta = struct.unpack('b', byte)[0]
            original_value = reference_value + delta
            print(original_value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-for-int8.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_for_int8(input_file)

if __name__ == "__main__":
    main()
