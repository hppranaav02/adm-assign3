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

    # Determine base filename (without extension) for output files
    base_filename = os.path.splitext(input_file)[0]

    # Set output file based on mode and desired file format
    if mode == "en":
        output_file = f"{base_filename}.{algorithm}"
    elif mode == "de":
        output_file = f"{base_filename}.{algorithm}.csv"
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

    # Build command to call the respective script
    script = algorithm_scripts[algorithm]
    python_cmd = "python3" if os.name != "nt" else "python"
    command = [python_cmd, script, mode, data_type, input_file, output_file]

    # Print the command being executed
    print(f"Executing command: {' '.join(command)}")

    # Execute the command and capture any output or errors
    try:
        subprocess.run(command, check=True)
        print(f"Operation {mode} on {algorithm} with data type {data_type} completed successfully.")
        print(f"Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script}: {e}")

if __name__ == "__main__":
    main()
