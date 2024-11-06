import sys
import struct

def encode_for_int64(input_file):
    output_file = f"{input_file}.for"
    
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        data = [int(line.strip()) for line in infile]
        reference_value = min(data)
        
        # Write reference value
        outfile.write(struct.pack('<q', reference_value))  # Little-endian int64
        
        for value in data:
            delta = value - reference_value
            outfile.write(struct.pack('<q', delta))  # Store each delta as int64

    print(f"Encoding completed. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-en-for-int64.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    encode_for_int64(input_file)
