# Tree Objects (Directory Snapshots in Git)

In this step, I implemented the creation of Git tree objects.

While blob objects store file content, tree objects represent
directory structure. A tree acts as a snapshot of a directory
at a specific point in time.

---

## 1. Role of Tree Objects

Git internally organizes data in three layers:

- Blob → stores file content
- Tree → stores directory structure (file names + blob hashes)
- Commit → points to a tree and records metadata

A tree connects file names to their corresponding blob hashes.

---

## 2. Tree Entry Format

Each entry inside a tree follows this binary structure:
<mode> <filename>\0<20-byte binary SHA>

Example (conceptually):
100644 mynotes.txt\0[binary blob SHA]


Important details:

- The SHA is stored as raw 20-byte binary, not hex text.
- Multiple entries are concatenated.
- The entire entry list becomes the tree content.

---

## 3. Tree Object Structure

Like blobs, tree objects follow Git’s standard object format:
tree <size>\0<entries>


Where:

- `<size>` is the byte length of all entries.
- `<entries>` is the concatenated binary tree data.

This entire byte sequence is then:

1. Hashed using SHA-1
2. Compressed using zlib
3. Stored inside `.git/objects/`

---

## 4. Directory Layout

Tree objects are stored using the same content-addressable layout:
.git/objects/aa/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

Where:
- `aa` → first 2 characters of SHA
- remainder → file name

This structure ensures efficient filesystem storage.

---

## 5. Implementation

The implementation is available here:

[`src/write_tree.py`](../src/write_tree.py)

This script:

- Iterates through files in the working directory
- Computes blob hashes
- Constructs tree entries in binary format
- Builds a valid Git tree object
- Compresses and stores it in `.git/objects/`

---

## 6. Verifying Correctness

To verify correctness, I ran:
python src/write_tree.py

Then inspected the tree using native Git:
git cat-file -p <tree_hash>

Git successfully printed the directory structure,
confirming that the tree object was correctly constructed.

---
## 7. Key Takeaway

Tree objects form the bridge between file content and commits.

They allow Git to:

- Represent directory structure
- Track file names and modes
- Create complete project snapshots

At this stage, I have implemented both blob and tree object handling,
which forms the core of Git’s object storage system.