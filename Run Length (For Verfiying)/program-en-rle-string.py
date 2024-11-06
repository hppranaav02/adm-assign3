import sys
import struct

def encode_rle_string(input_file):
    output_file = f"{input_file}.rle"
    
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        data = [line.strip() for line in infile]
        
        i = 0
        while i < len(data):
            value = data[i]
            count = 1
            while i + 1 < len(data) and data[i + 1] == value:
                count += 1
                i += 1
            encoded_string = value.encode('utf-8')
            length = len(encoded_string)
            outfile.write(struct.pack('<H', length))  # String length as unsigned int16
            outfile.write(encoded_string)  # Write the actual string
            outfile.write(struct.pack('<I', count))  # Unsigned int32 for count
            i += 1

    print(f"Encoding completed. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-en-rle-string.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    encode_rle_string(input_file)
