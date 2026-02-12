# Reimplementing `git hash-object` (Blob Hashing)

In this step, I reimplemented the core logic behind `git hash-object`
to understand how Git generates object hashes.

The goal was to produce the exact same SHA-1 hash as native Git,
using only Python.

---

## 1. What Git Actually Hashes

Initially, I assumed Git hashes only the raw file content.

However, Git does not hash just the file bytes.

Instead, it hashes the following structure:

blob <file_size>\0<file_content>


For example, if the file contains:


which is 5 bytes long, Git internally hashes:
blob 5\0hello


The header (`blob 5\0`) is part of the data being hashed.

---

## 2. Why the Header Is Required

The header serves two purposes:

- It encodes the object type (`blob`, `tree`, `commit`)
- It encodes the size of the content

This ensures that:
- A blob and a commit with the same content produce different hashes
- Object identity is tied to both type and content

Without the header, hashing would not follow Git’s object format.

---

## 3. Python Implementation

The implementation:

[`src/hash_object.py`](../src/hash_object.py)

Steps:

- Read file content as raw bytes.

- Construct the Git-style header.

- Concatenate header + content.

- Compute SHA-1 of the combined bytes.

## 4. Important Lessons Learned
Byte-Level Accuracy Matters

Git hashes raw bytes, not text.

Small differences such as:

- newline characters `(\n)`

- Windows line endings `(\r\n)`

- encoding differences (UTF-8 vs UTF-16)

- missing spaces in the header format

all produce completely different hashes.

During debugging, I discovered:

- PowerShell can create UTF-16 encoded files.

- Even a missing space in "blob {size}\0" changes the hash.

- Hash identity is fully determined by exact byte sequence.

## 5. Verifying Against Native Git

To confirm correctness, I compared the output of:

```bash
python src/hash_object.py mynotes.txt
```

with:
```bash
git hash-object mynotes.txt
```

After fixing header formatting and encoding issues,
the hashes matched exactly.

This confirmed that the implementation reproduces
Git’s blob hashing behavior precisely.

## 6. Key Takeaway

Git’s object model is simple but extremely precise.

It relies on:

- structured headers

- content-addressable storage

- cryptographic hashing