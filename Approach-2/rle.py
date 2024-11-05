class RunLengthCompressor:
    def compress(self, data, data_type):
        """
        Compresses the data using run-length encoding (RLE).
        
        Parameters:
        - data: List of values to compress.
        - data_type: String indicating the type of data ('int' or 'str').
        
        Returns:
        - Byte-like object containing the run-length encoded data.
        """
        encoded_data = bytearray()
        if data_type.startswith("int"):
            # Process integers with RLE
            i = 0
            while i < len(data):
                count = 1
                while i + count < len(data) and data[i] == data[i + count]:
                    count += 1
                # Store the value and its count in binary format
                encoded_data.extend(data[i].to_bytes(4, byteorder='big', signed=True))
                encoded_data.extend(count.to_bytes(2, byteorder='big'))
                i += count
        else:
            # Process strings with RLE
            i = 0
            while i < len(data):
                count = 1
                while i + count < len(data) and data[i] == data[i + count]:
                    count += 1
                # Store the character as bytes and its count
                encoded_data.extend(data[i].encode('utf-8'))
                encoded_data.extend(count.to_bytes(2, byteorder='big'))
                i += count

        return encoded_data

    def decompress(self, encoded_data, data_type):
        """
        Decompresses the data using run-length decoding (RLE).
        
        Parameters:
        - encoded_data: Byte-like object containing the run-length encoded data.
        - data_type: String indicating the type of data ('int' or 'str').
        
        Returns:
        - List of original values reconstructed from the run-length encoded data.
        """
        decoded_data = []
        i = 0
        if data_type.startswith("int"):
            # Decode integer data
            while i < len(encoded_data):
                # Read the value (4 bytes for integer) and the count (2 bytes)
                value = int.from_bytes(encoded_data[i:i+4], byteorder='big', signed=True)
                count = int.from_bytes(encoded_data[i+4:i+6], byteorder='big')
                decoded_data.extend([value] * count)
                i += 6
        else:
            # Decode string data
            while i < len(encoded_data):
                # Read the character (1 byte for a single UTF-8 character) and the count (2 bytes)
                value = encoded_data[i:i+1].decode('utf-8')
                count = int.from_bytes(encoded_data[i+1:i+3], byteorder='big')
                decoded_data.extend([value] * count)
                i += 3

        return decoded_data
