# Databricks DBUtils

## 1. What is DBUtils?

`dbutils` = **Databricks Utilities**

Think of it as a collection of helper tools that Databricks gives you inside a notebook.

A simple analogy from Python:

```text
Python
  ↓
os module
  ↓
work with files/folders/system

Databricks
  ↓
dbutils
  ↓
work with files, folders, notebooks, secrets, widgets, jobs, etc.
```

So:

> **DBUtils provides utilities that help you interact with the Databricks environment and data/storage from your notebook.**

---

# 2. What can DBUtils do?

The lecture shows several major modules:

```text
dbutils
│
├── fs          → Files/folders
├── secrets     → Secrets
├── widgets     → Notebook parameters
├── notebook    → Run/control notebooks
├── jobs        → Job-related operations
├── credentials
├── library
└── meta
```

For your current Data Engineering learning:

### Highest priority

```text
dbutils.fs
dbutils.widgets
dbutils.secrets
dbutils.notebook
```

The lecture focuses mainly on:

```text
dbutils.fs
```

---

# 3. `dbutils.help()`

You can ask Databricks for help:

```python
dbutils.help()
```

This shows the available DBUtils modules.

For a specific module:

```python
dbutils.fs.help()
```

This shows the functions available under `dbutils.fs`.

Think:

```text
dbutils.help()
      ↓
"What can DBUtils do?"

dbutils.fs.help()
      ↓
"What can I do with files/folders?"
```

---

# 4. `dbutils.fs` ⭐⭐⭐

`fs` means **file system**.

It provides commands for working with files and directories.

The lecture demonstrates:

```text
ls
cp
mv
rm
mkdirs
head
put
```

The ones you should know particularly well are:

```text
ls     → list files
cp     → copy
mv     → move
rm     → remove/delete
mkdirs → create directory
```

---

# 5. `dbutils.fs.ls()` ⭐⭐⭐

## What does `ls` mean?

`ls` = **list**

It lists the contents of a directory.

Example:

```python
files = dbutils.fs.ls(
    "abfss://raw@storage.dfs.core.windows.net/staging/"
)
```

Conceptually:

```text
staging/
├── customers/
├── orders/
├── products/
└── file1.json
```

`dbutils.fs.ls()` gives information about the objects in that location.

The returned file information can include things such as:

```text
path
name
size
modification time
```

The lecture uses this to inspect the contents of an ADLS folder.

---

# 6. Why is `ls()` useful in Data Engineering?

This is actually one of the more important ideas from the lecture.

You don't always know exactly which files have arrived.

For example:

```text
ADLS
└── orders/
    ├── orders_01.json
    ├── orders_02.json
    ├── orders_03.json
    └── orders_04.json
```

You can dynamically discover them:

```python
files = dbutils.fs.ls(path)
```

Then process the returned list.

So instead of hard-coding:

```text
orders_01.json
orders_02.json
...
```

you can programmatically inspect the folder.

---

# 7. Using `ls()` for incremental ingestion ⭐⭐⭐

This is probably the **most important practical point** in this lecture.

The instructor describes a traditional code-based incremental-ingestion approach:

```text
ADLS folder
     ↓
dbutils.fs.ls()
     ↓
Get available files
     ↓
Filter files
     ↓
Process only required files
```

For example, suppose:

```text
Already processed:
file1.json
file2.json

New:
file3.json
file4.json
```

Your code can list the directory and determine which files should be processed.

Conceptually:

```text
List files
   ↓
Filter based on some condition
   ↓
Read selected files
   ↓
Ingest
```

This is one way to build **custom ingestion logic without relying on a managed connector**.

---

# 8. List comprehension

The lecture then uses Python list comprehension to extract only the file names.

Conceptually:

```python
file_names = [
    i.name
    for i in content
    if not i.name.endswith("/")
]
```

Why?

Because `dbutils.fs.ls()` returns file information objects, not just strings.

So:

```text
dbutils.fs.ls()
      ↓
FileInfo objects
      ↓
extract .name
      ↓
file names
```

You can then apply more conditions.

For example:

```python
json_files = [
    i.path
    for i in content
    if i.name.endswith(".json")
]
```

This means:

> Give me only files whose name ends in `.json`.

---

# 9. Filtering dynamically

Once you have the file list, you can apply conditions.

For example:

```python
files = [
    i
    for i in content
    if i.name.startswith("orders_")
]
```

You can also filter based on other metadata/conditions available in the returned file information.

This leads to the general pattern:

```text
LIST
 ↓
FILTER
 ↓
PROCESS
```

---

# 10. `dbutils.fs.cp()` ⭐⭐⭐

`cp` = **copy**

Used to copy a file from one location to another.

```python
dbutils.fs.cp(
    source_path,
    destination_path
)
```

