import sys
import struct

def rle_encode(data):
    encoded = []
    count = 1
    
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded.append((data[i - 1], count))
            count = 1
    encoded.append((data[-1], count))
    return encoded

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-rle-int32.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = f"{input_file}.rle"

    with open(input_file, 'r') as f:
        data = [int(line.strip()) for line in f]

    encoded_data = rle_encode(data)

    with open(output_file, 'wb') as f:
        for value, count in encoded_data:
            f.write(struct.pack('<i', value))  # int32 value
            f.write(struct.pack('<I', count))  # unsigned int32 count

    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
