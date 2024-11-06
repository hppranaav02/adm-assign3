import sys
import struct

def rle_decode(encoded_data):
    """Decode RLE-encoded data to its original integer form."""
    decoded = []
    for value, count in encoded_data:
        decoded.extend([value] * count)  # Repeat `value` for `count` times
    return decoded

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-de-rle-int64.py <encoded_file>")
        sys.exit(1)

    encoded_file = sys.argv[1]

    # Step 1: Read the encoded data
    encoded_data = []
    with open(encoded_file, 'rb') as f:
        while True:
            value_bytes = f.read(8)  # int64 for value
            count_bytes = f.read(8)  # unsigned int64 for count
            if not value_bytes or not count_bytes:
                break
            value = struct.unpack('<q', value_bytes)[0]
            count = struct.unpack('<Q', count_bytes)[0]
            encoded_data.append((value, count))

    # Step 2: Decode the data
    decoded_data = rle_decode(encoded_data)

    # Step 3: Print the decoded data line-by-line
    for value in decoded_data:
        print(value)

if __name__ == "__main__":
    main()
