import sys
import struct

def encode_for(input_file, output_file, data_type):
    
    type_formats = {
        "int8": ('b', 1),     
        "int16": ('<h', 2),   
        "int32": ('<i', 4),    
        "int64": ('<q', 8)    
    }

    if data_type not in type_formats:
        raise ValueError("Unsupported data type for frame of reference encoding.")

    format_char, byte_size = type_formats[data_type]

    with open(input_file, 'r') as infile:
        data = [int(line.strip()) for line in infile]
    reference_value = min(data)

    with open(output_file, 'wb') as outfile:

        outfile.write(struct.pack(format_char, reference_value))
        
        for value in data:
            delta = value - reference_value
            outfile.write(struct.pack(format_char, delta))

def decode_for(input_file, data_type):

    type_formats = {
        "int8": ('b', 1),       
        "int16": ('<h', 2),     
        "int32": ('<i', 4),     
        "int64": ('<q', 8)     
    }

    if data_type not in type_formats:
        raise ValueError("Unsupported data type for frame of reference decoding.")

    format_char, byte_size = type_formats[data_type]

    with open(input_file, 'rb') as infile:

        reference_value = struct.unpack(format_char, infile.read(byte_size))[0]
        
        while bytes_ := infile.read(byte_size):
            delta = struct.unpack(format_char, bytes_)[0]
            original_value = reference_value + delta
            print(original_value, end='\n')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: forf.py <en|de> <data_type> <input_file>")
        sys.exit(1)

    mode = sys.argv[1] 
    data_type = sys.argv[2]
    input_file = sys.argv[3]

    if mode == 'en':
        output_file = f"{input_file}.{data_type}.for"
        encode_for(input_file, output_file, data_type)
    elif mode == 'de':
        decode_for(input_file, data_type)
    else:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        sys.exit(1)
