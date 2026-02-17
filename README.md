# Git Internals From Scratch

A step-by-step reimplementation of Git’s core object model using Python.

This project reconstructs how Git stores data and tracks history by manually
creating and linking Git objects inside the `.git` directory — without using
Git’s high-level commands.

The goal is to understand Git as a content-addressable database rather than a
version control tool.

---

## What This Project Demonstrates

Git internally operates on four fundamental concepts:

blob → file content  
tree → directory snapshot  
commit → history node  
ref → pointer to history

This repository rebuilds that workflow manually.

By the end of the project, commits created by the custom scripts are readable
by native Git commands such as:

git cat-file
git log
---

## Implemented Components

### 1. Blob Objects — Content Storage
- Constructed Git blob format: `blob <size>\0<content>`
- Generated SHA-1 hash identical to `git hash-object`
- Stored compressed objects inside `.git/objects/`

Scripts:
src/hash_object.py
src/hash_object_write.py

---

### 2. Reading Objects — Object Parsing
- Located object using SHA-1
- Decompressed using zlib
- Parsed header and printed content

Script:
src/cat_file.py


---

### 3. Tree Objects — Directory Snapshots
- Built binary tree entries (`mode filename\0<raw_sha>`)
- Linked filenames to blob hashes
- Created valid tree objects readable by Git

Script:
src/write_tree.py

---

### 4. Commit Objects — History Nodes
- Constructed commit structure with metadata and message
- Linked commits to trees
- Produced valid commit objects

Script:
src/commit_tree.py

---

### 5. References — History Linking
- Updated branch references manually
- Connected commit to HEAD
- Made custom commits appear in `git log`

Script:
src/update_ref.py

---

## Result

This project reproduces the internal workflow of:
git add
git commit
git log


without invoking Git’s implementation — only interacting with its storage
format.
---

## Repository Structure

src/ → implementation scripts
docs/ → explanations of each internal component


Documentation is written alongside each step to explain the underlying Git
mechanism rather than only the code.

---

## Key Takeaway

Git is not primarily a version control system.

It is a content-addressable object database with a reference graph layered on
top.

Understanding this model clarifies how branching, merging, and history
rewriting actually work.

---

## Future Improvements

- Implement commit parent traversal (`git log` from scratch)
- Support nested directories in tree objects
- Implement index (staging area)
- Implement branching