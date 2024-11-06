import sys
import time

def encode_differential(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        data = [int(line.strip()) for line in infile]

    encoded_data = [data[0]]
    for i in range(1, len(data)):
        encoded_data.append(data[i] - data[i - 1])

    with open(output_file, 'w', newline='') as outfile:
        for value in encoded_data:
            outfile.write(f"{value}\n")

def decode_differential(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        data = [int(line.strip()) for line in infile]
    
    decoded_data = [data[0]]
    for i in range(1, len(data)):
        decoded_data.append(decoded_data[-1] + data[i])

    with open(output_file, 'w', newline='') as outfile:
        for number in decoded_data:
            outfile.write(f"{number}\n")
