import os
import time
import subprocess
import pandas as pd

# Define the directories
data_dir = "D:\CSE\GitHub\ADM-A3-Data-Folder\Data"
encoded_dir = "D:\CSE\GitHub\ADM-A3-Data-Folder\Encoded Data"
decoded_dir = "D:\CSE\GitHub\ADM-A3-Data-Folder\Decoded Data"
metrics_file = os.path.join(decoded_dir, "Metrics.xlsx")

# Ensure output directories exist
os.makedirs(encoded_dir, exist_ok=True)
os.makedirs(decoded_dir, exist_ok=True)

# Define algorithms, data types, and supported combinations
algorithms = ["bin", "rle", "dic", "for", "dif"]
data_types = ["int8", "int16", "int32", "int64", "string"]
supported_combinations = {
    "bin": ["int8", "int16", "int32", "int64"],
    "rle": ["int8", "int16", "int32", "int64", "string"],
    "dic": ["int8", "int16", "int32", "int64", "string"],
    "for": ["int8", "int16", "int32", "int64"],
    "dif": ["int8", "int16", "int32", "int64"]
}

# Collect metrics
metrics = []

def run_experiment(mode, algorithm, data_type, input_file, output_file):
    """Runs an encoding or decoding operation and returns the time taken."""
    command = ["python3", "main.py", mode, algorithm, data_type, input_file, output_file]
    start_time = time.time()
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        return None  # Indicates failure
    end_time = time.time()
    return end_time - start_time

# Run all experiments
for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        input_path = os.path.join(data_dir, filename)

        for algorithm in algorithms:
            for data_type in supported_combinations[algorithm]:
                # Set encoded and decoded file paths
                encoded_file = os.path.join(encoded_dir, f"{filename}.{algorithm}")
                decoded_file = os.path.join(decoded_dir, f"{filename}.{algorithm}.csv")

                # Encode
                encode_time = run_experiment("en", algorithm, data_type, input_path, encoded_file)
                if encode_time is not None:
                    # Decode
                    decode_time = run_experiment("de", algorithm, data_type, encoded_file, decoded_file)
                    if decode_time is not None:
                        # Store metrics
                        metrics.append({
                            "CSV Filename": filename,
                            "Algorithm": algorithm,
                            "Data Type": data_type,
                            "Encoded File": encoded_file,
                            "Decoded File": decoded_file,
                            "Encoding Time (s)": encode_time,
                            "Decoding Time (s)": decode_time
                        })
                    else:
                        print(f"Decoding failed for {filename} with {algorithm}-{data_type}")
                else:
                    print(f"Encoding failed for {filename} with {algorithm}-{data_type}")

# Save metrics to an Excel file
metrics_df = pd.DataFrame(metrics)
metrics_df.to_excel(metrics_file, index=False)
print(f"Metrics saved to {metrics_file}")