# References and History (Updating HEAD)

In this step, I connected the custom commit object to the repository
history so that Git recognizes it as the latest commit.

Previously, I created valid commit objects, but they were not visible
in `git log` because no branch was pointing to them.

This step implements the mechanism behind how Git tracks history.

---

## 1. Understanding Git References

Git history is not discovered by scanning objects.

Instead, Git follows pointers called references (refs).

The relationship looks like:

HEAD → branch → commit → parent commit → ...

The file `.git/HEAD` contains:

ref: refs/heads/main


This means HEAD does not store a commit hash directly.
It points to a branch file.

That branch file contains the hash of the latest commit.

---

## 2. Why the Custom Commit Was Invisible

Although a valid commit object existed inside `.git/objects/`,
no reference pointed to it.

Git only shows commits that are reachable from a reference.

Therefore:

- Object exists → not visible
- Reference updated → becomes history

---

## 3. Updating the Branch Pointer

To make the commit visible, I updated:
.git/refs/heads/main

with the new commit hash.

This moves the branch to the new commit and updates HEAD
because HEAD points to the branch.

---
## 4. Implementation

Implementation:

[`src/update_ref.py`](../src/update_ref.py)

The script:

1. Reads `.git/HEAD` to determine the active branch
2. Resolves the reference path
3. Writes the new commit hash into the branch file

This reproduces the behavior of:
git update-ref

---

## 5. Verifying the Result

After updating the reference:

python src/update_ref.py <commit_hash>
git log

Git displayed the custom commit as the latest commit.

This confirms the commit is now part of repository history.

---

## 6. Key Takeaway

Git history is pointer-based, not file-based.

Objects form a database.
References decide what belongs to history.

By updating the branch reference, a standalone commit
becomes part of the visible commit graph.

At this stage I have implemented:

- Blob objects (content storage)
- Tree objects (directory snapshots)
- Commit objects (history nodes)
- Reference updates (history linking)

This reproduces Git’s core commit workflow from scratch.