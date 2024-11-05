class RunLengthEncoder:
    def encode(self, data, dtype):
        """Encode data using Run-Length Encoding.
        
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
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for RLE encoding.")

        size = type_size[dtype]
        encoded_data = bytearray(size.to_bytes(1, byteorder='big'))  # First byte indicates size of integers
        
        # Run-Length Encoding: Count consecutive values
        count = 1
        prev_value = int(data[0])

        for value in data[1:]:
            value = int(value)
            if value == prev_value:
                count += 1
            else:
                # Append the previous value and its count
                encoded_data.extend(prev_value.to_bytes(size, byteorder='big', signed=True))
                encoded_data.extend(count.to_bytes(2, byteorder='big'))  # Use 2 bytes for count to handle large runs
                # Reset count and update previous value
                prev_value = value
                count = 1
        
        # Append the final value and its count
        encoded_data.extend(prev_value.to_bytes(size, byteorder='big', signed=True))
        encoded_data.extend(count.to_bytes(2, byteorder='big'))
        
        return encoded_data

    def decode(self, encoded_data, dtype):
        """Decode Run-Length Encoded data back to a list of integers.
        
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
            raise TypeError(f"Unsupported dtype {dtype}. Only integer types are supported for RLE decoding.")

        size = encoded_data[0]  # First byte contains the size of each integer
        if size != type_size[dtype]:
            raise ValueError(f"Data size mismatch. Expected size {type_size[dtype]} but got {size}.")

        decoded_data = []
        i = 1  # Start reading after the size byte
        
        # Decode each value and its count
        while i < len(encoded_data):
            value = int.from_bytes(encoded_data[i:i+size], byteorder='big', signed=True)
            count = int.from_bytes(encoded_data[i+size:i+size+2], byteorder='big')  # 2 bytes for count
            decoded_data.extend([value] * count)
            i += size + 2  # Move to the next encoded pair (value + count)
        
        return decoded_data
