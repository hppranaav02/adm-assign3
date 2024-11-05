class DifferentialCompressor:
    def compress(self, data):
        """
        Compresses the data using differential encoding.
        
        Parameters:
        - data: List of integer values to compress.
        
        Returns:
        - List of integers where each element is the difference from the previous element.
        """
        if not data:
            return []

        # The first value remains as is, subsequent values are stored as differences
        compressed_data = [data[0]]
        for i in range(1, len(data)):
            compressed_data.append(data[i] - data[i - 1])

        return compressed_data

    def decompress(self, compressed_data):
        """
        Decompresses the data using differential decoding.
        
        Parameters:
        - compressed_data: List of integers where each element is the difference from the previous element.
        
        Returns:
        - List of original integer values reconstructed from the differential data.
        """
        if not compressed_data:
            return []

        # The first value remains as is, subsequent values are added to reconstruct the data
        decompressed_data = [compressed_data[0]]
        for i in range(1, len(compressed_data)):
            decompressed_data.append(decompressed_data[-1] + compressed_data[i])

        return decompressed_data
