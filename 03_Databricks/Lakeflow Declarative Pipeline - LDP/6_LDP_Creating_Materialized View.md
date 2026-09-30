# LDP – Creating a Materialized View

## 1. Materialized View = Batch Table

Think of a Materialized View as a **batch-oriented table**.

The important point from the lecture is:

> **A Materialized View can work with both batch sources and streaming sources.**

```text
             Materialized View
                /          \
               ↓            ↓
        Batch Source    Streaming Source
```

But a Streaming Table is more restrictive:

```text
Streaming Table
       ↓
Streaming Source
```

The lecture's simple comparison is:

|                            | Streaming Table     | Materialized View |
| -------------------------- | ------------------- | ----------------- |
| Processing style           | Streaming           | Batch             |
| Can read batch source?     | No, in this pattern | Yes               |
| Can read streaming source? | Yes                 | Yes               |
| Incremental processing     | Yes                 | Yes               |
| Stores result              | Yes                 | Yes               |

So remember:

> **Materialized View is more flexible than a Streaming Table because it can read either batch or streaming data.**

---

# 2. How do we create a Materialized View?

Instead of:

```python
spark.readStream.table(...)
```

we use:

```python
spark.read.table(...)
```

Why?

Because we are reading the source using **batch semantics**.

Example:

```python
from pyspark import pipelines as dp

@dp.materialized_view
def aggregated_table():

    df = spark.read.table("served_data")

    df = (
        df.groupBy("id")
          .count()
    )

    return df
```

### Important parts

```python
spark.read.table(...)
```

→ Read as **batch**

```python
@dp.materialized_view
```

→ Tell LDP:

> "Make this function a Materialized View."

The lecture demonstrates exactly this pattern with a `groupBy()` aggregation.

---

# 3. Why use a Materialized View?

Suppose your data looks like:

```text
id
--
1
2
3
1
2
3
```

You want:

```sql
GROUP BY id
```

Result:

```text
id    count
------------
1       2
2       2
3       2
```

This type of **aggregation** is a good example for a Materialized View.

---

# 4. The interesting part: What happens when you run it again?

Suppose the first run has:

```text
1
2
3
4
5
6
```

Materialized View produces:

```text
1 → 2
2 → 2
3 → 2
```

Now you run the pipeline again.

There is **no new source data**.

What happens?

The Materialized View may still show that it **read/processed the existing data for the query**, because it needs to evaluate/refresh the materialized result.

But it does **not mean six new records were inserted again**.

Think:

```text
Existing source data
      ↓
Materialized View refresh/query
      ↓
Same result
      ↓
No duplicate six rows added
```

The lecture uses this to show that the Materialized View's displayed output/read count and the amount of newly written data are not the same thing.

---

# 5. Now add NEW data

This is where the difference becomes very clear.

Initially:

```text
Source
1
2
3
4
5
6
```

Then we add:

```text
1
2
3
```

So the source now has:

```text
1
2
3
4
5
6
1
2
3
```

### Streaming Table

The Streaming Table is append-oriented.

So it simply adds:

```text
1
2
3
```

Result:

```text
9 records
```

It doesn't suddenly group the data or remove duplicates.

---

# 6. What does the Materialized View do?

The Materialized View receives/uses the newly available data, but because it is maintaining a **materialized query result**, its aggregation reflects the previous data as well.

So instead of getting:

```text
1 → 1
2 → 1
3 → 1
```

from only the new batch, the final aggregation becomes:

```text
1 → 3
2 → 3
3 → 3
```

because the complete data now contains each of those IDs three times.

Conceptually:

```text
Previous result/state
        +
New incoming data
        ↓
Updated aggregation
```

This is the important behavior demonstrated in the lecture.

---

# 7. Why doesn't the Materialized View create duplicate rows?

Because it is **materializing the result of the query**.

Think about your query:

```sql
SELECT id, COUNT(*)
FROM served_data
GROUP BY id
```

