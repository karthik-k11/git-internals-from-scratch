# Reading Git Objects (Implementing `cat-file`)

In this step, I implemented the core functionality behind:
git cat-file -p <object_hash>


The goal was to read a stored Git object directly from
`.git/objects/`, decompress it, parse its structure,
and print its content.

This completes the full lifecycle of a Git blob object.

---

## 1. Locating the Object

Git stores objects inside:
.git/objects/

.git/objects
Each object is addressed using its SHA-1 hash.

Given a hash like:

b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0


The object is stored as:

.git/objects/b6/fc4c620b67d95f953a5c1c1230aaab5db5a1b0


The first two characters form the directory name,
and the remaining characters form the file name.

To read an object, I reconstructed this path from the hash.

---

## 2. Decompressing the Object

Git stores objects in compressed form using zlib.

The process for reading is:

1. Open the object file in binary mode.
2. Read the compressed bytes.
3. Decompress the data using `zlib.decompress()`.

After decompression, the raw structure looks like:

blob <size>\0<content>

For example:
blob 5\0hello


---

## 3. Parsing the Object Structure

After decompression, the object contains:

- A header (`blob <size>`)
- A null byte (`\0`)
- The raw content

To extract the content:

1. Split the byte sequence at the first null byte.
2. Separate the header from the content.
3. Validate the object type.
4. Print the content.

This mirrors Git’s internal logic when printing objects.

---

## 4. Implementation

The implementation is available here:

[`src/cat_file.py`](../src/cat_file.py)

This script:

- Reconstructs the object path from the SHA-1 hash
- Reads compressed object data
- Decompresses using zlib
- Parses header and content
- Prints the blob content

---

## 5. Verifying Correctness

To confirm correctness, I compared:
python src/cat_file.py <hash>

with:
git cat-file -p <hash>

Both produced identical output.

This confirms that:

- The object was stored correctly (Day 3)
- The object was read and parsed correctly (Day 4)
- The implementation is interoperable with native Git

---

## 6. Key Takeaway

At this stage, I have implemented both:

- Writing blob objects into Git’s object database
- Reading and interpreting those objects

This completes the full blob object lifecycle:

file → structured object → compressed storage →
retrieval → decompression → parsing → display

Understanding this pipeline provides a strong foundation
for implementing trees and commits in the next steps.
