import sys
import struct

def encode_rle_int64(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = [int(line.strip()) for line in infile]
    
    with open(output_file, 'wb') as outfile:
        i = 0
        while i < len(data):
            value = data[i]
            count = 1
            while i + 1 < len(data) and data[i + 1] == value:
                count += 1
                i += 1
            
            outfile.write(struct.pack('<q', value))   # int64 value
            outfile.write(struct.pack('<Q', count))   # unsigned int64 count
            i += 1

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-rle-int64.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = f"{input_file}.rle"
    encode_rle_int64(input_file, output_file)
    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
