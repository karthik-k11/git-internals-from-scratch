# Git Object Storage (Writing Blob Objects)

In this step, I extended the hashing logic from Day 2 to fully replicate
how Git stores blob objects inside the `.git/objects/` directory.

The goal was not just to compute the correct SHA-1 hash, but to
write a valid Git object that can be read by native Git commands.

---

## 1. From Hashing to Storage

On Day 2, I implemented the exact logic behind:
git hash-object <file>


Git internally builds a structured byte sequence:
blob <size>\0<content>


It then computes the SHA-1 hash of that structure.

In this step, I extended the process to match:
git hash-object -w <file>


The `-w` flag tells Git to write the object into its object database.

---

## 2. Git’s Object Directory Structure

Git stores all objects inside:
.git/objects/


Each object is stored using its SHA-1 hash.

The structure follows this pattern:
.git/objects/aa/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb


Where:

- `aa` → first 2 characters of the hash (directory name)
- remaining characters → file name

For example:

b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0


is stored as:

.git/objects/b6/fc4c620b67d95f953a5c1c1230aaab5db5a1b0


This design prevents too many files from being stored in a single directory,
which improves filesystem performance.

---

## 3. Compression with zlib

Before writing the object to disk, Git compresses the data using zlib.

The process is:

1. Construct the Git object format:
blob <size>\0<content>


2. Compress the entire byte sequence.
3. Write the compressed bytes into the object file.

Compression reduces disk usage and improves efficiency.

---

## 4. Immutable, Content-Addressable Storage

Git objects are immutable.

If the same content is written multiple times:

- The SHA-1 hash remains the same.
- The object path remains the same.
- The existing object is reused.

This makes Git a content-addressable storage system:
- The content determines the hash.
- The hash determines the storage location.

No object is ever modified once written.

---

## 5. Implementation

The implementation for writing blob objects is available here:

[`src/hash_object_write.py`](../src/hash_object_write.py)

This implementation:

- Reads file content as raw bytes
- Constructs the Git blob header
- Computes SHA-1
- Compresses the object using zlib
- Writes it into `.git/objects/` using the correct directory structure

---

## 6. Verifying Object Validity

After writing the object using the custom implementation,
I verified correctness using native Git:
git cat-file -p <hash>


If Git can read and print the content, the object is valid.

This confirms interoperability between the custom implementation
and Git’s internal object database.

---

## 7. Key Takeaway

At this stage, I have implemented:

- Byte-accurate blob hashing
- Git-style header formatting
- SHA-based object addressing
- zlib compression
- Proper object directory layout

This completes the full lifecycle of a Git blob:
from file → structured object → compressed storage → readable by Git.