Example:

```python
dbutils.fs.cp(
    "abfss://raw@storage.dfs.core.windows.net/source/file.json",
    "abfss://raw@storage.dfs.core.windows.net/archive/file.json"
)
```

Conceptually:

```text
source
  │
  │ COPY
  ▼
destination
```

The original file remains in the source location.

---

# 11. Why copy files in real pipelines?

A common pattern is:

```text
Incoming
   ↓
Process
   ↓
Archive
```

For example:

```text
/raw/incoming/
       ↓
    process
       ↓
 /raw/archive/
```

After successful processing, you may copy or move the file so you don't repeatedly process it.

---

# 12. `dbutils.fs.mv()` ⭐⭐⭐

`mv` = **move**

Instead of keeping the original file in the source location:

```python
dbutils.fs.mv(
    source_path,
    destination_path
)
```

Conceptually:

```text
source
   ↓
 MOVE
   ↓
destination

Original no longer remains at source
```

### `cp` vs `mv`

```text
cp → copy, original remains
mv → move, original is relocated
```

---

# 13. `dbutils.fs.rm()` ⭐⭐⭐

`rm` = **remove**

Used to delete a file or directory.

Example:

```python
dbutils.fs.rm(
    "abfss://raw@storage.dfs.core.windows.net/temp/file.json"
)
```

For directories/subdirectories, you may use recursive deletion where appropriate:

```python
dbutils.fs.rm(path, True)
```

Think:

```text
rm
 ↓
DELETE
```

Be careful with this in production because deleting data is destructive.

---

# 14. `dbutils.fs.mkdirs()` ⭐⭐⭐

`mkdirs` = **make directories**

Used to create a folder.

Example:

```python
dbutils.fs.mkdirs(
    "abfss://raw@storage.dfs.core.windows.net/new_folder"
)
```

Conceptually:

```text
ADLS
  ↓
mkdirs()
  ↓
new_folder/
```

The lecture demonstrates exactly this type of operation.

---

# 15. `dbutils.fs.head()`

`head()` lets you inspect the beginning of a file.

Conceptually:

```python
dbutils.fs.head(
    file_path
)
```

It is useful for quickly looking at file content without fully loading the file into a DataFrame.

Think:

```text
Large file
   ↓
head()
   ↓
First part of file
```

---

# 16. `dbutils.fs.put()`

`put()` can be used to write content to a file.

Conceptually:

```python
dbutils.fs.put(
    file_path,
    "some content"
)
```

This is useful for small text files or utility operations, not for bulk data processing.

---

# 17. Important: DBUtils is NOT your main data-processing tool

This distinction is very important.

You don't normally use:

```text
dbutils.fs
```

to transform millions of rows.

You use:

```text
PySpark
SQL
DataFrames
```

for data processing.

DBUtils is more about:

```text
File operations
Notebook utilities
Secrets
Parameters
Environment operations
```

Think:

```text
DBUtils
   ↓
"Manage/interact with the environment"

PySpark
   ↓
"Process the data"
```

---

# 18. Example: Traditional file-based ingestion

Suppose your folder contains:

```text
raw/incoming/
    orders_001.json
    orders_002.json
    orders_003.json
```

A traditional custom pipeline could look conceptually like:

```python
files = dbutils.fs.ls(input_path)

json_files = [
    f.path
    for f in files
    if f.name.endswith(".json")
]

for file in json_files:
    df = spark.read.json(file)
    # transformations
    # write to Bronze
```

The flow becomes:

```text
ADLS
 ↓
dbutils.fs.ls()
 ↓
Find files
 ↓
Filter files
 ↓
Spark reads selected files
 ↓
Transform
 ↓
Write Bronze
```

This is the kind of **code-based ingestion approach** the lecture is referring to when it talks about manually building incremental ingestion pipelines.

---

# 19. DBUtils and incremental ingestion ⭐⭐⭐

This connects directly to the incremental-ingestion questions you've been asking.

One possible traditional strategy is:

```text
             ADLS
              │
              ▼
       dbutils.fs.ls()
              │
              ▼
        List all files
              │
              ▼
      Determine which are new
              │
              ▼
        Process new files
              │
              ▼
          Bronze
```

You might maintain some state such as:

```text
last_processed_file
last_processed_time
processed file list
```

Then:

```text
Current files
     -
Already processed
     ↓
New files
```

This is conceptually similar to the watermark idea you've already learned.

---

# 20. But don't confuse this with Auto Loader

This is important for modern Databricks.

### Manual approach

```text
dbutils.fs.ls()
     ↓
YOU write filtering/state logic
     ↓
YOU manage ingestion
```

### Auto Loader

```text
Auto Loader
     ↓
Databricks handles file discovery/state
     ↓
Incremental ingestion
```

