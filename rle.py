from argparse import ArgumentParser
import re
import time


def config_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("encoding", choices=("en", "de"))
    parser.add_argument("compression", choices=("bin", "rle", "dic", "for", "dif"))
    parser.add_argument("input_type", choices=("int8", "int16", "int32", "int64", "string"))
    parser.add_argument("file_path", type=str)
    return parser.parse_args()


def rle_encode(path: str, args: ArgumentParser) -> None:
    
    start_time = time.time()

    with open(path, 'r') as file_read, open(path + ".rle", 'w', newline='') as file_write:

        prev = None
        count = 0

        # Read a row
        for i, message in enumerate(file_read):

            row = message.rstrip('\n')

            if row == prev:
                count += 1

            elif prev == None:
                pass
                
            else:
                # subtract 1 because 1 ahead, add one because count starts at 1
                to_write = f"{prev},{i-count-1},{count+1}\n"
                
                # Write to the ouput file
                file_write.write(to_write)
                
                count = 0

            # Update prev
            prev = row

        # not 1 ahead anymore, do not need to subtract 1
        file_write.write(f"{prev},{i-count},{count+1}\n")

        end_time = time.time()

        with open('logging time.csv', 'a') as time_file:
            time_file.write(f"{args.encoding} rle {path} {end_time-start_time}\n")


def rle_decode(path: str, args:ArgumentParser) -> None:

    start_time = time.time()

    with open(path, 'r') as file_read, open(path + ".csv", 'w', newline='') as file_write:

        # Read a row
        for i, message in enumerate(file_read):

            # Use a regular expression to split based on the last two commas
            match = re.match(r"^(.*),(.*),(.*)$", message)

            if match:
                part1 = match.group(1)
                part3 = match.group(3)
            else:
                print("The string does not match the expected format.")

            # Write to the output file
            file_write.write(f"{part1}\n" * int(part3))

    end_time = time.time()

    with open('logging time.csv', 'a') as time_file:
            time_file.write(f"{args.encoding} rle {path} {end_time-start_time}\n")

    


def main(args):
    encoding = args.encoding
    compression = args.compression
    input_type = args.input_type
    file_path = args.file_path

    # Determine which method to use
    if encoding == "en" and compression == "rle":
        rle_encode(file_path, args)
    elif encoding == "de" and compression == "rle":
        rle_decode(file_path, args)
    else:
        raise Exception("ERROR: Not yet implemented :p")

if __name__ == "__main__":
    main(config_parser())

