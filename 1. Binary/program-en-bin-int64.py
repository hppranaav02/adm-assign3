import sys
import struct

def encode_bin_int64(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        for line in infile:
            value = int(line.strip())
            outfile.write(struct.pack('<q', value))  # '<q' for little-endian int64

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-bin-int64.py <input_file>")
        return
    
    input_file = sys.argv[1]
    output_file = f"{input_file}.bin"
    encode_bin_int64(input_file, output_file)
    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()