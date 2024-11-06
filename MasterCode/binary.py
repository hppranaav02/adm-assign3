import sys
import struct
import time

def encode_binary(input_file, output_file):
    """Encodes integers using dynamic byte-width based on max value."""
    with open(input_file, 'r', newline='') as infile:
        data = [int(line.strip()) for line in infile]
    max_value = max(max(data), -min(data))
    if max_value < 2**7:
        size = 1
    elif max_value < 2**15:
        size = 2
    elif max_value < 2**31:
        size = 4
    else:
        size = 8

    encoded_data = bytearray(size.to_bytes(1, byteorder='big'))
    for number in data:
        encoded_data.extend(number.to_bytes(size, byteorder='big', signed=True))

    with open(output_file, 'wb') as outfile:
        outfile.write(encoded_data)

def decode_binary(input_file, output_file):
    with open(input_file, 'rb') as infile:
        size = int.from_bytes(infile.read(1), byteorder='big')
        data = []
        while chunk := infile.read(size):
            data.append(int.from_bytes(chunk, byteorder='big', signed=True))

    with open(output_file, 'w', newline='') as outfile:
        for number in data:
            outfile.write(f"{number}\n")
