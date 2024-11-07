import sys
import json

def load_encoded_data(file_path):
    """Load encoded content and dictionary from the specified file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    encoded_line = lines[1].strip()
    encoded_content = [int(code) for code in encoded_line.split()]
   
    dict_start_index = lines.index("Encoding Dictionary:\n") + 1
    dictionary_content = "".join(lines[dict_start_index:])
    encoding_dict = json.loads(dictionary_content)

    decoding_dict = {code: value for value, code in encoding_dict.items()}
    return encoded_content, decoding_dict

def decode_content(encoded_content, decoding_dict):
    """Rebuild the original int64 values using the decoding dictionary."""
    return [decoding_dict[code] for code in encoded_content]

def main():
    if len(sys.argv) < 2:
        print("Usage: python program-de-dic-int64.py <encoded_file_path>")
        return

    encoded_file_path = sys.argv[1]
    
    encoded_content, decoding_dict = load_encoded_data(encoded_file_path)

    decoded_content = decode_content(encoded_content, decoding_dict)

    for value in decoded_content:
        print(value)

if __name__ == "__main__":
    main()
