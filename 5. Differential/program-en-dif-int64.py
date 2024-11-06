import sys
import struct

def encode_dif_int64(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = [int(line.strip()) for line in infile]
    
    with open(output_file, 'wb') as outfile:
        outfile.write(struct.pack('<q', data[0]))  # int64 reference value

        for i in range(1, len(data)):
            delta = data[i] - data[i - 1]
            outfile.write(struct.pack('<q', delta))  # int64 delta

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-dif-int64.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = f"{input_file}.dif"
    encode_dif_int64(input_file, output_file)
    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
