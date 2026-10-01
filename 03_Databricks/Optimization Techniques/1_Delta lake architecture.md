# Delta Lake Architecture

## 1. What is a Delta Table underneath?

A Delta table **looks like a normal table**, but underneath it is basically a **folder** containing:

```text
Delta Table
   │
   ├── _delta_log/        ← keeps track of table changes
   │
   └── Parquet files      ← actual data
```

### Simple way to think about it

* **Parquet files** = actual data
* **Delta log** = instruction/history about which data files are currently valid

So when you query a Delta table, Databricks first uses the **Delta log** to understand which Parquet files it should read.

---

# 2. What happens when we INSERT data?

Suppose initially we have:

```text
_delta_log/
sales_file1.parquet
```

Now you insert more records.

Databricks can create another Parquet file:

```text
_delta_log/
sales_file1.parquet
sales_file2.parquet
```

The Delta log is updated so Databricks knows that both files are part of the current table.

```text
INSERT
  ↓
New Parquet file
  ↓
Delta log updated
```

### Remember

> **Insert → new data can be written into new Parquet files.**

---

# 3. What happens when we UPDATE?

This is the really important part.

Suppose:

```text
sale_id | amount
--------|-------
1       | 50
2       | 70
3       | 90
```

And we run:

```sql
UPDATE sales
SET amount = 100
WHERE sale_id = 1;
```

The record with `sale_id = 1` is inside a Parquet file.

Parquet files are not normally edited like an Excel cell where you simply open the file and change one value.

So the existing file is rewritten.

Conceptually:

```text
Old file
file1.parquet
    ↓
contains sale_id = 1
    ↓
rewrite
    ↓
New file
file3.parquet
```

The updated record is written into the new file.

---

# 4. But now we have a problem...

We now have:

```text
file1.parquet  ← old version
file3.parquet  ← updated version
```

Both may contain information related to `sale_id = 1`.

So how does Databricks know:

> "Don't read the old file."

### Answer: Delta Log

The **Delta log keeps track of which files are valid and which old files should no longer be read for the current table state.**

Conceptually:

```text
Delta Log

file1.parquet → old / expired
file2.parquet → valid
file3.parquet → valid
```

So when you query the table:

```text
Query
  ↓
Delta Log
  ↓
Which files are valid?
  ↓
Read only valid files
```

That's why you **don't see duplicate old + new records** in the current table result.

---

# 5. What is a Tombstone?

The lecture uses the term **tombstone**.

Very simply:

> **Tombstone = a marker that says an old data file is no longer part of the current table state.**

Think:

```text
file1.parquet
      ↓
   Tombstone
      ↓
"Don't read this file for the current table."
```

The old file isn't necessarily physically deleted immediately; the important point here is that Delta knows it is no longer active.

---

# 6. Complete UPDATE flow

This is the main diagram you should remember:

```text
                 UPDATE sale_id = 1
                         │
                         ↓
              Find file containing row
                         │
                         ↓
                  Rewrite the file
                         │
                         ↓
                 Create new file
                         │
                         ↓
                  Update Delta Log
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
      Old file marked           New file valid
      as expired
             │                       │
             └───────────┬───────────┘
                         ↓
                    Query table
                         ↓
                Read valid files only
```

---

# 7. Why is Delta Log so important?

Without the Delta log, Databricks wouldn't have the same transaction/state information needed to know which Parquet files represent the current table.

So:

```text
Parquet
   =
Actual data

Delta Log
   =
"How should I interpret these files?"
```

### Easy analogy

Imagine a library:

```text
Books = Parquet files

Library catalog = Delta Log
```

The catalog tells you:

> Which books are currently available/valid.

Similarly, the Delta log tells Databricks which data files belong to the current table state.

---

# 8. Data Engineering Example

Imagine a **Sales table**:

```text
sale_id | customer | amount
--------|----------|-------
1       | A        | 500
2       | B        | 700
3       | C        | 900
```

Your business says:

> "Sale 1 amount was corrected from 500 to 550."

You run:

```sql
UPDATE sales
SET amount = 550
WHERE sale_id = 1;
```

Conceptually:

```text
Old Parquet file
       ↓
contains amount = 500
       ↓
rewrite
       ↓
New Parquet file
       ↓
amount = 550
```

Delta log records the file change, so when your downstream dashboard queries `sales`, it gets:

```text
1 | A | 550
2 | B | 700
3 | C | 900
```

It doesn't simply return both `500` and `550`.

---

# 9. Optimization connection

This is where your new **Optimization Techniques** chapter starts becoming important.

Delta Lake has mechanisms for managing and optimizing how data files are read and changed.

The lecture briefly mentions **Deletion Vectors** as a newer optimization that you'll cover later.

For now, don't go deep into it.

Just remember:

> **Traditional mental model:** an update can involve rewriting the affected Parquet file, while the Delta log keeps track of the current valid files.

---

# ⭐ summary

Think of Delta Lake like this:

```text
            DELTA TABLE
                 │
        ┌────────┴────────┐
        ↓                 ↓
   Parquet files      Delta Log
   (actual data)      (file tracking)
```

When you **INSERT**:

```text
New records
   ↓
New Parquet file
   ↓
Delta Log updated
```

When you **UPDATE**:

```text
Existing record
   ↓
Affected file rewritten
   ↓
New Parquet file
   ↓
Delta Log updated
   ↓
Old file no longer read for current table
```

### One-line interview answer

> **A Delta table stores data in Parquet files and uses the Delta transaction log to track table state and determine which files should be read for the current version of the table.**
