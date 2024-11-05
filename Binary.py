class BinaryDataCompressor:
    def compress(self, data, data_type):
        """
        Compress the given data into binary format according to the specified integer type.

        Parameters:
        - data: List of integer values to compress.
        - data_type: A string indicating the data type (e.g., 'int8', 'int16', 'int32', 'int64').

        Returns:
        - bytearray of binary compressed data.
        """
        # Ensure we are working with integer types only
        if not data_type.startswith("int"):
            raise ValueError("Binary compression is only valid for integer types")

        # Determine the byte size based on the data type (e.g., 'int8' -> 1 byte)
        byte_size = int(data_type[3:]) // 8
        compressed_data = bytearray()

        # Append byte size as the first byte to indicate the integer size for decompression
        compressed_data.append(byte_size)

        # Convert each integer to binary format and append to the compressed data
        for number in data:
            compressed_data.extend(number.to_bytes(byte_size, byteorder='big', signed=True))

        return compressed_data

    def decompress(self, binary_data, data_type):
        """
        Decompress binary data back to a list of integers based on the specified integer type.

        Parameters:
        - binary_data: Bytearray of compressed binary data.
        - data_type: A string indicating the data type (e.g., 'int8', 'int16', 'int32', 'int64').

        Returns:
        - List of integers decompressed from the binary data.
        """
        if not data_type.startswith("int"):
            raise ValueError("Binary decompression is only valid for integer types")

        # Extract byte size from the first byte
        byte_size = binary_data[0]
        decompressed_data = []

        # Read each segment of binary data, converting it back to integers
        for i in range(1, len(binary_data), byte_size):
            value = int.from_bytes(binary_data[i:i + byte_size], byteorder='big', signed=True)
            decompressed_data.append(value)

        return decompressed_data
