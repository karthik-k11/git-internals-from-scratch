import os
import hashlib
import zlib


def write_tree():
    entries = []

    for file_name in os.listdir():
        if file_name == ".git":
            continue

        if os.path.isfile(file_name):
            with open(file_name, "rb") as f:
                content = f.read()

            header = f"blob {len(content)}\0".encode()
            store = header + content
            sha1 = hashlib.sha1(store).hexdigest()

            mode = "100644"
            entry = f"{mode} {file_name}\0".encode() + bytes.fromhex(sha1)
            entries.append(entry)

    tree_data = b"".join(entries)

    tree_header = f"tree {len(tree_data)}\0".encode()
    full_tree = tree_header + tree_data

    tree_hash = hashlib.sha1(full_tree).hexdigest()

    dir_name = tree_hash[:2]
    file_name = tree_hash[2:]

    object_dir = os.path.join(".git", "objects", dir_name)
    os.makedirs(object_dir, exist_ok=True)

    with open(os.path.join(object_dir, file_name), "wb") as f:
        f.write(zlib.compress(full_tree))

    print(tree_hash)


if __name__ == "__main__":
    write_tree()