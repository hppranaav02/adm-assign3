class BinaryDataCompressor:
    def compress(self, data, data_type):
        """
        Compresses the input integer data into binary format.
        
        Parameters:
        - data: List of integer values to compress.
        - data_type: String representing the integer data type ('int8', 'int16', 'int32', 'int64').
        
        Returns:
        - bytearray containing the compressed binary data.
        """
        if not data_type.startswith("int"):
            raise ValueError("Binary compression is only valid for integer types")

        # Calculate the byte size based on the data type (e.g., int8 -> 1 byte, int16 -> 2 bytes)
        byte_size = int(data_type[3:]) // 8
        compressed_data = bytearray()

        # Add the byte size as the first byte for decoding reference
        compressed_data.append(byte_size)

        # Convert each integer to binary format and add to the compressed data
        for number in data:
            compressed_data.extend(number.to_bytes(byte_size, byteorder='big', signed=True))

        return compressed_data

    def decompress(self, binary_data, data_type):
        """
        Decompresses binary data back to a list of integers based on the specified data type.
        
        Parameters:
        - binary_data: bytearray containing the compressed binary data.
        - data_type: String representing the integer data type ('int8', 'int16', 'int32', 'int64').
        
        Returns:
        - List of decompressed integers.
        """
        if not data_type.startswith("int"):
            raise ValueError("Binary decompression is only valid for integer types")

        # Extract byte size from the first byte for reference
        byte_size = binary_data[0]
        decompressed_data = []

        # Read each segment of binary data and convert back to integers
        for i in range(1, len(binary_data), byte_size):
            value = int.from_bytes(binary_data[i:i + byte_size], byteorder='big', signed=True)
            decompressed_data.append(value)

        return decompressed_data
