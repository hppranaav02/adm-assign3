import sys
import ast
import time

def encode_dictionary(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        data = [line.strip() for line in infile]
    
    dictionary = {}
    encoded_data = []
    index = 0

    for item in data:
        if item not in dictionary:
            dictionary[item] = index
            index += 1
        encoded_data.append(dictionary[item])

    with open(output_file, 'w', newline='') as outfile:
        outfile.write(f"{str(dictionary)}\n")
        for index in encoded_data:
            outfile.write(f"{index}\n")

def decode_dictionary(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        dictionary = ast.literal_eval(infile.readline().strip())
        reverse_dict = {v: k for k, v in dictionary.items()}
        encoded_data = [int(line.strip()) for line in infile]
    
    with open(output_file, 'w', newline='') as outfile:
        for index in encoded_data:
            outfile.write(f"{reverse_dict[index]}\n")
