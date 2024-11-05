class DifferentialEncoder:
    def encode(self, data, dtype):
        """Encode data using Differential Encoding.
        
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
        if dtype not in type_size:
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for differential encoding.")

        size = type_size[dtype]
        encoded_data = bytearray()

        # Store the first value as is
        previous_value = int(data[0])
        encoded_data.extend(previous_value.to_bytes(size, byteorder='big', signed=True))

        # Encode subsequent values as differences from the previous value
        for value in data[1:]:
            delta = value - previous_value
            encoded_data.extend(delta.to_bytes(size, byteorder='big', signed=True))
            previous_value = value  # Update previous value
        
        return encoded_data

    def decode(self, encoded_data, dtype):
        """Decode Differential Encoded data back to a list of original values.
        
        Parameters:
            encoded_data (bytearray): Encoded binary data.
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
        if dtype not in type_size:
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for differential decoding.")

        size = type_size[dtype]

        # Read the first value as it is
        first_value = int.from_bytes(encoded_data[:size], byteorder='big', signed=True)
        decoded_data = [first_value]

        # Decode each delta and reconstruct the original values
        for i in range(size, len(encoded_data), size):
            delta = int.from_bytes(encoded_data[i:i+size], byteorder='big', signed=True)
            decoded_data.append(decoded_data[-1] + delta)  # Add delta to the last decoded value
        
        return decoded_data
