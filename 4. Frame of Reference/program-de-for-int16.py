import sys
import struct

def decode_for_int16(input_file):
    with open(input_file, 'rb') as infile:
        reference_value = struct.unpack('<h', infile.read(2))[0]

        while bytes_ := infile.read(2):
            delta = struct.unpack('<h', bytes_)[0]
            original_value = reference_value + delta
            print(original_value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-for-int16.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_for_int16(input_file)

if __name__ == "__main__":
    main()
