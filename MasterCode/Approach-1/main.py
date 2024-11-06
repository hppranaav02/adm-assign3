import sys
import os
import subprocess

def main():
    if len(sys.argv) != 5:
        print("Usage: main.py <en|de> <bin|rle|dic|for|dif> <data_type> <input_file>")
        sys.exit(1)

    # Parse command-line arguments
    mode = sys.argv[1]  # 'en' for encode, 'de' for decode
    algorithm = sys.argv[2]  # Compression technique
    data_type = sys.argv[3]  # Data type
    input_file = sys.argv[4]  # Input file path

    # Ensure the output file is named correctly
    if mode == "en":
        output_file = f"{input_file}.{algorithm}"
    elif mode == "de":
        output_file = f"{input_file}.csv"
    else:
        print("Invalid mode. Use 'en' for encoding or 'de' for decoding.")
        sys.exit(1)
        
    # Define the path to each script relative to the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    algorithm_scripts = {
        "bin": os.path.join("D:\CSE\GitHub\ADM-A3\MasterCode", "binary.py"),
        "rle": os.path.join("D:\CSE\GitHub\ADM-A3\MasterCode", "rle.py"),
        "dic": os.path.join("D:\CSE\GitHub\ADM-A3\MasterCode", "dictionary.py"),
        "for": os.path.join("D:\CSE\GitHub\ADM-A3\MasterCode", "forf.py"),
        "dif": os.path.join("D:\CSE\GitHub\ADM-A3\MasterCode", "differential.py")
    }

    # Check if the algorithm is supported
    if algorithm not in algorithm_scripts:
        print(f"Invalid algorithm: {algorithm}. Supported algorithms are: bin, rle, dic, for, dif.")
        sys.exit(1)

    # Check compatibility of data types with algorithms
    if algorithm in {"bin", "for", "dif"} and data_type == "string":
        print(f"The algorithm '{algorithm}' does not support the data type 'string'.")
        sys.exit(1)

    # Build command based on the specific algorithm
    script = algorithm_scripts[algorithm]
    python_cmd = "python3" if os.name != "nt" else "python"

    # For algorithms that don’t use data_type, omit it from the command
    if algorithm in {"rle", "dic"}:
        command = [python_cmd, script, mode, input_file, output_file]
    else:
        command = [python_cmd, script, mode, data_type, input_file, output_file]

    # Execute the command and capture any output or errors
    try:
        subprocess.run(command, check=True)
        print(f"Operation {mode} on {algorithm} with data type {data_type} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script}: {e}")

if __name__ == "__main__":
    main()
