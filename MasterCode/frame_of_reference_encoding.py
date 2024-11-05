class FrameOfReferenceEncoder:
    def encode(self, data, dtype):
        """Encode data using Frame of Reference Encoding.
        
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
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for frame of reference encoding.")
        
        size = type_size[dtype]
        reference_value = min(data)  # Frame of reference
        encoded_data = bytearray()
        encoded_data.extend(reference_value.to_bytes(size, byteorder='big', signed=True))  # Store reference value first
        
        # Store each value as the difference from the reference
        for value in data:
            delta = value - reference_value
            encoded_data.extend(delta.to_bytes(size, byteorder='big', signed=True))
        
        return encoded_data

    def decode(self, encoded_data, dtype):
        """Decode Frame of Reference Encoded data back to a list of original values.
        
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
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for frame of reference decoding.")
        
        size = type_size[dtype]
        
        # Extract the reference value
        reference_value = int.from_bytes(encoded_data[:size], byteorder='big', signed=True)
        decoded_data = []
        
        # Decode each delta value and reconstruct original values
        for i in range(size, len(encoded_data), size):
            delta = int.from_bytes(encoded_data[i:i+size], byteorder='big', signed=True)
            decoded_data.append(reference_value + delta)
        
        return decoded_data