The output isn't the individual source records.

The output is:

```text
id → count
```

So when the source changes, the Materialized View updates the **result of the aggregation**.

It does NOT simply do:

```text
old output
+
new output
```

as an append-only table would.

---

# 8. Streaming Table vs Materialized View — THE IMPORTANT EXAMPLE

Suppose:

### Initial data

```text
1
2
3
1
2
3
```

### Streaming Table

Stores:

```text
1
2
3
1
2
3
```

It is basically saying:

> "New records arrived → append/process them."

---

### Materialized View

Query:

```sql
GROUP BY id
```

Result:

```text
1 → 2
2 → 2
3 → 2
```

Now add:

```text
1
2
3
```

Streaming Table:

```text
1
2
3
1
2
3
1
2
3
```

Materialized View:

```text
1 → 3
2 → 3
3 → 3
```

### That's the key difference.

```text
STREAMING TABLE
New data
   ↓
Append/process it


MATERIALIZED VIEW
New data
   ↓
Refresh/materialize query result
   ↓
Correct updated aggregation
```

---

# 9. Materialized View can read a Streaming Table

This is another important point from the example.

The pipeline is:

```text
Delta Source
     ↓
Streaming Table
     ↓
Materialized View
```

The Materialized View is using:

```python
spark.read.table("served_data")
```

So although the **upstream table was produced by streaming**, the Materialized View itself is doing **batch-style reading/query processing**.

That's why the Materialized View can work on top of a Streaming Table.

---

# 10. Why multiple Python files still work as one pipeline

The lecture also demonstrates something useful.

You can have:

```text
transformations/
│
├── ingest.py
├── transform.py
├── serve.py
└── materialized_view.py
```

You don't need to put everything in one Python file.

Because they're inside the pipeline's source-code folder, LDP treats them as part of the same pipeline and can automatically discover dependencies between the objects.

So:

```text
materialized_view.py
        ↓
reads served_data
        ↓
LDP knows:
"this depends on served_data"
```

---

# 11. Complete example from the lectures

This is the pipeline you've built so far:

```text
                    LDP PIPELINE
                         │
                         ↓
                  Delta Source
                         │
                    readStream
                         ↓
                ┌────────────────┐
                │ Streaming Table│
                │   ingest_data  │
                └───────┬────────┘
                        ↓
                 Streaming View
                ┌───────┴────────┐
                │ transform_data │
                └───────┬────────┘
                        ↓
                ┌────────────────┐
                │ Streaming Table│
                │   served_data  │
                └───────┬────────┘
                        ↓
                   spark.read
                        ↓
                ┌────────────────┐
                │ Materialized   │
                │ View           │
                │ aggregated_tbl │
                └────────────────┘
```

---

# ⭐ CRUX — What you need to remember

Don't memorize the long explanation. Remember these **5 things**:

### 1. Materialized View = Batch Table

```text
Materialized View
      ↓
Batch processing
```

But it can read from **both batch and streaming sources**.

---

### 2. Streaming Table is more restrictive

```text
Streaming Table
      ↓
Streaming source
```

---

### 3. Code difference

```python
# Streaming
spark.readStream.table(...)
```

```python
# Batch / Materialized View
spark.read.table(...)
```

And:

```python
@dp.table
```

means:

> Create a table.

```python
@dp.materialized_view
```

means:

> Create a Materialized View.

---

### 4. The most important difference

```text
Streaming Table
→ new records arrive
→ append/process them


Materialized View
→ new data arrives
→ update/refresh the query result
→ aggregation stays correct
```

---

### 5. The easiest way to remember everything

Think of a **photograph album**:

```text
Streaming Table
= Keep adding new photos to the album.

Materialized View
= Keep the latest summary of the album.
```

So:

> **Streaming Table remembers the incoming records.**

> **Materialized View maintains the result of a query over that data.**

That is the key concept this lecture is trying to teach.
