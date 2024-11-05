class FrameOfReferenceCompressor:
    def compress(self, data):
        """
        Compresses the data using frame of reference encoding.
        
        Parameters:
        - data: List of integer values to compress.
        
        Returns:
        - Tuple of (reference_value, adjusted_values), where:
            - reference_value: The minimum value in the data.
            - adjusted_values: List of differences between each data point and the reference value.
        """
        if not data:
            return None, []

        # Use the minimum value as the reference (frame of reference)
        reference_value = min(data)
        adjusted_values = [value - reference_value for value in data]

        return reference_value, adjusted_values

    def decompress(self, reference_value, adjusted_values):
        """
        Decompresses the data using frame of reference decoding.
        
        Parameters:
        - reference_value: The reference value (minimum value used during compression).
        - adjusted_values: List of differences between each data point and the reference value.
        
        Returns:
        - List of original integer values reconstructed from the frame of reference encoded data.
        """
        # Reconstruct original values by adding the reference value to each adjusted value
        decompressed_data = [reference_value + value for value in adjusted_values]

        return decompressed_data
