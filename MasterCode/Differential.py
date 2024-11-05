class DifferentialEncoder:
    def encode(self, data, dtype):
        data = [int(d) for d in data]
        reference = data[0]
        adjusted_values = [d - reference for d in data]
        
        encoded_data = bytearray()
        encoded_data.extend(reference.to_bytes(4, byteorder='big', signed=True))
        for val in adjusted_values:
            encoded_data.extend(val.to_bytes(4, byteorder='big', signed=True))
        
        return encoded_data

    def decode(self, data, dtype):
        reference = int.from_bytes(data[0:4], byteorder='big', signed=True)
        decoded_data = [reference]
        
        for i in range(4, len(data), 4):
            delta = int.from_bytes(data[i:i+4], byteorder='big', signed=True)
            decoded_data.append(reference + delta)
        
        return decoded_data
