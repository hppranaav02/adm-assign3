import sys
import time

def encode_differential(input_file, output_file):
    """Encodes a CSV file using differential encoding."""
    encoded_data = []
    previous_value = None

    start_time = time.time()
    with open(input_file, 'r') as infile:
        for line in infile:
            current_value = int(line.strip())
            if previous_value is None:
                encoded_data.append(current_value)  # First value is stored as-is
            else:
                encoded_data.append(current_value - previous_value)  # Store the difference
            previous_value = current_value

    with open(output_file, 'w') as outfile:
        for value in encoded_data:
            outfile.write(f"{value}\n")

    end_time = time.time()
    print(f"Encoding time for {input_file}: {end_time - start_time:.6f} seconds")

def decode_differential(input_file, output_file):
    """Decodes a file that was encoded with differential encoding."""
    decoded_data = []
    previous_value = None

    start_time = time.time()
    with open(input_file, 'r') as infile:
        for line in infile:
            delta = int(line.strip())
            if previous_value is None:
                decoded_data.append(delta)  # First value is stored as-is
                previous_value = delta
            else:
                current_value = previous_value + delta
                decoded_data.append(current_value)
                previous_value = current_value

    with open(output_file, 'w') as outfile:
        for value in decoded_data:
            outfile.write(f"{value}\n")

    end_time = time.time()
    print(f"Decoding time for {input_file}: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: differential.py <en|de> <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]  # 'en' for encode, 'de' for decode
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == 'en':
        encode_differential(input_file, output_file)
    elif mode == 'de':
        decode_differential(input_file, output_file)
    else:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        sys.exit(1)
