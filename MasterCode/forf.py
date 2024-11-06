import sys
import time

def encode_for(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        data = [int(line.strip()) for line in infile]
    
    reference = data[0]
    threshold = 999
    encoded_data = [f"N{reference}"]

    for i in range(1, len(data)):
        offset = data[i] - reference
        if abs(offset) > threshold:
            reference = data[i]
            encoded_data.append(f"N{reference}")
        else:
            encoded_data.append(str(offset))

    with open(output_file, 'w', newline='') as outfile:
        outfile.write("\n".join(encoded_data))

def decode_for(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        data = [line.strip() for line in infile]
    
    decoded_data = []
    for item in data:
        if item.startswith("N"):
            reference = int(item[1:])
            decoded_data.append(reference)
        else:
            decoded_data.append(reference + int(item))
    
    with open(output_file, 'w', newline='') as outfile:
        for value in decoded_data:
            outfile.write(f"{value}\n")
