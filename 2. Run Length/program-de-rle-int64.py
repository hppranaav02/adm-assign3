import sys
import struct

def decode_rle_int64(input_file):
    with open(input_file, 'rb') as infile:
        while True:
            value_bytes = infile.read(8)  # int64 value
            count_bytes = infile.read(8)  # unsigned int64 count
            if not value_bytes or not count_bytes:
                break
            value = struct.unpack('<q', value_bytes)[0]
            count = struct.unpack('<Q', count_bytes)[0]
            for _ in range(count):
                print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-rle-int64.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_rle_int64(input_file)

if __name__ == "__main__":
    main()
