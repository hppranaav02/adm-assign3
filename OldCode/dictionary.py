import sys
import time
import pickle

def encode_dictionary(input_file, output_file):
    dictionary = {}
    encoded_data = []

    start_time = time.time()
    with open(input_file, 'r') as infile:
        for line in infile:
            value = line.strip()
            if value not in dictionary:
                dictionary[value] = len(dictionary)  
            encoded_data.append(dictionary[value])

    with open(output_file, 'wb') as outfile:
        pickle.dump((dictionary, encoded_data), outfile)

    end_time = time.time()
    print(f"Encoding time for {input_file}: {end_time - start_time:.6f} seconds")

def decode_dictionary(input_file, output_file):
    """Decodes a file that was encoded with dictionary encoding."""
    start_time = time.time()
    with open(input_file, 'rb') as infile:
        dictionary, encoded_data = pickle.load(infile)  

    reverse_dict = {index: value for value, index in dictionary.items()}  

    with open(output_file, 'w') as outfile:
        for index in encoded_data:
            outfile.write(f"{reverse_dict[index]}\n")

    end_time = time.time()
    print(f"Decoding time for {input_file}: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: dictionary.py <en|de> <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]  
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == 'en':
        encode_dictionary(input_file, output_file)
    elif mode == 'de':
        decode_dictionary(input_file, output_file)
    else:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        sys.exit(1)
