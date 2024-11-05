from utils import is_integer_dtype, is_string_dtype, validate_data_for_encoding, check_value_within_dtype_range
import sys

class BinaryEncoder:
    def encode(self, data, dtype):
        """Encode data as a bytearray in uncompressed binary format.
        
        Parameters:
            data (list): List of integer values to encode.
            dtype (str): Data type ('int8', 'int16', 'int32', or 'int64').

        Returns:
            bytearray: Encoded binary data.
        """
        # Define byte size for each integer type
        type_size = {
            'int8': 1,
            'int16': 2,
            'int32': 4,
            'int64': 8
        }
        
        # Ensure dtype is an integer type
        if not is_integer_dtype(dtype):
            raise TypeError(f"Binary encoding supports only integer types. Unsupported dtype '{dtype}'.")

        if not validate_data_for_encoding(data, dtype):
            return bytearray()  # Skip encoding if data is incompatible

        size = int(int(dtype[3:]) / 8)
        encoded_data = bytearray(size.to_bytes(1, byteorder='big'))  # First byte: size of each integer

        for value in data:
            value = int(value)
            if check_value_within_dtype_range(value, dtype):
                encoded_data.extend(value.to_bytes(size, byteorder='big', signed=True))
            else:
                print(f"Warning: Value '{value}' exceeds byte limit for dtype '{dtype}'. Skipping.", file=sys.stderr)

        return encoded_data

    def decode(self, encoded_data, dtype):
        """Decode bytearray data back to a list of integers.
        
        Parameters:
            encoded_data (bytearray): Binary data to decode.
            dtype (str): Data type used in encoding ('int8', 'int16', 'int32', or 'int64').

        Returns:
            list: Decoded list of integers.
        """
        # Define byte size for each integer type
        type_size = {
            'int8': 1,
            'int16': 2,
            'int32': 4,
            'int64': 8
        }
        
        # Ensure dtype is an integer type
        if not is_integer_dtype(dtype):
            raise TypeError(f"Binary decoding supports only integer types. Unsupported dtype '{dtype}'.")

        size = int.from_bytes(data[0:1], byteorder='big')
        decoded_data = []

        for i in range(1, len(data), size):
            decoded_data.append(int.from_bytes(data[i:i + size], byteorder='big', signed=True))

        return decoded_data
