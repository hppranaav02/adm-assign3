import sys
import struct

def decode_rle_int16(input_file):
    with open(input_file, 'rb') as infile:
        while True:
            value_bytes = infile.read(2)  
            count_bytes = infile.read(2)  
            if not value_bytes or not count_bytes:
                break
            value = struct.unpack('<h', value_bytes)[0]
            count = struct.unpack('<H', count_bytes)[0]
            for _ in range(count):
                print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-rle-int16.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_rle_int16(input_file)

if __name__ == "__main__":
    main()
