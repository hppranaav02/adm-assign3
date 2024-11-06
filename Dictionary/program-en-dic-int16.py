import sys
import json
import struct

def build_dictionary(data):
    unique_values = list(dict.fromkeys(data))
    encoding_dict = {value: index for index, value in enumerate(unique_values)}
    encoded_data = [encoding_dict[value] for value in data]
    return encoding_dict, encoded_data

def write_encoded_file(output_path, encoded_content, encoding_dict):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Encoded Content:\n")
        f.write(" ".join(map(str, encoded_content)) + "\n")
        f.write("Encoding Dictionary:\n")
        f.write(json.dumps(encoding_dict, ensure_ascii=False, indent=2))

def main():
    if len(sys.argv) != 2:
        print("Usage: python program-en-dic-int16.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = f"{input_file}.dic"

    with open(input_file, 'r') as f:
        data = [int(line.strip()) for line in f]

    encoding_dict, encoded_content = build_dictionary(data)
    write_encoded_file(output_file, encoded_content, encoding_dict)

    print(f"Encoded data saved to {output_file}")

if __name__ == "__main__":
    main()
