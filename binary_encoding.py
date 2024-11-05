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
        if dtype not in type_size:
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for binary encoding.")

        # Convert data to integers and determine encoding size
        size = type_size[dtype]
        encoded_data = bytearray(size.to_bytes(1, byteorder='big'))  # First byte indicates the size of each integer
        
        # Encode each integer in the specified byte size
        for value in data:
            encoded_data.extend(int(value).to_bytes(size, byteorder='big', signed=True))
        
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
        if dtype not in type_size:
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for binary decoding.")

        # Extract size from the first byte
        size = encoded_data[0]
        if size != type_size[dtype]:
            raise ValueError(f"Data size mismatch. Expected size {type_size[dtype]} but got {size}.")

        # Decode each value
        decoded_data = []
        for i in range(1, len(encoded_data), size):
            decoded_data.append(int.from_bytes(encoded_data[i:i+size], byteorder='big', signed=True))
        
        return decoded_data
