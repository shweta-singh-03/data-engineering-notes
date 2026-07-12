# Complete Git & GitHub Study Notes (Follow-Along Guide)

> Based on: *"Complete Git and GitHub Tutorial For Data Engineers (2025)"*
> This is a **hands-on / project-based** tutorial, so these notes are structured as a **numbered follow-along guide**. Every command is shown in the exact order it was run, with the "why" behind it.

---

## Prerequisites (Set Up Before You Start)

| Tool | Why you need it | How to get it |
|---|---|---|
| **VS Code** | Acts as your code editor **and** terminal in one place. Not mandatory for Git, but widely used, free, cross-platform. | Search "VS Code download" → pick your OS (Windows/Mac/Linux) → install |
| **Git** | The actual version-control software you're learning. | Search "git download" → pick your OS → install |
| **Git Graph extension (VS Code)** | Lets you *see* your commit history as a visual graph instead of reading raw text logs. | VS Code → Extensions → search "Git Graph" → Install |
| **GitHub account** | Needed later for remote repositories, push/pull, pull requests. | Create free account at github.com |

🌟 **Analogy for the whole course**: Think of Git like the "Undo/Redo + Save Versions" feature in a video game, but for code — except multiple people can play (edit) different "save files" (branches) of the same game world at once, and later merge their progress together.

⚠️ **Installer gotcha (Windows)**: During Git installation, on the page asking for the default editor, make sure you select **"Use Visual Studio Code as Git's default editor"** — otherwise Git defaults to Vim, which is confusing for beginners when writing commit messages.

⚠️ The tutorial deliberately uses **plain text files** (`.txt`, `.md`) instead of Python/SQL/any language files. This is intentional — Git treats every file the same way regardless of language, so using plain text removes distractions and keeps focus purely on Git concepts.

### Terminal choice
- Windows: **PowerShell** is recommended (used throughout this course) — it's OS-friendly and Linux-like commands (`ls`, `touch`) don't fully work in classic **Command Prompt**.
- **Git Bash** (installed alongside Git) is also an option but not used in this course.
- Open terminal in VS Code: `Ctrl + Shift + ` ` (backtick) or via the "..." menu → Terminal → New Terminal.

---

## Section 1 — What is Git, GitHub, and a Repository?

### What is Git?
Git is a **version control system** — software installed on your local machine that tracks every change you make to your files/code over time, letting you "time travel" between versions.

### What is GitHub?
GitHub is a **cloud platform that hosts Git repositories online**. Git is the tool on your computer; GitHub is where you store/share that work so teams can collaborate, review code, and track issues.

```
┌─────────────────────┐        push/pull        ┌─────────────────────┐
│   LOCAL MACHINE      │  ───────────────────►   │   GITHUB (CLOUD)     │
│   (Git installed)    │  ◄───────────────────   │  Remote Repository   │
│   Your Repository    │                          │  (shared with team)  │
└─────────────────────┘                          └─────────────────────┘
```
*Caption: Git = local tool; GitHub = cloud host for your Git repo. Code moves between them via `push` (local→cloud) and `pull`/`clone` (cloud→local).*

🌟 **Analogy**: Git is like Microsoft Word's "Track Changes + Save As version 1, 2, 3" on your own laptop. GitHub is like uploading that Word file to Google Drive so your teammates can access, edit, and merge their versions too.

### What is a Repository ("repo")?
A **repository** is just a normal project folder that Git is tracking. Casually called a "repo." It contains your code, documentation, and the full **history of changes**. It can live:
- **Locally** (on your computer)
- **Remotely** (hosted on GitHub)

⚠️ A folder only becomes a "repository" once you run `git init` inside it (see Step 3 below). Before that, it's just a plain directory — Git has no awareness of it.

### Interview Questions
1. **Q: What is the difference between Git and GitHub?**
   A: Git is a version-control *software* installed locally that tracks file history. GitHub is a *cloud platform* that hosts Git repositories so teams can collaborate remotely.
2. **Q: What is a repository in Git terms?**
   A: A project folder converted into a version-tracked unit via `git init` (or created remotely then cloned); it holds code + the `.git` history database.
3. **Q: Scenario — Your teammate says "clone my repo," but you've never used Git before. What would you tell them you need first?**
   A: You'd need Git installed locally, a terminal/editor, and the repo's URL to run `git clone <url>`.
4. **Q: Can a repository exist without ever touching GitHub?**
   A: Yes — a purely local Git repository (via `git init`) is fully functional for version control; GitHub is only needed for remote hosting/collaboration.

---

## Section 2 — Initializing Your First Repository

### Step 1: Confirm you're NOT yet in a Git repo
```bash
git status
```
**Why:** Best practice — always run `git status` first, on any folder, to understand its current state.
Expected output (before init): `fatal: not a git repository (or any of the parent directories): .git`

### Step 2: Configure your identity (one-time, global)
```bash
git config --global user.email "your_email@gmail.com"
git config --global user.name "YourName"
```
**Why:** Every commit needs an author identity attached to it, so collaborators know who made which change. The `--global` flag means you only do this **once ever** on your machine — it applies to all future repositories automatically.

✅ **Checkpoint:** No output means success. You only need to redo this if you want to change identity (e.g., switch to your GitHub username/email later).

### Step 3: Initialize the repository
```bash
git init
```
**Why:** This is the **single command** that converts a plain folder into a Git repository. It creates a hidden `.git` folder — the "brain"/database of your repo that stores all history, commits, and branches.

✅ **Checkpoint:** Run `git status` again — it should now say:
```
On branch master
No commits yet
nothing to commit
```

⚠️ **Common confusion**: You won't *see* the `.git` folder by default because it's hidden. To reveal it in VS Code: Settings → search "exclude" → remove `.git` from the excluded files list. (You can look at it, but **never manually edit files inside `.git`** — it's the backbone of your version history.)

### Interview Questions
1. **Q: What does `git init` actually do internally?**
   A: It creates a hidden `.git` directory containing the object database, refs, HEAD pointer, and config — turning a normal folder into a Git-tracked repository.
2. **Q: Why is `git config --global` used instead of running config for every repo?**
   A: `--global` stores identity settings at the system/user level so they auto-apply to every repository you create or clone, avoiding repetitive setup.
3. **Q: Scenario — You run `git status` and get "not a git repository." What's your fix?**
   A: Run `git init` in that folder to initialize it as a Git repository.
4. **Q: Should you ever manually edit files inside the `.git` folder?**
   A: No — it's the internal database Git relies on; manual edits can corrupt your entire history.

---

## Section 3 — Core Concepts: Working Directory → Staging Area → Repository

### The 3-stage flow
```
 ┌────────────────────┐     git add      ┌────────────────┐     git commit     ┌────────────────┐
 │  WORKING DIRECTORY  │ ───────────────► │  STAGING AREA   │ ─────────────────► │   REPOSITORY    │
 │ (create/edit files) │                  │ (snapshot prep) │                    │ (.git database, │
 │  Untracked/Modified │                  │     Staged      │                    │  permanent hist)│
 └────────────────────┘                  └────────────────┘                    └────────────────┘
