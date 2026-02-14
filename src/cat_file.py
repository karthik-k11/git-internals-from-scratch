import sys
import os
import zlib

def read_object(sha1):
    git_dir = ".git"
    objects_dir = os.path.join(git_dir, "objects")

    dir_name = sha1[:2]
    file_name = sha1[2:]

    object_path = os.path.join(objects_dir, dir_name, file_name)

    if not os.path.exists(object_path):
        raise FileNotFoundError("Object does not exist.")

    with open(object_path, "rb") as f:
        compressed_data = f.read()

    decompressed = zlib.decompress(compressed_data)

    return decompressed


def pretty_print_blob(data):
    header, content = data.split(b"\0", 1)

    object_type, size = header.split(b" ")

    if object_type != b"blob":
        raise ValueError("Not a blob object.")

    print(content.decode())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cat_file.py <sha1>")
        sys.exit(1)

    sha1 = sys.argv[1]

    data = read_object(sha1)
    pretty_print_blob(data)