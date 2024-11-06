import sys

def encode_bin_int32(input_file):
    output_file = f"{input_file}.bin"
    
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        for line in infile:
            value = int(line.strip())  # Convert line to integer
            outfile.write(value.to_bytes(4, byteorder='big', signed=True))

    print(f"Encoding completed for int32. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-en-bin-int32.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    encode_bin_int32(input_file)
