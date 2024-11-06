import sys
import struct

def encode_dif_int8(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = [int(line.strip()) for line in infile]
    
    with open(output_file, 'wb') as outfile:
        # Write the first value as the initial reference point
        outfile.write(struct.pack('b', data[0]))  # int8 reference value

        # Calculate and write differences
        for i in range(1, len(data)):
            delta = data[i] - data[i - 1]
            outfile.write(struct.pack('b', delta))  # int8 delta

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-dif-int8.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = f"{input_file}.dif"
    encode_dif_int8(input_file, output_file)
    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
