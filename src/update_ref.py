import sys
import os


def update_ref(commit_hash):
    with open(".git/HEAD", "r") as f:
        ref_line = f.read().strip()

    if not ref_line.startswith("ref:"):
        raise Exception("Detached HEAD not supported")

    ref_path = ref_line.split(" ")[1]
    full_path = os.path.join(".git", ref_path)

    # Update branch pointer
    with open(full_path, "w") as f:
        f.write(commit_hash + "\n")

    print(f"Branch updated to {commit_hash}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_ref.py <commit_hash>")
        sys.exit(1)

    update_ref(sys.argv[1])