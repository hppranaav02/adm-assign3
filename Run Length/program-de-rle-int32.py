import sys
import struct

def decode_rle_int32(input_file):
    with open(input_file, 'rb') as infile:
        while True:
            value_bytes = infile.read(4)  # int32 value
            count_bytes = infile.read(4)  # unsigned int32 count
            if not value_bytes or not count_bytes:
                break
            value = struct.unpack('<i', value_bytes)[0]
            count = struct.unpack('<I', count_bytes)[0]
            for _ in range(count):
                print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-rle-int32.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_rle_int32(input_file)

if __name__ == "__main__":
    main()
