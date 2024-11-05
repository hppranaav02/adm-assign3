from utils import is_integer_dtype, is_string_dtype, validate_data_for_encoding, check_value_within_dtype_range
import sys


class DictionaryEncoder:
    def encode(self, data, dtype):
        """Encode data using Dictionary Encoding."""
        if not (is_integer_dtype(dtype) or is_string_dtype(dtype)):
            raise TypeError(
                f"Dictionary encoding supports only integer types and strings. Unsupported dtype '{dtype}'.")

        if not validate_data_for_encoding(data, dtype):
            return bytearray()  # Skip encoding if data is incompatible

        dictionary = {}
        encoded_data = bytearray()
        next_code = 0
        size = int(dtype[3:]) // 8 if is_integer_dtype(dtype) else None

        for item in data:
            if item not in dictionary:
                dictionary[item] = next_code
                next_code += 1

            if is_string_dtype(dtype) and isinstance(item, str):
                encoded_data.extend(dictionary[item].to_bytes(2, byteorder='big'))
            elif is_integer_dtype(dtype) and check_value_within_dtype_range(item, dtype):
                encoded_data.extend(dictionary[item].to_bytes(2, byteorder='big'))

        dictionary_bytes = bytearray()
        for key, value in dictionary.items():
            try:
                if is_string_dtype(dtype) and isinstance(key, str):
                    encoded_key = key.encode() + b'\x00'
                elif is_integer_dtype(dtype):
                    encoded_key = int(key).to_bytes(size, byteorder='big', signed=True)
                dictionary_bytes.extend(encoded_key)
                dictionary_bytes.extend(value.to_bytes(2, byteorder='big'))
            except (OverflowError, ValueError):
                print(f"Warning: Skipping dictionary entry '{key}' for dtype '{dtype}' due to byte limit.",
                      file=sys.stderr)

        final_encoded_data = len(dictionary_bytes).to_bytes(4, byteorder='big') + dictionary_bytes + encoded_data
        return final_encoded_data

    def decode(self, encoded_data, dtype):
        """Decode Dictionary Encoded data."""
        if not (is_integer_dtype(dtype) or is_string_dtype(dtype)):
            raise TypeError(
                f"Dictionary decoding supports only integer types and strings. Unsupported dtype '{dtype}'.")

        dict_size = int.from_bytes(encoded_data[:4], byteorder='big')
        dictionary = {}
        index = 4
        size = int(dtype[3:]) // 8 if is_integer_dtype(dtype) else None

        while index < 4 + dict_size:
            if is_string_dtype(dtype):
                end = encoded_data.index(b'\x00', index)
                key = encoded_data[index:end].decode()
                index = end + 1
            else:
                key = int.from_bytes(encoded_data[index:index + size], byteorder='big', signed=True)
                index += size

            value = int.from_bytes(encoded_data[index:index + 2], byteorder='big')
            dictionary[value] = key
            index += 2

        decoded_data = []
        for i in range(4 + dict_size, len(encoded_data), 2):
            code = int.from_bytes(encoded_data[i:i + 2], byteorder='big')
            decoded_data.append(dictionary.get(code, None))

        return decoded_data
