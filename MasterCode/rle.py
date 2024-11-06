import sys
import time

def encode_rle(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        data = [line.strip() for line in infile]

    encoded_data = []
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append(f"{data[i - 1]},{count}")
            count = 1
    encoded_data.append(f"{data[-1]},{count}")

    with open(output_file, 'w', newline='') as outfile:
        outfile.write("\n".join(encoded_data))

def decode_rle(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        data = [line.strip().split(",") for line in infile]
    
    decoded_data = []
    for value, count in data:
        decoded_data.extend([value] * int(count))

    with open(output_file, 'w', newline='') as outfile:
        outfile.write("\n".join(decoded_data))
