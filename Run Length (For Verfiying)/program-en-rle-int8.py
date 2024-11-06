import sys
import struct

def encode_rle_int8(input_file):
    output_file = f"{input_file}.rle"
    
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        data = [int(line.strip()) for line in infile]
        
        i = 0
        while i < len(data):
            value = data[i]
            count = 1
            while i + 1 < len(data) and data[i + 1] == value:
                count += 1
                i += 1
            # Write value and count as int8
            outfile.write(struct.pack('b', value))
            outfile.write(struct.pack('B', count))  # Unsigned int8 for count
            i += 1

    print(f"Encoding completed. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-en-rle-int8.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    encode_rle_int8(input_file)
