# Git Directory Structure (Core Internals)

In this document, I describe what I learned by manually exploring the `.git/`
directory after running `git init` and creating my first commit.

Instead of treating Git as a black box, I observed how it stores data internally
using simple files, references, and hashes.

---

## 1. What the `.git/` directory represents

The `.git/` directory is the core of a Git repository.

While using Git normally hides this complexity, all version control data is
stored here as plain files and folders. Git does not use a traditional database.
Its design is based on:
- simple file storage
- references between files
- cryptographic hashes

Understanding `.git/` makes Git’s behavior predictable rather than magical.

---

## 2. How `HEAD` defines the current state

The `HEAD` file tells Git where I am currently positioned in the repository.

When I opened the `HEAD` file, I saw:

ref: refs/heads/master


This showed me that:
- `HEAD` does not directly store a commit hash
- it points to a branch reference
- the branch reference later points to a commit

The pointer flow becomes:
HEAD → branch → commit


This indirection allows Git to switch branches without rewriting history.

---

## 3. Branches are simple reference files

Branches are stored as plain text files inside:
.git/refs/heads/


Before creating my first commit, I noticed that the branch file did not exist.
This made it clear that Git does not create unnecessary references.

After making the first commit, Git created the branch file and stored a
40-character SHA-1 hash inside it. This hash represents the commit.

This observation helped me realize that branches are not complex structures —
they are just pointers.

---

## 4. Commits are identified by content, not names

Git does not track commits using version numbers or labels.

Each commit is identified by a SHA-1 hash that is generated from its content.
If the content changes, the hash changes as well.

This makes Git a content-addressable system, where integrity is guaranteed by
cryptographic hashing rather than manual tracking.

---

## 5. How Git stores data as objects

All Git data is stored inside:
.git/objects/


After creating the first commit, I observed directories named using the first
two characters of object hashes, with files named using the remaining characters.

Using this structure, Git stores:
- file contents as blobs
- directory structures as trees
- repository snapshots as commits

All of these are stored using the same object mechanism.

---

## 6. What clicked for me

By exploring `.git/` directly, I realized that Git is internally very simple.

It is built from:
- small text files
- pointer-based references
- hashed content

This understanding forms the foundation for implementing Git behavior from
scratch in the next steps of this project.