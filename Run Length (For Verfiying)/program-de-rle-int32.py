import sys
import struct

def rle_decode(encoded_data):
    decoded = []
    for value, count in encoded_data:
        decoded.extend([value] * count)
    return decoded

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-rle-int32.py <encoded_file>")
        sys.exit(1)

    encoded_file = sys.argv[1]

    encoded_data = []
    with open(encoded_file, 'rb') as f:
        while True:
            value_bytes = f.read(4)  # int32 for value
            count_bytes = f.read(4)  # unsigned int32 for count
            if not value_bytes or not count_bytes:
                break
            value = struct.unpack('<i', value_bytes)[0]
            count = struct.unpack('<I', count_bytes)[0]
            encoded_data.append((value, count))

    decoded_data = rle_decode(encoded_data)

    for value in decoded_data:
        print(value)

if __name__ == "__main__":
    main()
