import sys
import struct

def decode_for_int64(input_file):
    with open(input_file, 'rb') as infile:
        # Read reference value
        reference_value = struct.unpack('<q', infile.read(8))[0]
        
        while bytes_ := infile.read(8):  # Read each delta as int64
            delta = struct.unpack('<q', bytes_)[0]
            original_value = reference_value + delta
            print(original_value, end='\n')  # Output original values

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program-de-for-int64.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    decode_for_int64(input_file)
