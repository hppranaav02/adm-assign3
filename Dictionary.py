class DictionaryCompressor:
    def compress(self, data):
        """
        Compresses the data using dictionary encoding.
        
        Parameters:
        - data: List of values to compress.
        
        Returns:
        - Tuple of (dictionary, encoded_data), where:
            - dictionary: A mapping of unique values to indices.
            - encoded_data: List of indices representing the data.
        """
        # Create a dictionary of unique values with indices
        unique_values = {value: idx for idx, value in enumerate(set(data))}
        encoded_data = [unique_values[value] for value in data]

        return unique_values, encoded_data

    def decompress(self, dictionary, encoded_data):
        """
        Decompresses the data using dictionary decoding.
        
        Parameters:
        - dictionary: A mapping of indices to unique values.
        - encoded_data: List of indices representing the data.
        
        Returns:
        - List of original values reconstructed from the encoded data.
        """
        # Reverse the dictionary to map indices back to values
        reverse_dict = {idx: value for value, idx in dictionary.items()}
        decompressed_data = [reverse_dict[idx] for idx in encoded_data]

        return decompressed_data
