import sys
import time

def encode_rle(input_file, output_file):
    """Encodes a CSV file using run-length encoding."""
    encoded_data = []

    start_time = time.time()
    with open(input_file, 'r') as infile:
        previous_value = None
        count = 0

        for line in infile:
            value = line.strip()
            if value == previous_value:
                count += 1  # Increment count if the same value repeats
            else:
                if previous_value is not None:
                    encoded_data.append((previous_value, count))  # Store the previous value and count
                previous_value = value
                count = 1  # Reset count for the new value

        # Append the last value and count
        if previous_value is not None:
            encoded_data.append((previous_value, count))

    # Write encoded data to output file
    with open(output_file, 'w') as outfile:
        for value, count in encoded_data:
            outfile.write(f"{value},{count}\n")

    end_time = time.time()
    print(f"Encoding time for {input_file}: {end_time - start_time:.6f} seconds")

def decode_rle(input_file, output_file):
    """Decodes a file that was encoded with run-length encoding."""
    start_time = time.time()
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            value, count = line.strip().split(',')
            count = int(count)
            for _ in range(count):
                outfile.write(f"{value}\n")  # Write the value 'count' times

    end_time = time.time()
    print(f"Decoding time for {input_file}: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: rle.py <en|de> <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]  # 'en' for encode, 'de' for decode
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == 'en':
        encode_rle(input_file, output_file)
    elif mode == 'de':
        decode_rle(input_file, output_file)
    else:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        sys.exit(1)
