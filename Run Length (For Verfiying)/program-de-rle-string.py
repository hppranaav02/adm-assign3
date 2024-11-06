import sys
import struct

def decode_rle_string(input_file):
    with open(input_file, 'rb') as infile:
        while length_bytes := infile.read(2):  # Read string length as unsigned int16
            length = struct.unpack('<H', length_bytes)[0]
            encoded_string = infile.read(length)  # Read the string
            value = encoded_string.decode('utf-8')
            count = struct.unpack('<I', infile.read(4))[0]  # Unsigned int32 for count
            for _ in range(count):
                print(value, end='\n')  # Print each string `count` times

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-rle-string.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_rle_string(input_file)
