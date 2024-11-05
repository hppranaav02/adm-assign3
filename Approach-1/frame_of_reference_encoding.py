from utils import is_integer_dtype, validate_data_for_encoding, check_value_within_dtype_range
import sys

class FrameOfReferenceEncoder:
    def encode(self, data, dtype):
        """Encodes data using Frame of Reference Encoding."""
        if not is_integer_dtype(dtype):
            raise TypeError(f"Frame of Reference Encoding supports only integer types. Unsupported dtype '{dtype}'.")

        if not validate_data_for_encoding(data, dtype):
            return bytearray()

        size = int(dtype[3:]) // 8
        reference_value = min(data)
        encoded_data = bytearray(reference_value.to_bytes(size, byteorder='big', signed=True))

        for value in data:
            delta = value - reference_value
            if check_value_within_dtype_range(delta, dtype):
                encoded_data.extend(delta.to_bytes(size, byteorder='big', signed=True))
            else:
                print(f"Warning: Delta '{delta}' exceeds byte limit for dtype '{dtype}'. Skipping.", file=sys.stderr)

        return encoded_data

    def decode(self, encoded_data, dtype):
        """Decodes Frame of Reference Encoded data."""
        size = int(dtype[3:]) // 8
        reference_value = int.from_bytes(encoded_data[:size], byteorder='big', signed=True)
        decoded_data = []

        for i in range(size, len(encoded_data), size):
            delta = int.from_bytes(encoded_data[i:i+size], byteorder='big', signed=True)
            decoded_data.append(reference_value + delta)

        return decoded_data
