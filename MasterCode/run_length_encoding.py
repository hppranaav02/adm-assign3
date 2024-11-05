from utils import is_integer_dtype, is_string_dtype, validate_data_for_encoding, check_value_within_dtype_range
import sys

class RunLengthEncoder:
    def encode(self, data, dtype):
        """Encodes data using Run-Length Encoding."""
        if not (is_integer_dtype(dtype) or is_string_dtype(dtype)):
            raise TypeError(f"RLE supports only integer types and strings. Unsupported dtype '{dtype}'.")

        if not validate_data_for_encoding(data, dtype):
            return bytearray()

        size = int(dtype[3:]) // 8 if is_integer_dtype(dtype) else None
        encoded_data = bytearray(size.to_bytes(1, byteorder='big') if size else b'\x00')  # First byte for integer size

        count = 1
        prev_value = data[0]

        for value in data[1:]:
            if value == prev_value:
                count += 1
            else:
                if is_string_dtype(dtype):
                    encoded_data.extend(prev_value.encode() + b'\x00')
                elif is_integer_dtype(dtype) and check_value_within_dtype_range(prev_value, dtype):
                    encoded_data.extend(int(prev_value).to_bytes(size, byteorder='big', signed=True))
                encoded_data.extend(count.to_bytes(2, byteorder='big'))
                prev_value = value
                count = 1

        return encoded_data

    def decode(self, encoded_data, dtype):
        """Decodes Run-Length Encoded data."""
        size = int.from_bytes(encoded_data[0:1], byteorder='big') if is_integer_dtype(dtype) else None
        decoded_data = []

        i = 1
        while i < len(encoded_data):
            if is_string_dtype(dtype):
                end = encoded_data.index(b'\x00', i)
                value = encoded_data[i:end].decode()
                i = end + 1
            else:
                value = int.from_bytes(encoded_data[i:i+size], byteorder='big', signed=True)
                i += size
            count = int.from_bytes(encoded_data[i:i+2], byteorder='big')
            decoded_data.extend([value] * count)
            i += 2

        return decoded_data
