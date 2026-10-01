# Delta Lake Optimization — Deletion Vectors

## 1. What problem are Deletion Vectors solving?

Previously, we learned:

```text
UPDATE 1 row
     ↓
Rewrite entire Parquet file
```

Suppose a Parquet file contains **100 MB of data**, but you only change **1 record**.

Without Deletion Vectors:

```text
100 MB file
    ↓
Rewrite entire file
```

This can be expensive in terms of **time and storage**.

---

# 2. What is a Deletion Vector?

A **Deletion Vector (DV)** is a piece of metadata that tells Delta Lake:

> **"These particular rows in this Parquet file should no longer be considered active."**

Instead of rewriting the whole Parquet file, Delta can mark the affected row using the deletion vector and store the updated record separately.

Think of it like a **to-do/ignore list for rows**.

```text
Original Parquet file

ID 1
ID 2
ID 3
ID 4
ID 5
```

Suppose ID 1 is updated.

With DV:

```text
Original Parquet file
ID 1  ← marked in DV
ID 2
ID 3
ID 4
ID 5

Deletion Vector
→ ID 1 is no longer read from this file

New small Parquet file
→ updated ID 1
```

The lecture demonstrates this exact idea: the original file remains, the changed record is written separately, and the deletion vector records that the original record should be ignored.

---

# 3. Without DV vs With DV

### Without Deletion Vector

```text
UPDATE 1 row
      ↓
Rewrite entire Parquet file
      ↓
New large file
```

### With Deletion Vector

```text
UPDATE 1 row
      ↓
Mark old row in Deletion Vector
      ↓
Write updated row separately
      ↓
No need to rewrite entire large file
```

### Main benefit

> **Less unnecessary rewriting → less work and potentially lower storage/time cost.**

---

# 4. What happens when we READ the table?

Suppose:

```text
Original file:
ID 1
ID 2
ID 3
ID 4

Deletion Vector:
ID 1 = marked
```

When Delta reads the table:

```text
Parquet file
      +
Deletion Vector
      ↓
Ignore marked row
      ↓
Read valid rows
```

And then it also reads the new file containing the updated version of ID 1.

So the user sees the **correct current data**, not duplicate old + new records.

---

# 5. A new problem: Small files

Now think about this:

```text
UPDATE 1 row → small file
UPDATE 1 row → small file
UPDATE 1 row → small file
UPDATE 1 row → small file
...
```

You could end up with many small Parquet files.

The lecture points out this **small-file problem** and introduces file merging as the next optimization.

```text
Small files
   ↓
Merge/compact
   ↓
Larger efficient file
```

For this lecture, just remember **DV solves the unnecessary rewrite problem**, while **file merging addresses the small-file problem**.

---

# 6. What happens to the Delta Log?

Delta Lake still uses the transaction log to track what should be read.

Conceptually:

```text
Delta Log
   ↓
REMOVE old file/row state
ADD new data
   ↓
Current table state
```

The lecture's example shows the log recording the removal of the old file and addition of the new/updated data.

---

# 7. Real Data Engineering Example

Imagine your **sales Delta table** has:

```text
sales.parquet
→ 10 million records
```

You update just one sale:

```sql
UPDATE sales
SET amount = 5000
WHERE sale_id = 6;
```

### Old approach

```text
10 million records
        ↓
Rewrite affected large Parquet file
```

### With Deletion Vector

```text
Original Parquet
      ↓
Mark sale_id = 6 in DV
      ↓
Write updated sale_id = 6
to a new small Parquet file
```

This avoids rewriting all the unrelated records. The lecture demonstrates this with a table where the updated record is placed in a separate small Parquet file and the deletion vector identifies the changed row.

---

# ⭐ What to remember

```text
OLD APPROACH
Update 1 row
   ↓
Rewrite whole Parquet file

WITH DELETION VECTOR
Update 1 row
   ↓
Mark old row using DV
   ↓
Write updated row separately
```

### Interview one-liner

> **Deletion Vectors optimize updates and deletes in Delta Lake by recording affected rows separately, reducing the need to rewrite entire Parquet files.**

### Memory trick

> **Deletion Vector = "Don't rewrite the whole file; just mark the affected rows and handle the changed data separately."**
