import sys
import struct

def decode_rle_int8(input_file):
    with open(input_file, 'rb') as infile:
        while True:
            value_bytes = infile.read(1)  # int8 value
            count_bytes = infile.read(1)  # unsigned int8 count
            if not value_bytes or not count_bytes:
                break
            value = struct.unpack('b', value_bytes)[0]
            count = struct.unpack('B', count_bytes)[0]
            for _ in range(count):
                print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-rle-int8.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_rle_int8(input_file)

if __name__ == "__main__":
    main()