So `dbutils.fs.ls()` is useful for **custom/manual file handling**, but it is not a replacement for Auto Loader when you need a production-grade scalable file-ingestion mechanism.

---

# 21. `dbutils.notebook.run()` ⭐⭐

The lecture also mentions:

```python
dbutils.notebook.run(...)
```

This allows one notebook to invoke another notebook.

Conceptually:

```text
Notebook A
    ↓
dbutils.notebook.run()
    ↓
Notebook B
```

Historically, this was used to orchestrate notebook workflows programmatically.

The instructor notes that Databricks Jobs now provides a more structured way to create tasks and workflows.

So for your notes:

> **`dbutils.notebook.run()` = programmatically run another notebook.**

But don't treat it as the modern replacement for Jobs.

---

# 22. Other DBUtils modules mentioned

## `dbutils.secrets`

Used to retrieve secrets securely rather than hard-coding sensitive values.

Conceptually:

```text
Secret Scope
     ↓
dbutils.secrets
     ↓
Retrieve secret
```

Useful for things such as:

```text
passwords
tokens
API keys
connection secrets
```

---

## `dbutils.widgets`

Used to create notebook parameters.

Example concept:

```text
Notebook
   ↓
Widget
   ↓
date = 2026-09-29
```

Then the same notebook can run with different values.

This becomes especially useful in parameterized Jobs/pipelines.

---

# 23. Main DBUtils commands to memorize

| Command                  | Purpose                       |
| ------------------------ | ----------------------------- |
| `dbutils.fs.ls()`        | List files/folders            |
| `dbutils.fs.cp()`        | Copy                          |
| `dbutils.fs.mv()`        | Move                          |
| `dbutils.fs.rm()`        | Delete                        |
| `dbutils.fs.mkdirs()`    | Create directory              |
| `dbutils.fs.head()`      | Read beginning of a file      |
| `dbutils.fs.put()`       | Write small content to a file |
| `dbutils.notebook.run()` | Run another notebook          |
| `dbutils.secrets`        | Access secrets                |
| `dbutils.widgets`        | Notebook parameters           |

---

# 24. The most important real-world flow

For your Data Engineering notes, I'd remember this:

```text
                  DBUTILS
                     │
       ┌─────────────┼─────────────┐
       │             │             │
      FS          SECRETS       WIDGETS
       │
       ├── ls       → list files
       ├── cp       → copy
       ├── mv       → move
       ├── rm       → delete
       └── mkdirs   → create folder
```

And specifically for file ingestion:

```text
ADLS
  ↓
dbutils.fs.ls()
  ↓
Discover files
  ↓
Filter files
  ↓
Spark reads files
  ↓
Transform
  ↓
Bronze/Silver
```

---

# 25. One important syntax correction

In a Databricks notebook, you normally use:

```python
dbutils.fs.ls(path)
```

directly because `dbutils` is available in the notebook environment.

You generally don't write:

```python
import DBUtils
```

as the normal way of accessing the notebook utility. The lecture is explaining the concept correctly, but that particular import wording should not be memorized.

---

# ⭐ Final notes

```text
DBUTILS
=======

Databricks Utilities = helper utilities available
inside Databricks notebooks.

Most important module:
dbutils.fs

dbutils.fs.ls(path)
→ list files/folders

dbutils.fs.cp(src, dest)
→ copy

dbutils.fs.mv(src, dest)
→ move

dbutils.fs.rm(path)
→ delete

dbutils.fs.mkdirs(path)
→ create directory

dbutils.fs.head(path)
→ inspect beginning of file

dbutils.fs.put(path, content)
→ write small content

Other useful modules:
dbutils.secrets
→ access secrets

dbutils.widgets
→ notebook parameters

dbutils.notebook.run()
→ run another notebook

Important production concept:
dbutils.fs.ls()
→ can be used in custom/manual file-ingestion
pipelines to discover and filter files.

But:
dbutils.fs.ls() ≠ Auto Loader

Manual:
list → filter → process → maintain state yourself

Auto Loader:
Databricks manages incremental file discovery/state
more automatically.

Memory:
DBUtils = manage/interact with Databricks environment
PySpark = process/transform data
```

### ⭐ The 5 commands I'd memorize first

```text
dbutils.fs.ls()       → LIST
dbutils.fs.cp()       → COPY
dbutils.fs.mv()       → MOVE
dbutils.fs.rm()       → DELETE
dbutils.fs.mkdirs()   → CREATE FOLDER
```

The biggest takeaway from this lecture is **`dbutils.fs.ls()` + filtering files**, because that connects directly to the kind of **manual incremental ingestion** you were asking about earlier. The rest are useful productivity utilities that you can pick up as needed.
