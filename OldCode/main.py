import sys
import os
import subprocess

def main():
    if len(sys.argv) != 6:
        print("Usage: main.py <en|de> <bin|rle|dic|for|dif> <data_type> <input_file> <print|file>")
        sys.exit(1)

    mode = sys.argv[1]
    algorithm = sys.argv[2]
    data_type = sys.argv[3]
    input_file = sys.argv[4]
    output_mode = sys.argv[5]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    algorithm_scripts = {
        "bin": os.path.join(script_dir, "binary.py"),
        "rle": os.path.join(script_dir, "rle.py"),
        "dic": os.path.join(script_dir, "dictionary.py"),
        "for": os.path.join(script_dir, "forf.py"),
        "dif": os.path.join(script_dir, "differential.py")
    }

    encoded_file = f"{input_file}.{algorithm}"
    decoded_file = f"{encoded_file}.csv"

    if mode == "en":
        command = ["python", algorithm_scripts[algorithm], mode, data_type, input_file, encoded_file]
    elif mode == "de":
        if output_mode == "print":
            command = ["python", algorithm_scripts[algorithm], mode, data_type, input_file]
        elif output_mode == "file":
            command = ["python", algorithm_scripts[algorithm], mode, data_type, input_file, decoded_file]
        else:
            print("Invalid output mode.")
            sys.exit(1)
    else:
        print("Invalid mode.")
        sys.exit(1)

    print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
