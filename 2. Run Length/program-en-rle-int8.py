import sys
import struct

def encode_rle_int8(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = [int(line.strip()) for line in infile]
    
    with open(output_file, 'wb') as outfile:
        i = 0
        while i < len(data):
            value = data[i]
            count = 1
            # Count consecutive occurrences of the same value
            while i + 1 < len(data) and data[i + 1] == value:
                count += 1
                i += 1
            
            # Write the value and count as int8 and unsigned int8
            outfile.write(struct.pack('b', value))   # int8 value
            outfile.write(struct.pack('B', count))   # unsigned int8 count
            i += 1

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-rle-int8.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = f"{input_file}.rle"
    encode_rle_int8(input_file, output_file)
    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
