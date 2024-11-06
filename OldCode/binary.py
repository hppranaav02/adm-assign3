import sys
import struct

def encode_binary(input_file, output_file, data_type):
    print(f"Encoding {input_file} to {output_file} as {data_type}")
    type_formats = {
        "int8": ('b', 1),
        "int16": ('<h', 2),
        "int32": ('<i', 4),
        "int64": ('<q', 8)
    }

    if data_type not in type_formats:
        raise ValueError(f"Unsupported data type {data_type} for binary encoding.")

    format_char, byte_size = type_formats[data_type]

    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        for line in infile:
            value = int(line.strip())
            outfile.write(struct.pack(format_char, value))

def decode_binary(input_file, data_type, output_file=None):
    print(f"Decoding {input_file} as {data_type}, output to {'console' if not output_file else output_file}")
    type_formats = {
        "int8": ('b', 1),
        "int16": ('<h', 2),
        "int32": ('<i', 4),
        "int64": ('<q', 8)
    }

    if data_type not in type_formats:
        raise ValueError(f"Unsupported data type {data_type} for binary decoding.")

    format_char, byte_size = type_formats[data_type]

    with open(input_file, 'rb') as infile:
        if output_file:
            with open(output_file, 'w') as outfile:
                while byte := infile.read(byte_size):
                    value = struct.unpack(format_char, byte)[0]
                    outfile.write(f"{value}\n")
        else:
            while byte := infile.read(byte_size):
                value = struct.unpack(format_char, byte)[0]
                print(value, end='\n')

if __name__ == "__main__":
    print("Arguments received:", sys.argv)
    if len(sys.argv) not in (4, 5):
        print("Usage: binary.py <en|de> <data_type> <input_file> [output_file]")
        sys.exit(1)

    mode = sys.argv[1]
    data_type = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) == 5 else None

    if mode == 'en':
        if not output_file:
            print("Encoding requires an output file.")
            sys.exit(1)
        encode_binary(input_file, output_file, data_type)
    elif mode == 'de':
        decode_binary(input_file, data_type, output_file)
    else:
        print("Invalid mode.")
        sys.exit(1)
