import sys
import struct

def decode_for_int16(input_file):
    with open(input_file, 'rb') as infile:
        # Read reference value
        reference_value = struct.unpack('<h', infile.read(2))[0]
        
        while bytes_ := infile.read(2):  # Read each delta as int16
            delta = struct.unpack('<h', bytes_)[0]
            original_value = reference_value + delta
            print(original_value, end='\n')  # Output original values

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-for-int16.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_for_int16(input_file)
