import sys
import struct

def decode_rle_string(input_file):
    with open(input_file, 'rb') as infile:
        while True:
            length_bytes = infile.read(2)   
            if not length_bytes:
                break
            length = struct.unpack('<H', length_bytes)[0]
            encoded_string = infile.read(length)           
            value = encoded_string.decode('utf-8')
            count = struct.unpack('<I', infile.read(4))[0]  

            for _ in range(count):
                print(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-rle-string.py <input_file>")
        return

    input_file = sys.argv[1]
    decode_rle_string(input_file)

if __name__ == "__main__":
    main()
