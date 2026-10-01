# Delta Lake — Versioning, Time Travel, Restore & Checkpoints

## 1. What is Time Travel?

Imagine you have a Delta table and you perform several operations:

```text
Create table
   ↓
Insert data
   ↓
Insert more data
   ↓
Update data
   ↓
Delete data
```

Normally, you would expect to see only the **latest state** of the table.

But Delta Lake keeps track of the table's previous states.

That allows you to ask:

> **"What did my table look like before?"**

This is called **Time Travel**.

### Simple definition

> **Time Travel = ability to read an older version of a Delta table.**

The idea is similar to **Ctrl + Z / rollback**, although time travel itself is primarily about accessing an earlier version.

---

# 2. Versioning — the foundation of Time Travel

To understand Time Travel, first understand **versions**.

Every time you make a change to a Delta table, Delta creates a **new version**.

For example:

```text
Version 0 → CREATE TABLE
Version 1 → INSERT
Version 2 → INSERT
Version 3 → UPDATE
Version 4 → DELETE
```

So the table is not just:

> "one current table"

It has a sequence of states:

```text
V0 → V1 → V2 → V3 → V4
```

The lecture shows exactly this sequence using the example table.

### Important

> **A version represents the state of the Delta table after a particular operation.**

---

# 3. How do we see the versions?

Use:

```sql
DESCRIBE HISTORY catalog.schema.table;
```

For example:

```sql
DESCRIBE HISTORY my_catalog.sales;
```

This gives you the history of the table.

You can see information such as:

```text
Version
Timestamp
Operation
User
```

Example:

```text
Version | Operation
--------|----------------
0       | CREATE TABLE
1       | WRITE
2       | WRITE
3       | UPDATE
4       | DELETE
```

The lecture also notes that the history contains information such as timestamps and the user associated with the operation.

### Easy memory trick

> **DESCRIBE HISTORY = "What happened to my table?"**

---

# 4. Current version vs Older version

Normally:

```sql
SELECT * FROM my_catalog.sales;
```

you get the **latest/current state** of the table.

Suppose:

```text
Version 3
sale_id = 1
sale_id = 2
sale_id = 3
```

Then at Version 4:

```text
sale_id = 2 is deleted
```

Current table:

```text
1
3
```

But Version 3 still represents:

```text
1
2
3
```

Because Delta knows how the table looked at Version 3.

---

# 5. Reading an old version — Time Travel

You can tell Delta:

> "Show me the table as it existed at Version 3."

Use:

```sql
SELECT *
FROM my_catalog.sales
VERSION AS OF 3;
```

This is **Time Travel**.

```text
Current table
     ↓
VERSION AS OF 3
     ↓
Read the table as it existed at Version 3
```

So if `sale_id = 2` was deleted in Version 4:

```text
Current Version (4)
→ sale_id 2 ❌

Version 3
→ sale_id 2 ✅
```

The lecture demonstrates this by reading the table at Version 3 and seeing the previously deleted record again.

---

# 6. VERY IMPORTANT: Time Travel does NOT change the table

This is a key distinction.

When you run:

```sql
SELECT *
FROM sales
VERSION AS OF 3;
```

you are only **reading an old version**.

You have NOT changed the current table.

Think:

```text
Version 4 = current table

        ↓
VERSION AS OF 3

        ↓
"Let me LOOK at Version 3"
```

The current table is still Version 4.

---

# 7. What if I actually want to bring the old version back?

This is where **RESTORE** comes in.

Suppose:

```text
Version 3 → data is correct
Version 4 → accidentally deleted data
```

You don't just want to look at Version 3.

You want the current table to become like Version 3 again.

Use:

```sql
RESTORE TABLE my_catalog.sales
TO VERSION AS OF 3;
```

### Simple difference

```text
TIME TRAVEL
→ "Show me the old data"

RESTORE
→ "Make that old version the current table state"
```

This is probably the most important distinction in the lecture.

---

# 8. RESTORE does NOT erase history

This is another very important point.

Suppose you have:

```text
V0 → CREATE
V1 → INSERT
V2 → INSERT
V3 → UPDATE
V4 → DELETE
```

Now you restore Version 3.

You might think:

```text
V0 → V1 → V2 → V3
```

and Version 4 disappears.

**No.**

Instead, Delta creates another version:

```text
V0 → V1 → V2 → V3 → V4 → V5
                                  ↑
                               RESTORE
```

So:

> **RESTORE creates a new version that brings the table back to an earlier state.**

It doesn't erase the previous versions.

The lecture demonstrates this by showing that after restoring Version 3, a new Version 5 appears in the history with `RESTORE` as the operation.

