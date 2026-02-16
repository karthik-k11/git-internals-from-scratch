import hashlib
import os
import sys
import zlib
import time
import subprocess

def get_git_user():
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True
        ).strip()

        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()

        return f"{name} <{email}>"

    except:
        return "Unknown <unknown@example.com>"

def create_commit(tree_hash, message):
    timestamp = int(time.time())
    timezone = "+0530"

    author = get_git_user()

    commit_content = f"""tree {tree_hash}
author {author} {timestamp} {timezone}
committer {author} {timestamp} {timezone}

{message}
""".encode()

    header = f"commit {len(commit_content)}\0".encode()
    store = header + commit_content

    sha1 = hashlib.sha1(store).hexdigest()

    dir_name = sha1[:2]
    file_name = sha1[2:]
    object_dir = os.path.join(".git", "objects", dir_name)
    os.makedirs(object_dir, exist_ok=True)

    with open(os.path.join(object_dir, file_name), "wb") as f:
        f.write(zlib.compress(store))

    return sha1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python commit_tree.py <tree_hash> <message>")
        sys.exit(1)

    tree_hash = sys.argv[1]
    message = sys.argv[2]

    commit_hash = create_commit(tree_hash, message)
    print(commit_hash)