```
*Caption: Files move through three stages before they're permanently versioned.*

🌟 **Analogy**: Copying files on your computer — **selecting** files (Ctrl+C) = staging (`git add`), **pasting** them (Ctrl+V) into a destination = committing (`git commit`). You choose *which* files to bundle together before finalizing them.

### File states
| State | Meaning | How it's marked in VS Code / `git status` |
|---|---|---|
| **Untracked (U)** | A brand-new file Git has noticed but is not yet tracking | `U` |
| **Modified (M)** | An existing (already-tracked) file that has changes not yet staged | `M` |
| **Staged (A)** | File added to the staging area, snapshot taken, ready to commit | `A` |
| **Committed** | Snapshot permanently saved in repository history | — |

### Worked example — creating and committing files
```bash
# Create a file (via editor "New File" or terminal)
echo "This is another data injection file" > data_ingest.txt   # creates file via terminal command (not a Git command)

git status          # shows data_ingest.txt as Untracked (U)

git add data_ingest.txt      # stage ONE specific file
# OR
git add .                    # stage ALL changed/new files at once (common shortcut)

git status           # file now shows as "Added" (staged)

git commit -m "ingest data"  # commits the staged snapshot with a message
```
✅ **Checkpoint:** After commit, `git status` shows a clean tree (or only remaining untracked files), and Git Graph shows a new commit node.

⚠️ **If you forget `-m "message"`**: Git opens your default editor (VS Code) waiting for a commit message. Type the message, **Save (Ctrl+S)**, then **close the tab** — only then does the commit complete.

### Commit message convention (best practice)
Write commit messages in **simple present tense**, like a command to Git — e.g., `ingest data`, `fix bug`, `add readme` — rather than past tense (`ingested data`). This is an industry convention that keeps history readable.

### Interview Questions
1. **Q: Explain the three states a file passes through before being permanently versioned.**
   A: Working Directory (created/edited, untracked or modified) → Staging Area (`git add`, snapshot prepared) → Repository (`git commit`, permanently recorded).
2. **Q: What's the difference between `git add filename` and `git add .`?**
   A: The first stages only the named file; the second stages *all* new/modified files in the current directory tree at once.
3. **Q: Scenario — You edited 5 files but only want to commit 2 of them. What do you do?**
   A: Use `git add file1 file2` (naming only those two) instead of `git add .`, then `git commit -m "..."`.
4. **Q: Why does Git show "U" for a new file but not for an existing modified file?**
   A: "U" (untracked) applies only to files Git has never tracked before; once a file is tracked, further edits show as "Modified (M)," not untracked.
5. **Q: What happens if you run `git commit` without `-m`?**
   A: Git opens the configured default editor for you to type a message manually; the commit only finalizes once you save and close that editor tab.

---

## Section 4 — HEAD, Logs, and `.git` Internals

### What is HEAD?
**HEAD = the latest commit on the branch you're currently on.** Whenever you create a new branch, it is created starting from the HEAD of the current branch by default.

```
master:  C1 ── C2 ── C3   ← HEAD (points here, the latest commit)
```
*Caption: HEAD always points at the tip/most recent commit of your active branch.*

### Viewing history — `git log`
```bash
git log                 # full detailed history (verbose, hard to read)
git log --oneline       # compact: short commit hash + message per line (RECOMMENDED)
git reflog               # (a.k.a. "ref log") — like log --oneline but also shows HEAD@{n} references, very useful for undoing mistakes
```
🌟 **Analogy**: `git log` is like a detailed diary entry per day; `git log --oneline` is like a bullet-point calendar — much faster to scan.

⚠️ Only the first 6–7 characters of a commit hash are needed to uniquely identify a commit — you don't need the full long hash.

### Registering a branch — the "initial commit" rule
A branch is **not recognized by `git branch`** until it has **at least one commit**. That's why almost every project's first commit is literally called "initial commit" — it registers the main/master branch. This only needs to happen once, for the parent branch.

### Interview Questions
1. **Q: What does HEAD represent in Git?**
   A: A pointer to the latest commit on the currently checked-out branch.
2. **Q: Why do new branches by default inherit all prior commits of their parent branch?**
   A: Because a branch is created starting from the HEAD (latest commit) of the branch you're on, so it includes that entire commit history as its ancestor chain.
3. **Q: Scenario — `git branch` shows nothing even though you just ran `git init`. Why?**
   A: The branch has no commits yet; Git doesn't register a branch name until at least one commit exists on it.
4. **Q: Why prefer `git log --oneline` over plain `git log` in daily use?**
   A: It's far more readable — one line per commit (short hash + message) instead of a verbose multi-line block per commit.

---

## Section 5 — `.gitignore` and `.gitkeep`

### Why `.gitignore` matters
Some files should **never** be tracked (e.g., `.env` secrets, credential files, large raw data). `.gitignore` tells Git "track everything except these."

### Step-by-step
1. Create a file named exactly `.gitignore` at the root of your repo (same level as `.git`).
2. Add filenames/patterns, one per line:
   ```
   .env
   API_secrets.txt
   bronze/
   ```
3. Save. Run `git status` — those files disappear from the untracked list.
4. Stage and commit the `.gitignore` file itself (its content is just filenames — safe to track):
   ```bash
   git add .
   git commit -m "gitignore file"
   ```

⚠️ **Gotcha — ignoring folders**: Write the folder name **with a trailing slash** (e.g., `bronze/`) to ignore an entire folder and its contents.

### Special fact: Git does NOT track empty folders
```
Empty folder created  →  git status shows NOTHING (Git ignores empty dirs entirely)
Add a file inside it  →  git status shows the folder as Untracked
```
*Caption: Git only tracks files, never folders directly — an empty folder is invisible to Git.*

**Workaround — keep an empty folder's structure**: create a placeholder file called `.gitkeep` inside it.
```bash
# inside the empty folder you want to preserve (e.g., "silver/")
# create a file named exactly: .gitkeep
git add .
git commit -m "added silver folder"
```
🌟 **Analogy**: Think of `.gitkeep` like putting an empty labeled box on a shelf just to reserve its spot — Git won't track an empty shelf space, but it *will* track a box (even an empty one) if you name it.

### Interview Questions
1. **Q: What is the purpose of `.gitignore`?**
   A: It lists file/folder patterns Git should never track (e.g., secrets, `.env`, generated data), keeping the repo clean and secure.
2. **Q: Why doesn't Git track empty folders?**
   A: Git's data model tracks file *content* (blobs), not directories as standalone objects; a folder with zero files has nothing to snapshot.
3. **Q: How do you preserve an empty folder's structure in a Git repo?**
   A: Add a placeholder file (commonly `.gitkeep`) inside it so Git has something to track, making the folder "exist" once committed.
4. **Q: Scenario — You accidentally committed a `.env` file with secrets before adding it to `.gitignore`. Does adding it to `.gitignore` now remove it from history?**
   A: No — `.gitignore` only prevents *future* tracking of untracked files. A file already committed must be explicitly removed from tracking (e.g., `git rm --cached` and a new commit) and, for full removal from history, the commit history itself would need rewriting.

---

## Section 6 — Branches (The Heart of Git)

### Why branches exist
In real teams, multiple developers work on the same project but on **different, isolated tasks** in parallel — without waiting for each other or interfering with each other's code.

```
                     C1───C2───C3   ← master (HEAD)
                              │
                              └──── feature_1 (created from master's HEAD)
                                     C4───C5   ← developer XYZ works here, isolated
```
*Caption: A feature branch is created from the HEAD of its parent branch and evolves independently until merged back.*

### Key commands
```bash
git branch                 # list all branches (current one is marked)
git switch master           # switch to an existing branch (modern command, post-2019)
git switch -c feature_1     # create AND switch to a new branch in one step
git checkout master          # OLDER, multi-purpose command — same switching effect
git checkout -b feature_1    # OLDER equivalent of "switch -c"
```

| Old way | New way (post-2019) | Notes |
|---|---|---|
| `git checkout <branch>` | `git switch <branch>` | Switch to existing branch |
| `git checkout -b <branch>` | `git switch -c <branch>` | Create + switch to new branch |

⚠️ `git checkout` is a **heavy-duty, multi-purpose** command (can switch branches, create branches, and even discard file changes) — this is exactly why Git introduced `git switch` in 2019: a focused command that *only* handles branch switching/creation, reducing accidental mistakes.

### Best practice: always go to master first
Before creating a new feature branch, explicitly `git switch master` first — even if you think you're already there — to guarantee the new branch is based on master's HEAD, not some other branch's HEAD by mistake.

### Worked example
```bash
git switch master
git switch -c feature_1        # create feature_1 branch from master's HEAD
# ... edit files ...
git add .
git commit -m "added more data"

git log --oneline               # shows ALL ancestor commits too (inherited from master)
```
✅ **Checkpoint:** Git Graph now shows `feature_1` one commit ahead of `master`; switching branches with `git switch master` shows the file WITHOUT the feature branch's changes — proof branches are isolated.

### Interview Questions
1. **Q: Why does Git recommend `git switch` over `git checkout` today?**
   A: `git checkout` does too many unrelated things (switch branches, restore files, create branches); `git switch` isolates just branch switching/creation, reducing risk of mistakes.
2. **Q: What determines the starting point (base) of a new branch?**
   A: By default, the HEAD (latest commit) of whichever branch you're currently on when you create it.
3. **Q: Scenario — You're on `feature_1` and accidentally create a new branch `feature_2` without switching to master first. What's the risk?**
   A: `feature_2` will be based on `feature_1`'s HEAD (including all its unfinished changes) instead of master's clean HEAD — polluting the new branch with unintended commits.
4. **Q: How do you prove two branches are truly isolated from each other?**
   A: Make a change/commit on one branch, then switch to the other branch and observe the file does NOT show that change — confirming isolation.
5. **Q: What is an "ancestor commit" in the context of branches?**
   A: The commit from which a branch was created — all commits before that point are inherited automatically into the new branch's history.

---

## Section 7 — Merging Branches

### Fast, conflict-free merge (different files touched)
```bash
git switch master           # go to the branch you want to merge INTO
git merge feature_lambda_1   # merges feature_lambda_1's commits into master
```
If the two branches touched **completely different files**, Git merges automatically without any conflict, creating a **merge commit**.

```
master:      C1───C2──────────────M   ← merge commit (M) combines both branches
                    \             /
feature_lambda:      C3───C4────
```
*Caption: A three-way / non-fast-forward merge creates a special merge commit joining two diverged histories.*

### Merge Conflicts — why they happen
A conflict occurs when **two branches modify the same lines of the same file** relative to their shared ancestor commit — Git can't automatically decide whose version is "correct," even if the literal same line wasn't touched (Git compares whole-file version lineage, not just line-by-line).

### Worked conflict example
```bash
git switch master
git switch -c bug_fix          # developer A's branch
# edit data_ingest.txt line 3, e.g. remove "love", change wording
git add .
git commit -m "fix bug"

git switch master              # tech lead also edits SAME file differently
# edit data_ingest.txt differently
git add .
git commit -m "bug is fixed"

git merge bug_fix               # ← CONFLICT!
```

### Resolving conflicts — two methods
**Method 1: Merge Editor (VS Code UI)**
- Click "Resolve in Merge Editor"
- Options per hunk: **Accept Current Change**, **Accept Incoming Change**, **Accept Both Changes**, or manually type a custom combined result
- Click **Complete Merge** when done

**Method 2: Manual editing (in the raw conflict markers)**
```
<<<<<<< HEAD (current change / master)
I am ingesting the data.
=======
I am not ingesting the data in this file, bug is fixed.
>>>>>>> bug_fix (incoming change)
```
Manually delete the `<<<<<<<`, `=======`, `>>>>>>>` markers and keep whichever text (or combination) you want.

⚠️ **Non-negotiable final step after resolving ANY conflict:**
```bash
git add .
git commit -m "conflict resolved"
```
Resolving the visual conflict is not enough — you must stage and commit to actually conclude the merge.

✅ **Checkpoint:** `git status` after resolving but before committing says: *"All conflicts fixed but you are still merging"* — this confirms you still need `git add` + `git commit`.

### Comparison: Merge outcome types
| Merge Type | When it happens | Result |
|---|---|---|
| **Fast-forward merge** | Target branch has no new commits since the source branch diverged | No merge commit; history looks like a straight line |
| **Three-way / non-fast-forward merge** | Both branches have new commits since diverging | Creates a special **merge commit** joining both histories |
| **Conflicted merge** | Same file/lines changed differently on both branches | Git pauses and asks you to manually resolve before committing |

### Aborting a merge
```bash
git merge --abort
```
**Why:** Instantly cancels an in-progress conflicted merge and returns you to the pre-merge state — useful when you decide you don't actually want to merge right now (e.g., "the other person's branch isn't needed anymore").

### Interview Questions
1. **Q: What causes a merge conflict even if two commits don't touch the exact same line of code?**
   A: Git tracks each branch's version lineage of the *whole file* from a common ancestor; if both branches diverge in how the file should look at the same point in history, Git can't auto-resolve which version is authoritative, even without literal line overlap.
2. **Q: What is the difference between a fast-forward merge and a three-way merge?**
   A: Fast-forward simply moves the branch pointer forward (no new commit) because the target has no divergent commits; a three-way merge creates a new merge commit because both branches have independent commits to reconcile.
3. **Q: Scenario — after resolving a conflict in the Merge Editor, `git status` still shows the merge as unfinished. What step did you forget?**
   A: You must run `git add .` (to stage the resolved files) and `git commit` — resolving visually isn't enough to conclude the merge.
4. **Q: How would you cancel a merge you just realized you don't want, mid-conflict?**
   A: `git merge --abort`.
5. **Q: If both branches touch entirely different files, will a merge conflict occur?**
   A: No — merges across non-overlapping files complete automatically and cleanly (usually creating a straightforward merge commit).

---

## Section 8 — Rebase

### What is Rebase?
Rebase **moves ("re-bases") the starting point of a branch** to a different, usually more recent, commit — rewriting the branch's history to look as if it was created from that new point.

```
BEFORE REBASE:
master:   C1───C2───C3
               \
feature:        C4───C5

AFTER "git rebase master" (run while on feature):
master:   C1───C2───C3
                     \
feature:              C4'───C5'   (commits re-created on top of C3)
```
*Caption: Rebase relocates a branch's commits onto a new base commit, producing a cleaner, linear history.*

### Commands
```bash
git switch feature_branch     # go to the branch you want to move
git rebase master              # rebase onto master's current HEAD
```
Then, to merge cleanly afterward:
```bash
git switch master
git merge feature_branch        # this will now be a FAST-FORWARD merge (clean, no merge commit)
```

### Comparison: Merge vs Rebase
| Aspect | Merge | Rebase |
|---|---|---|
| History shape | Branching/diverging graph, has merge commits | Clean, linear history |
| Rewrites commit history? | No | Yes (creates new commits on top of new base) |
| Best for | Preserving exact chronological/branching record | Cleaner history before merging into main |
| Conflict handling | Same principle — resolve, then `add` + `commit` | Same principle — resolve, then `git rebase --continue` (conceptually same steps) |

⚠️ Rebase conflicts are resolved **exactly the same way** as merge conflicts (pick current/incoming/both, then stage and continue).

🌟 The instructor's personal recommendation: use **rebase + fast-forward merge** together for the cleanest possible project history.

### Interview Questions
1. **Q: In one sentence, what does `git rebase` do?**
   A: It moves a branch's commits to originate from a new base commit, replaying them on top and producing new commit hashes.
2. **Q: Why do teams often prefer rebase before merging into main?**
   A: It produces a clean, linear history (fast-forward merge) instead of a tangled graph full of merge commits.
3. **Q: Scenario — after `git rebase master`, do the commit hashes on the rebased branch stay the same?**
   A: No — rebase recreates the commits on the new base, so they get new commit hashes even though the content/message may look identical.
4. **Q: Is rebase considered "safe" to use on a shared/public branch that others have already pulled?**
   A: Generally no (though not explicitly detailed in this transcript's basic coverage) — rewriting history that others have already based work on can cause major confusion; rebase is safest on local/unshared branches.

---

## Section 9 — Time Travel: `git reset` and `git reflog`

### Undoing a commit — going back in time
```bash
git reflog                     # shows detailed history WITH HEAD@{n} references (better for undo purposes than git log)
git reset --hard <commit_id>    # move HEAD (and branch) back to a specific commit — RECOMMENDED (uses exact commit ID)
git reset --hard HEAD~1         # alternative: move back exactly 1 commit from current HEAD (modern syntax; older "HEAD@{1}" syntax is deprecated)
```

🌟 **Analogy**: `git reflog` is like a black-box flight recorder — even actions like resets and deleted commits are logged, letting you "undo the undo" if needed.

⚠️ Preferred approach: use the **exact commit ID** (found via `git reflog` or `git log --oneline`) rather than relative references like `HEAD~1`, because the commit ID is the definitive "source of truth" and doesn't shift as HEAD moves.

### Worked example — recovering a deleted file
```bash
# Accidentally delete data_ingest.txt and commit the deletion
git add .
git commit -m "delete file data_ingest.txt"

git reflog                      # find the commit ID BEFORE the deletion
git reset --hard <that_commit_id>    # restores repo (and the file) to that exact point
```
✅ **Checkpoint:** File reappears in your working directory; `git reflog` now logs a new entry: "reset moving to <commit_id>".

### `git diff` — comparing states
```bash
git diff                # compares WORKING DIRECTORY vs STAGING AREA
git diff --staged       # compares STAGING AREA vs REPOSITORY (last commit)
```
Reading the output:
- `-` (minus) = source/original side
- `+` (plus) = destination side
- `@@` = line number marker

### Un-staging (revert staging without losing edits)
```bash
git reset               # moves staged changes back to "modified" (working directory) state — does NOT delete your edits, just un-stages them
```
If you specify a filename, only that file is un-staged; without one, all staged files are reverted to modified state.

### Interview Questions
1. **Q: What's the safest way to identify exactly which commit to reset to?**
   A: Use `git reflog` or `git log --oneline` to get the exact commit hash, then `git reset --hard <commit_id>` — avoiding relative pointers that shift as HEAD changes.
2. **Q: Scenario — you deleted an important file and already committed the deletion. How do you get it back?**
   A: Find the commit hash right before the deletion via `git reflog`, then run `git reset --hard <that_commit_id>`.
3. **Q: What's the difference between `git diff` and `git diff --staged`?**
   A: `git diff` compares your working directory against the staging area (unstaged changes); `git diff --staged` compares the staging area against the last commit (what will actually be committed).
4. **Q: If you run `git reset` (no flags) on staged files, do you lose your code changes?**
   A: No — it only un-stages the files, moving them back to "modified" in the working directory; your actual edits remain intact.
5. **Q: Why is `git reflog` considered more useful than `git log` for undo scenarios?**
   A: It captures HEAD movement events (resets, checkouts, rebases) with `HEAD@{n}` references, giving visibility into actions that `git log` alone wouldn't show as clearly.

---

## Section 10 — Cherry-Picking

### What is Cherry-Pick?
Cherry-picking lets you take **one specific commit** from a branch and apply it onto another branch — **without** merging the entire branch.

```
feature branch:   C1(bug fix) ── C2(new feature dev)
                        │
                        └────────► cherry-picked onto master
master:    Cm1 ── Cm2 ── C1'   (only the bug-fix commit applied, new commit ID assigned)
```
*Caption: Cherry-pick copies a single commit's changes onto another branch as a brand-new commit (new commit ID, same content).*

### Commands
```bash
git switch master              # cherry-pick target must be checked out FIRST
git reflog                     # or git log --oneline — find the exact commit ID you want
git cherry-pick <commit_id>     # applies just that commit onto current branch
git cherry-pick <id1> <id2> <id3>   # can cherry-pick MULTIPLE commits — must be in the SAME chronological order they were originally applied, otherwise can create conflicts
```

⚠️ The cherry-picked commit is **NOT** the same commit — it gets a brand-new commit ID on the target branch (content stays the same, but it's technically a distinct commit object).

### Real-world use case
🌟 **Analogy**: Imagine a critical hotfix sitting in your `dev` branch, but production needs it *right now* — you don't want to wait for the whole dev branch (with unfinished/untested features) to go through QA. Cherry-pick lets you grab just that one hotfix commit and apply it straight to production.

### Interview Questions
1. **Q: What problem does cherry-picking solve that a full branch merge doesn't?**
   A: It lets you selectively bring over just one (or a few) specific commits, without pulling in unrelated/unfinished commits from the rest of the branch.
2. **Q: Does a cherry-picked commit keep the same commit hash as the original?**
   A: No — it's recreated as a new commit object with a new hash on the target branch, even though the content/message is identical.
3. **Q: Scenario — you need to cherry-pick 3 commits that all modified the same file in sequence. What must you be careful about?**
   A: Apply them in the exact same chronological order they were originally created; applying out of order can create conflicts since later commits may depend on earlier changes to the same file.
4. **Q: Give a real production scenario where cherry-picking is the ideal tool.**
   A: Promoting an urgent hotfix commit directly from a dev branch straight to production, bypassing the full QA-promotion pipeline that the rest of the dev branch would need.

---

## Section 11 — Stashing

### What is Stash?
Stash is **temporary storage** for uncommitted changes, letting you switch branches cleanly without committing half-finished work.

### The problem it solves
```
Scenario:
1. You're deep in development on branch "dev_one" (uncommitted changes)
2. Your manager says: "URGENT bug on master — fix it now!"
3. You try: git switch master
4. Git blocks you: "local changes would be overwritten by checkout, please commit or stash them"
```

### Solution flow
```
WORKING DIRECTORY (uncommitted work)  ──git stash push──►  STASH (temporary storage, stack-based)
        │                                                          │
        ▼ (branch is now clean, safe to switch)                   │
   git switch master → fix urgent bug → commit → done              │
        │                                                          │
        ▼                                                          │
   git switch dev_one → git stash pop  ◄────────────────────────────
   (work restored exactly as it was)
```
*Caption: Stash is a stack; your paused work sits safely until you're ready to bring it back with `apply` or `pop`.*

### Commands
```bash
git stash push -m "my development paused"     # save current uncommitted changes (RECOMMENDED — use "push", not bare "stash")
git stash list                                 # view all stashes (stack: latest on top, indexed from 0)
git stash apply                                # re-apply the LATEST stash, but KEEP it in the stash list
git stash apply "stash@{0}"                    # apply a SPECIFIC stash by index (note: wrap in double quotes due to special characters { })
git stash pop                                   # re-apply the LATEST stash AND remove it from the stash list
```

⚠️ **Important**: `git stash pop` will refuse to remove the stash from the list until the restored changes are actually **committed** — this is a safety guardrail.

⚠️ **Special-character gotcha**: When referencing a specific stash index like `stash@{0}`, wrap it in double quotes (e.g., `"stash@{0}"`) because of the curly braces `{}` — otherwise the shell may throw an "unknown switch" error.

### Key insight: Stash is repo-wide, not branch-specific
A stash created while on one branch can be applied/popped on **any** branch in the same repository — stashes are shared across the whole repo, not locked to their originating branch.

### Interview Questions
1. **Q: What problem does `git stash` solve?**
   A: It lets you temporarily save uncommitted work so you can safely switch branches (e.g., for an urgent fix) without committing half-finished code.
2. **Q: What's the difference between `git stash apply` and `git stash pop`?**
   A: `apply` restores the stashed changes but keeps them in the stash list; `pop` restores them AND removes that entry from the stash list.
3. **Q: Scenario — you `stash` your work, switch branches, and try to `pop` before committing anything. Does Git allow overwriting risk?**
   A: Git applies safety checks — if popping would overwrite uncommitted local changes, it warns you; you generally need a clean working directory (or committed changes) before popping safely.
4. **Q: Is a stash tied to the branch it was created on?**
   A: No — stashes are stored at the repository level and can be applied to any branch, not just the one they were created on.
5. **Q: How do you view all currently saved stashes and their order?**
   A: `git stash list` — shows them like a stack, with the most recently created stash at index 0 (top).

---

## Section 12 — Working with GitHub (Remote Repositories)

### Setting up
1. **Create a GitHub account** (username, email, verified).
2. Update your local Git identity to match your GitHub account (optional but recommended for consistency):
   ```bash
   git config --global user.email "your_github_email@gmail.com"
   git config --global user.name "your_github_username"
   ```
3. On GitHub: **New Repository** → give it a name → choose Public/Private → optionally check "Add README" (sets `main` as the default branch name).

### Personal Access Token (PAT) — required for HTTPS push
GitHub requires proof you own a repo before letting you push code.
**Steps to create a PAT:**
1. GitHub → Profile picture → **Settings**
2. **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token** → copy it immediately (it won't be shown again — store it securely!)

⚠️ HTTPS vs SSH: This course uses **HTTPS** (simpler for beginners). SSH is the other common method (not covered in depth here).

### Scenario A: You already have a LOCAL repo, want to push it to a NEW remote repo
```bash
git remote -v                                      # check existing remotes (should be empty)
git remote add origin <repository_HTTPS_URL>        # set the destination ("origin") for pushes
git remote -v                                      # confirm origin was added

git branch -m main                                  # rename local "master" branch to "main" to match GitHub's default (good practice, not mandatory)

git push origin main                                 # attempt push → prompts sign-in (browser or token)
```
⚠️ **Common error**: `! [rejected] main -> main (fetch first)` — happens when the remote repo already has commits (e.g., from the auto-generated README) that your local repo doesn't have.
**Fix:**
```bash
git pull origin main --allow-unrelated-histories     # merges the two unrelated commit histories (needed because local repo was created from scratch, not cloned)
```
This will prompt for a merge commit message (accept default is fine). Then:
```bash
git push origin main                                  # now succeeds
```

✅ **Checkpoint:** Refresh your GitHub repo page — all your local files and folders now appear there.

### Scenario B: You already have a REMOTE repo on GitHub, want to clone it locally (the MORE COMMON real-world flow)
```bash
git clone <repository_HTTPS_URL>          # downloads the full repo (all files + full history) into a new local folder
cd <cloned_folder_name>
git status                                # confirm you're on "main" and up to date with origin/main
```
🌟 **Note:** After cloning, `origin` is **automatically configured** for you — you don't need to run `git remote add origin` manually (unlike Scenario A).

**Typical contribution workflow after cloning:**
```bash
git switch -c feature_1          # NEVER commit directly to main — always branch first
# ...create/edit files...
git add .
git commit -m "opensource contribution"

git push origin feature_1         # push the FEATURE branch (not main!) to GitHub — this is the standard team practice
```
⚠️ **Best practice reinforced repeatedly in the video**: Never merge your feature branch into main *locally* and push main. Instead, always push the **feature branch** to the remote and do the merge **on GitHub** via a Pull Request — this allows code review before merging.

### Creating and merging a Pull Request (PR) on GitHub
1. After pushing a feature branch, GitHub shows a banner: **"Compare & pull request"** → click it.
2. Add a title/description.
3. Review the diff (Split view = side-by-side old vs new; Unified view = single combined view).
4. Click **Create pull request**.
5. Click **Merge pull request** → **Confirm merge**.
6. Optionally **Delete branch** afterward (cleanup — the feature branch is no longer needed once merged).

✅ **Checkpoint:** Go to the repo's main branch — the new file/change from your feature branch now appears there.

### Interview Questions
1. **Q: Why do you need a Personal Access Token to push code via HTTPS?**
   A: GitHub needs proof that you are the authorized owner/collaborator of the repository before accepting pushes; the PAT authenticates you (replacing password-based auth).
2. **Q: What's the difference between the two ways of starting a GitHub-connected project (local-first vs remote-first)?**
   A: Local-first: `git init` locally, then `git remote add origin <url>` and push (may need `--allow-unrelated-histories` if the remote already has commits). Remote-first: create repo on GitHub first, then `git clone <url>` locally — this is the more common, safer real-world flow since `origin` is auto-configured.
3. **Q: Why does `git push` sometimes fail with "fetch first" / "rejected"?**
   A: The remote branch has commits your local branch doesn't have (e.g., an auto-created README); you must `git pull` (and merge) those changes first before pushing.
4. **Q: Why is it considered best practice to push feature branches instead of merging locally and pushing main?**
   A: It enables team code review via Pull Requests on GitHub before changes reach the main branch, rather than bypassing review by merging privately and pushing directly.
5. **Q: What does `--allow-unrelated-histories` do and when is it needed?**
   A: It forces Git to merge two branches/repos whose commit histories share no common ancestor — needed when a from-scratch local repo (with its own initial commit) is merged with a GitHub repo that has its own separate initial commit (e.g., from an auto-generated README).
6. **Q: Scenario — After cloning a repo, do you need to configure `origin` manually?**
   A: No — `git clone` automatically sets the cloned URL as your `origin` remote.

---

## Full Step-by-Step Recap Checklist

Use this to redo the entire project from scratch without rewatching the video.

- [ ] 1. Install VS Code and Git.
- [ ] 2. Install the "Git Graph" extension in VS Code (optional but recommended).
- [ ] 3. Open (or create) a project folder in VS Code, open the integrated terminal (PowerShell recommended).
- [ ] 4. Run `git status` → confirm it's not yet a Git repo.
- [ ] 5. Run `git config --global user.email "..."` and `git config --global user.name "..."` (one-time).
- [ ] 6. Run `git init` to initialize the repository.
- [ ] 7. Create a file (e.g., `README.md`), then `git add .` and `git commit -m "initial commit"` to register the branch.
- [ ] 8. Practice creating/editing more files → `git add` → `git commit` cycle repeatedly.
- [ ] 9. Explore `git log --oneline` and `git reflog` to view history.
- [ ] 10. Create a `.gitignore` file, list files/folders to exclude (e.g., `.env`, `bronze/`).
- [ ] 11. Use `.gitkeep` to preserve any empty folder you want tracked.
- [ ] 12. Create a feature branch: `git switch -c feature_1`.
- [ ] 13. Make commits on the feature branch; switch back to master to confirm isolation.
- [ ] 14. Merge a conflict-free branch: `git switch master` → `git merge feature_branch`.
- [ ] 15. Deliberately create a merge conflict (edit same file on two branches) and practice resolving it via the Merge Editor AND manually, then `git add .` + `git commit`.
- [ ] 16. Practice `git merge --abort` to cancel an unwanted merge.
- [ ] 17. Practice `git rebase master` from a feature branch, then merge (should be fast-forward).
- [ ] 18. Practice `git reset --hard <commit_id>` to undo a mistaken commit (e.g., recover a deleted file), using `git reflog` to find the commit ID.
- [ ] 19. Practice `git diff` and `git diff --staged`.
- [ ] 20. Practice `git cherry-pick <commit_id>` to bring a single commit onto another branch.
- [ ] 21. Practice `git stash push -m "..."`, `git stash list`, `git stash apply`, and `git stash pop`.
- [ ] 22. Create a free GitHub account.
- [ ] 23. Generate a Personal Access Token (Settings → Developer settings → Tokens classic).
- [ ] 24. **Option A**: `git remote add origin <url>` on an existing local repo → `git push origin main` (handle `--allow-unrelated-histories` if needed).
- [ ] 25. **Option B (preferred)**: Create the repo on GitHub first → `git clone <url>` locally.
- [ ] 26. Create a feature branch after cloning, make a change, commit, and `git push origin <feature_branch>`.
- [ ] 27. On GitHub, open "Compare & pull request," review the diff, and merge the Pull Request.
- [ ] 28. Optionally delete the merged feature branch.

---

## Final Revision Cheat Sheet

### Core mental model
```
WORKING DIRECTORY  --add-->  STAGING AREA  --commit-->  REPOSITORY (.git)
      (local files)                                          │
                                                               │ push / pull / clone
                                                               ▼
                                                          GITHUB (remote)
```

### Rapid-fire Q&A
- **Q: Git vs GitHub?** → Git = local tool; GitHub = cloud host.
- **Q: Repo?** → A Git-tracked project folder.
- **Q: HEAD?** → Pointer to the latest commit on the current branch.
- **Q: Untracked vs Modified?** → Untracked = brand-new file; Modified = existing tracked file changed.
- **Q: Staging area purpose?** → Lets you selectively "snapshot" only chosen changes before committing.
- **Q: `git switch` vs `git checkout`?** → `switch` is the modern, focused command just for branch switching/creation; `checkout` is older and multi-purpose.
- **Q: Fast-forward merge?** → No divergent commits on target → pointer just moves forward, no merge commit.
- **Q: Three-way merge?** → Both branches diverged → creates a merge commit.
- **Q: Merge conflict cause?** → Same file's version lineage diverges differently on two branches.
- **Q: Rebase?** → Moves a branch's commits onto a new base commit → rewrites history → linear look.
- **Q: Cherry-pick?** → Applies ONE specific commit from another branch (gets a new commit ID).
- **Q: Stash?** → Temporary storage (stack) for uncommitted work so you can switch branches safely.
- **Q: `.gitignore`?** → List of files/patterns Git should never track.
- **Q: `.gitkeep`?** → Placeholder file to force Git to track an otherwise-empty folder.
- **Q: `git reflog` vs `git log`?** → `reflog` also tracks HEAD movements (resets/checkouts), great for undo; `log` shows commit history only.
- **Q: PAT (Personal Access Token)?** → Credential proving repo ownership, required for HTTPS pushes to GitHub.
- **Q: Best practice for team pushes?** → Push feature branches (not main) and merge via Pull Request on GitHub for code review.

### Diagram recap: Branch lifecycle
```
   master:  C1───C2───C3──────────────M
                     \                /
   feature:           C4───C5───────
                       ▲
             created from master's HEAD (C2 in this case)
```
*Caption: A feature branch forks from master's HEAD, evolves independently, then rejoins master via merge (M).*

---

## Key Commands / Code Reference (Quick Copy-Paste)

```bash
# ── SETUP (one-time) ──────────────────────────────
git config --global user.email "you@example.com"
git config --global user.name "yourname"

# ── INITIALIZE ────────────────────────────────────
git init
git status

# ── STAGE & COMMIT ────────────────────────────────
git add <file>
git add .
git commit -m "message in simple present tense"

# ── HISTORY / LOGS ────────────────────────────────
git log
git log --oneline
git reflog

# ── IGNORE FILES ──────────────────────────────────
# .gitignore file contents example:
#   .env
#   API_secrets.txt
#   bronze/
# .gitkeep -> empty placeholder file to force-track an empty folder

# ── BRANCHES ───────────────────────────────────────
git branch                     # list branches
git switch <branch>             # switch to existing branch
git switch -c <branch>          # create + switch (modern)
git checkout <branch>           # switch (older, multipurpose)
git checkout -b <branch>        # create + switch (older)
git branch -m <new_name>        # rename current branch

# ── MERGE ──────────────────────────────────────────
git merge <branch>
git merge --abort               # cancel an in-progress conflicted merge
# after resolving conflicts:
git add .
git commit -m "conflict resolved"

# ── REBASE ─────────────────────────────────────────
git rebase <new_base_branch>
# then, to fast-forward merge:
git switch master
git merge <rebased_branch>

# ── RESET / TIME TRAVEL ────────────────────────────
git reset --hard <commit_id>
git reset --hard HEAD~1
git reset                       # un-stage without discarding edits
git diff                        # working dir vs staging area
git diff --staged               # staging area vs last commit

# ── CHERRY-PICK ─────────────────────────────────────
git cherry-pick <commit_id>
git cherry-pick <id1> <id2>     # apply multiple, in original order

# ── STASH ───────────────────────────────────────────
git stash push -m "message"
git stash list
git stash apply
git stash apply "stash@{0}"
git stash pop

# ── REMOTE / GITHUB ─────────────────────────────────
git remote -v
git remote add origin <url>
git push origin <branch>
git pull origin <branch>
git pull origin <branch> --allow-unrelated-histories
git clone <url>
```

---

*End of notes. These cover the full hands-on flow demonstrated in the tutorial: environment setup → init → staging/committing → HEAD/logs → gitignore/gitkeep → branching → merging/conflicts → rebase → reset/reflog → diff → cherry-pick → stash → GitHub remote workflows (both local-first and clone-first) → Pull Requests.*
