# Commit Objects (Creating Git History)

In this step, I implemented creation of Git commit objects.

While blobs store file contents and trees store directory structure,
commits connect snapshots together and form project history.

---

## 1. Role of Commit Objects

Git organizes repository data as:

blob → file content  
tree → directory snapshot  
commit → project history

A commit records:

- Which tree represents the snapshot
- Who created the snapshot
- When it was created
- A commit message
- (Optionally) a parent commit

---

## 2. Commit Structure

After inspecting a real commit using:
git cat-file -p <commit_hash>

I observed the internal format:

tree <tree_hash>
parent <parent_commit_hash> (optional)
author <name> <email> <timestamp> <timezone>
committer <name> <email> <timestamp> <timezone>

<commit_message>

The entire content is then wrapped as:
commit <size>\0<content>

and stored using the same process as other Git objects:
SHA-1 hashing → zlib compression → `.git/objects/`

---

## 3. Implementation

Implementation:

[`src/commit_tree.py`](../src/commit_tree.py)

The script:

- Accepts a tree hash and message
- Builds a valid commit structure
- Adds timestamp and author information
- Computes SHA-1 of the commit
- Compresses and writes it into `.git/objects/`

---

## 4. Verifying the Commit

After creating a commit using the script:

python src/commit_tree.py <tree_hash> "Initial commit"
I verified it using native Git:

git cat-file -p <commit_hash>

Git successfully printed the commit data, confirming the object
format is correct and interoperable with Git.

---

## 5. Key Takeaway

Commits do not store files directly.

They point to trees, which point to blobs.

This design allows Git to behave like a graph database where
history is formed by linking snapshots together.

At this stage I have implemented:

- Blob objects (content)
- Tree objects (structure)
- Commit objects (history nodes)

This completes Git’s core object model.