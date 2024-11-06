import sys
import struct

def encode_rle_string(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = [line.strip() for line in infile]
    
    with open(output_file, 'wb') as outfile:
        i = 0
        while i < len(data):
            value = data[i]
            count = 1
            while i + 1 < len(data) and data[i + 1] == value:
                count += 1
                i += 1
            
            # Encode the string length and string itself, followed by count
            encoded_string = value.encode('utf-8')
            length = len(encoded_string)
            outfile.write(struct.pack('<H', length))       # Unsigned int16 for string length
            outfile.write(encoded_string)                  # Encoded string
            outfile.write(struct.pack('<I', count))        # Unsigned int32 for count
            i += 1

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-rle-string.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = f"{input_file}.rle"
    encode_rle_string(input_file, output_file)
    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
