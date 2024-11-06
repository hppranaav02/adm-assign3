import sys
import time

def encode_for(input_file, output_file):
    """Encodes a CSV file using frame of reference encoding."""
    offsets = []
    reference_value = None

    start_time = time.time()
    with open(input_file, 'r') as infile:
        values = [int(line.strip()) for line in infile]  # Read all values into a list
        reference_value = min(values)  # Set the reference as the minimum value

        # Calculate offsets from the reference value
        for value in values:
            offsets.append(value - reference_value)

    # Write reference and offsets to the output file
    with open(output_file, 'w') as outfile:
        outfile.write(f"{reference_value}\n")  # Write reference value at the top
        for offset in offsets:
            outfile.write(f"{offset}\n")

    end_time = time.time()
    print(f"Encoding time for {input_file}: {end_time - start_time:.6f} seconds")

def decode_for(input_file, output_file):
    """Decodes a file that was encoded with frame of reference encoding."""
    start_time = time.time()
    with open(input_file, 'r') as infile:
        reference_value = int(infile.readline().strip())  # First line is the reference value
        offsets = [int(line.strip()) for line in infile]  # Read all offsets

    with open(output_file, 'w') as outfile:
        for offset in offsets:
            outfile.write(f"{reference_value + offset}\n")  # Reconstruct original values

    end_time = time.time()
    print(f"Decoding time for {input_file}: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: forf.py <en|de> <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]  # 'en' for encode, 'de' for decode
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == 'en':
        encode_for(input_file, output_file)
    elif mode == 'de':
        decode_for(input_file, output_file)
    else:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        sys.exit(1)
