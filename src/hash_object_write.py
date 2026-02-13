import hashlib
import sys
import os
import zlib


def hash_object(file_path):
    with open(file_path, "rb") as f:
        content = f.read()

    header = f"blob {len(content)}\0".encode()
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()
    return sha1, store


def write_object(sha1, store):
    git_dir = ".git"
    objects_dir = os.path.join(git_dir, "objects")

    dir_name = sha1[:2]
    file_name = sha1[2:]

    object_dir = os.path.join(objects_dir, dir_name)
    object_path = os.path.join(object_dir, file_name)

    if os.path.exists(object_path):
        return

    os.makedirs(object_dir, exist_ok=True)

    compressed_data = zlib.compress(store)

    with open(object_path, "wb") as f:
        f.write(compressed_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hash_object_write.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    sha1, store = hash_object(file_path)
    write_object(sha1, store)

    print(sha1)