import sys

class DictionaryEncoder:
    def encode(self, data, dtype):
        """Encode data using Dictionary Encoding.
        
        Parameters:
            data (list): List of values to encode (integers or strings).
            dtype (str): Data type ('int8', 'int16', 'int32', 'int64', or 'string').

        Returns:
            bytearray: Encoded binary data.
        """
        if dtype not in ["int8", "int16", "int32", "int64", "string"]:
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types and strings are supported for dictionary encoding.")

        dictionary = {}
        encoded_data = bytearray()
        next_code = 0

        # Build dictionary and encode data
        for item in data:
            if item not in dictionary:
                dictionary[item] = next_code
                next_code += 1
            try:
                # Ensure we only encode strings
                if isinstance(item, str):
                    encoded_data.extend(dictionary[item].to_bytes(2, byteorder='big'))
                else:
                    # Convert integers to byte representation based on dtype size
                    size = int(dtype[3:]) // 8  # Calculate byte size from dtype (e.g., 8, 16, 32, 64)
                    encoded_data.extend(int(item).to_bytes(size, byteorder='big', signed=True))
            except (OverflowError, ValueError) as e:
                print(f"Warning: Item '{item}' exceeds byte limit or cannot be encoded as '{dtype}'. Error: {e}", file=sys.stderr)
                continue

        # Serialize the dictionary at the beginning of the encoded data
        dictionary_bytes = bytearray()
        for key, value in dictionary.items():
            try:
                if dtype == "string" and isinstance(key, str):
                    encoded_key = key.encode() + b'\x00'  # Null-terminated strings
                else:
                    # Handle large integer keys properly
                    encoded_key = int(key).to_bytes(int(dtype[3:]) // 8, byteorder='big', signed=True)
                dictionary_bytes.extend(encoded_key)
                dictionary_bytes.extend(value.to_bytes(2, byteorder='big'))
            except (OverflowError, ValueError) as e:
                print(f"Warning: Key '{key}' exceeds byte limit or cannot be represented as '{dtype}'. Error: {e}", file=sys.stderr)
                continue

        # Combine dictionary and encoded data
        final_encoded_data = len(dictionary_bytes).to_bytes(4, byteorder='big') + dictionary_bytes + encoded_data
        return final_encoded_data

    def decode(self, encoded_data, dtype):
        """Decode Dictionary Encoded data back to a list of original values.
        
        Parameters:
            encoded_data (bytearray): Encoded binary data.
            dtype (str): Data type used in encoding ('int8', 'int16', 'int32', or 'int64', or 'string').

        Returns:
            list: Decoded list of original values.
        """
        if dtype not in ["int8", "int16", "int32", "int64", "string"]:
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types and strings are supported for dictionary decoding.")

        # Read dictionary size
        dict_size = int.from_bytes(encoded_data[:4], byteorder='big')
        dictionary = {}
        index = 4

        # Deserialize dictionary
        while index < 4 + dict_size:
            if dtype == "string":
                end = encoded_data.index(b'\x00', index)
                key = encoded_data[index:end].decode()
                index = end + 1
            else:
                size = int(dtype[3:]) // 8
                key = int.from_bytes(encoded_data[index:index+size], byteorder='big', signed=True)
                index += size

            value = int.from_bytes(encoded_data[index:index+2], byteorder='big')
            dictionary[value] = key
            index += 2

        # Decode data using dictionary
        decoded_data = []
        for i in range(4 + dict_size, len(encoded_data), 2):
            code = int.from_bytes(encoded_data[i:i+2], byteorder='big')
            decoded_data.append(dictionary.get(code, None))  # Use `get` to avoid key errors in case of issues

        return decoded_data