---

# 9. What happens underneath during RESTORE?

Remember your previous lesson:

```text
Delta Table
├── _delta_log
└── Parquet files
```

When you perform a restore, Delta doesn't need to recreate all the data from scratch.

Conceptually, it updates the Delta log so that the table's current state points back to the appropriate data files.

For example:

```text
Before restore:

Current state
   ↓
File A + File B


RESTORE to Version 3
   ↓
Delta Log updated
   ↓
Current state now points to
the files representing Version 3
```

The lecture demonstrates this as another log entry containing the inverse `remove/add` changes needed to make the older state current again.

---

# 10. Why is this powerful for Data Engineers?

Imagine a production table:

```text
customer_orders
```

Someone accidentally deletes thousands of records.

Without Delta's versioning:

```text
"Oh no 😭"
```

With Delta:

```text
DESCRIBE HISTORY
       ↓
Find correct version
       ↓
VERSION AS OF
       ↓
Check old data
       ↓
RESTORE if required
```

So Delta gives you a kind of **data safety net**.

---

# 11. Time Travel vs Restore

Keep this table in your notes:

| Feature              | What it does                             |
| -------------------- | ---------------------------------------- |
| **Versioning**       | Keeps track of different table states    |
| **Time Travel**      | Reads an older version                   |
| **Restore**          | Makes an older version the current table |
| **DESCRIBE HISTORY** | Shows what operations happened           |

### Easy analogy

Imagine Google Docs:

```text
Version History
      ↓
See old version
      ↓
Time Travel
```

And:

```text
Restore old version
      ↓
Make old version current
```

---

# 12. What is a Checkpoint?

Now comes the last concept from this lecture.

Imagine a table has many Delta log entries:

```text
000000.json
000001.json
000002.json
000003.json
000004.json
...
```

If Databricks had to read every single log file every time, that could become inefficient.

So Delta periodically creates a **checkpoint** containing a summarized representation of the table state.

The lecture calls this the **last checkpoint** and explains that it helps narrow the amount of log information that needs to be read repeatedly.

### Simple analogy

Imagine reading a huge book.

Instead of starting from page 1 every time:

```text
Page 1
Page 2
Page 3
...
Page 500
```

you have a bookmark saying:

> "Here's the latest known state."

That's roughly the idea of a checkpoint.

```text
Delta Logs
   ↓
Checkpoint
   ↓
Recent/current table state information
```

---

# 13. Complete picture

Now connect everything you've learned:

```text
                 DELTA TABLE
                      │
            ┌─────────┴─────────┐
            │                   │
       Parquet files         Delta Log
       actual data          table history
                                │
                    ┌───────────┴───────────┐
                    ↓                       ↓
               Versions                 Checkpoint
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
     Time Travel           Restore
          │                   │
   Read old version    Make old version
                       current again
```

---

# 14. Real DE scenario

Suppose you're maintaining a **sales pipeline**.

```text
SQL Server
   ↓
ADF / Databricks
   ↓
Delta Sales Table
```

Monday:

```text
V10 → 1,00,000 records
```

Tuesday:

```text
V11 → INSERT new sales
```

Wednesday:

```text
V12 → UPDATE sales
```

Thursday:

```text
V13 → Someone accidentally deletes records
```

You can investigate:

```sql
DESCRIBE HISTORY sales;
```

Then check the previous state:

```sql
SELECT *
FROM sales
VERSION AS OF 12;
```

If Version 12 is correct and you need to make it current again:

```sql
RESTORE TABLE sales
TO VERSION AS OF 12;
```

Now Delta creates:

```text
V14 → RESTORE
```

The history remains available.

---

# ⭐ What you should remember for interviews

### Versioning

> Delta Lake maintains different versions of a table as changes are made.

### Time Travel

> Time Travel allows us to query a previous version of a Delta table.

### `DESCRIBE HISTORY`

> Used to see the table's version history and operations.

### `VERSION AS OF`

> Used to read data from a specific historical version.

### RESTORE

> Restores an earlier version as the current table state and creates a new version.

### Checkpoint

> A checkpoint stores a summarized table state so Delta does not need to repeatedly process the entire transaction log from the beginning.

---

## 🧠 Super-easy memory trick

```text
HISTORY
"What happened?"

VERSION AS OF
"What did my table look like?"

RESTORE
"Make that old state current."

CHECKPOINT
"Remember the state so we don't start from zero."
```

This entire chapter is basically teaching you:

> **Delta doesn't just store your data — it keeps track of how the table changed over time. That's what enables Time Travel and Restore.**
