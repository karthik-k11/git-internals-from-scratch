import hashlib
import sys

def hash_object(file_path):
    with open(file_path, "rb") as f:
        content= f.read()

    header= f"blob {len(content)}\0".encode()

    store= header+content

    hash= hashlib.sha1(store).hexdigest()

    return hash

if __name__== "__main__":
    file_path= sys.argv[1]
    print(hash_object(file_path))