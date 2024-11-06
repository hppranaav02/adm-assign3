import sys
import struct

def encode_for_int32(input_file):
    output_file = f"{input_file}.for"
    
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        data = [int(line.strip()) for line in infile]
        reference_value = min(data)
        
        # Write reference value
        outfile.write(struct.pack('<i', reference_value))  # Little-endian int32
        
        for value in data:
            delta = value - reference_value
            outfile.write(struct.pack('<i', delta))  # Store each delta as int32

    print(f"Encoding completed. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-en-for-int32.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    encode_for_int32(input_file)
