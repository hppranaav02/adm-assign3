import sys
import struct

def decode_for_int32(input_file):
    with open(input_file, 'rb') as infile:
        # Read reference value
        reference_value = struct.unpack('<i', infile.read(4))[0]
        
        while bytes_ := infile.read(4):  # Read each delta as int32
            delta = struct.unpack('<i', bytes_)[0]
            original_value = reference_value + delta
            print(original_value, end='\n')  # Output original values

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-for-int32.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_for_int32(input_file)
