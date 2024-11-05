from utils import is_integer_dtype, validate_data_for_encoding, check_value_within_dtype_range
import sys

class DifferentialEncoder:
    def encode(self, data, dtype):
        """Encodes data using Differential Encoding."""
        if not is_integer_dtype(dtype):
            raise TypeError(f"Differential Encoding supports only integer types. Unsupported dtype '{dtype}'.")

        if not validate_data_for_encoding(data, dtype):
            return bytearray()

        size = int(dtype[3:]) // 8
        encoded_data = bytearray()
        prev_value = int(data[0])
        encoded_data.extend(prev_value.to_bytes(size, byteorder='big', signed=True))

        for value in data[1:]:
            delta = value - prev_value
            if check_value_within_dtype_range(delta, dtype):
                encoded_data.extend(delta.to_bytes(size, byteorder='big', signed=True))
                prev_value = value
            else:
                print(f"Warning: Delta '{delta}' exceeds byte limit for dtype '{dtype}'. Skipping.", file=sys.stderr)

        return encoded_data

    def decode(self, encoded_data, dtype):
        """Decodes Differential Encoded data."""
        size = int(dtype[3:]) // 8
        first_value = int.from_bytes(encoded_data[:size], byteorder='big', signed=True)
        decoded_data = [first_value]

        for i in range(size, len(encoded_data), size):
            delta = int.from_bytes(encoded_data[i:i+size], byteorder='big', signed=True)
            decoded_data.append(decoded_data[-1] + delta)

        return decoded_data
