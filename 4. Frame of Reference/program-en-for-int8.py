import sys
import struct

def encode_for_int8(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = [int(line.strip()) for line in infile]

    reference_value = min(data)
    deltas = [value - reference_value for value in data]

    with open(output_file, 'wb') as outfile:
        # Write reference value
        outfile.write(struct.pack('b', reference_value))  # int8 reference
        # Write deltas
        for delta in deltas:
            outfile.write(struct.pack('b', delta))  # int8 delta

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-for-int8.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = f"{input_file}.for"
    encode_for_int8(input_file, output_file)
    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
