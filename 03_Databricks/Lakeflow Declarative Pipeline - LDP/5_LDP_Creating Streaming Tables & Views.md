# LDP – Creating Streaming Tables & Streaming Views

# 1. First: What are we building?

We already know:

```text
LDP Pipeline
      ↓
   Flow(s)
      ↓
Streaming Table / View / Materialized View
```

In this lecture, we learn **how to actually create a Streaming Table and a Streaming View using Python**.

The source used in the example is a **Delta table**.

```text
Delta Table
   ↓
LDP Pipeline
   ↓
Streaming Table
```

A Delta table can be used as both a **batch source and a streaming source**.

---

# 2. Where do we write the code?

Inside the LDP pipeline:

```text
LDP basics/
│
├── transformations/
│      ├── ingest.py
│      ├── transform.py
│      └── serve.py
│
└── explorations/
```

### `transformations/`

This contains the **actual pipeline code**.

Python and SQL files can both be used.

You can have multiple files instead of putting the entire pipeline into one giant file.

### `explorations/`

This is just your **scratchpad**.

You can test queries and inspect results here.

It is **not part of the pipeline**.

---

# 3. Creating a Streaming Table

Let's understand the normal Spark approach first.

Suppose our source is:

```text
catalog.schema.source_table
```

With normal Structured Streaming, you would conceptually do:

```python
df = (
    spark.readStream
         .table("catalog.schema.source_table")
)
```

Then you perform transformations:

```python
df = df.withColumn(
    "ingest_timestamp",
    current_timestamp()
)
```

Normally, you'd then need things like:

```text
writeStream
checkpoint
output mode
trigger
query management
etc.
```

But in LDP, **you don't manually manage all that overhead**.

Instead, you basically say:

> "This is the data I want and these are my transformations."

Then return the DataFrame.

---

# 4. LDP's Python package

We import:

```python
from pyspark import pipelines as dp
```

Here:

```text
pipelines → LDP framework
dp        → short name/alias
```

So `dp` is what we use to tell LDP what kind of pipeline object we want.

---

# 5. The basic Streaming Table pattern

The basic idea from the lecture is:

```python
from pyspark import pipelines as dp
from pyspark.sql.functions import *

@dp.table
def ingest_data():

    df = (
        spark.readStream
             .table("catalog.schema.source_table")
    )

    df = df.withColumn(
        "ingest_timestamp",
        current_timestamp()
    )

    return df
```

Let's break this down.

---

## `def ingest_data()`

This is just a normal Python function.

It describes:

> "What data should this table contain?"

---

## `spark.readStream`

This tells Spark:

> **"Read this as streaming data."**

So:

```python
spark.readStream.table(...)
```

means that the source is being read using **streaming semantics**.

---

## `withColumn()`

This is your normal PySpark transformation.

Example:

```python
df = df.withColumn(
    "ingest_timestamp",
    current_timestamp()
)
```

It adds a column containing the current processing timestamp.

You already know `withColumn()` from your PySpark learning.

---

# 6. The most important part: `@dp.table`

This:

```python
@dp.table
```

is a **Python decorator**.

Think of a decorator as a label that tells LDP:

> **"Hey Databricks, this function should become a pipeline table."**

Without it:

```python
def ingest_data():
```

it's simply a Python function.

With it:

```python
@dp.table
def ingest_data():
```

LDP understands that this function defines a **table in the pipeline**.

The framework then takes care of much of the execution overhead for you.

---

# 7. Why don't we use `writeStream`?

This is one of the BIGGEST things to understand.

### Normal Spark Structured Streaming

You typically have:

```text
readStream
   ↓
transform
   ↓
writeStream
   ↓
checkpoint
   ↓
manage streaming query
```

### LDP

You mainly define:

```text
readStream
   ↓
transform
   ↓
return df
```

Databricks handles much of the pipeline execution/management overhead such as checkpoints and related processing infrastructure.

### Simple thought

> **Normal Spark → you manage more of the streaming machinery.**

> **LDP → you declare what you want, and Databricks manages much of the machinery.**

---

# 8. What is a DAG?

Before running the pipeline, LDP can show a **DAG**.

DAG = **Directed Acyclic Graph**

Don't get scared by the name.

It simply shows:

> **Which thing depends on which other thing?**

Example:

```text
Source Table
     ↓
Streaming Table
     ↓
Streaming View
     ↓
Final Streaming Table
```

That is your dependency graph.

You don't have to manually tell LDP:

> "Run A first, then B, then C."

LDP can identify dependencies from the data references in your code.

---

# 9. Auto Dependency Tracking

This is a very important LDP feature.

Suppose:

```text
Source Table
      ↓
Ingest Data
      ↓
Transform Data
      ↓
Serve Data
```

And your code says:

```python
spark.readStream.table("ingest_data")
```

LDP sees:

> "Oh, `transform_data` is using `ingest_data`."

So it automatically creates:

```text
ingest_data
     ↓
transform_data
```

Then if another function uses `transform_data`:

```text
ingest_data
     ↓
transform_data
     ↓
serve_data
```

This is called **automatic dependency tracking / auto orchestration** in the lecture.

### Simple analogy

You don't tell a teacher:

```text
First learn addition.
Then multiplication.
Then division.
```

The teacher sees that multiplication depends on understanding addition.

LDP similarly builds the dependency order from your pipeline definitions.

---

# 10. Creating a Streaming View

Now we already have:

```text
Streaming Table
```

Let's say we don't want to save another table for an intermediate transformation.

We just want a **temporary/intermediate view**.

Then we create a streaming view.

Example pattern:

```python
from pyspark import pipelines as dp
from pyspark.sql.functions import *

@dp.temporary_view
def transform_data():

    df = (
        spark.readStream
             .table("ingest_data")
    )

    df = df.withColumn(
        "transformed",
        lit("transformed")
    )

    return df
```

The important part is:

```python
@dp.temporary_view
```

This tells LDP:

> **"Create this as a view, not as a stored table."**

---

# 11. How does LDP know whether it is streaming or normal view?

This is based on **how you read the data**.

### Streaming view

```python
spark.readStream.table(...)
```

→ streaming processing

### Normal/batch view

```python
spark.read.table(...)
```

→ batch processing

The lecture's rule is:

```text
readStream → Streaming View

read        → Normal View
```

---

# 12. Why use a Streaming View?

Suppose:

```text
Source
  ↓
Streaming Table
  ↓
Clean data
  ↓
Calculate something
  ↓
Final Streaming Table
```

Maybe the **clean data step doesn't need to be permanently stored**.

Then:

```text
Streaming Table
       ↓
Streaming View
       ↓
Final Streaming Table
```

The view acts as an **intermediate step**.

Think of it as a temporary workbench.

---

# 13. Function name becomes the object name

Suppose you write:

```python
@dp.temporary_view
def transform_data():
    ...
```

The function name:

```text
transform_data
```

can become the object name.

So:

```text
function name
      ↓
transform_data
      ↓
view name
```

The lecture also mentions that a custom name can be supplied through decorator configuration when needed.

For learning purposes, it's easiest to **keep the function name and table/view name meaningful and aligned**.

---

# 14. Building the complete streaming pipeline

Now we can create this:

```text
            SOURCE
       Delta Source Table
              │
              ↓
      ┌─────────────────┐
      │ ingest_data     │
      │ Streaming Table │
      └────────┬────────┘
               ↓
      ┌─────────────────┐
      │ transform_data  │
      │ Streaming View  │
      └────────┬────────┘
               ↓
      ┌─────────────────┐
      │ served_data     │
      │ Streaming Table │
      └─────────────────┘
```

The key point:

> **LDP automatically understands the dependency between these objects.**

You didn't manually create a workflow saying:

```text
Run 1
then Run 2
then Run 3
```

The framework identifies the relationships from the code.

---

# 15. Streaming Table → Streaming View → Streaming Table

This is the exact pattern demonstrated in the lecture.

```text
Delta Source
     ↓
Streaming Table
     ↓
Streaming View
     ↓
Final Streaming Table
```

And all of this can be incrementally processed.

---

# 16. Testing incremental processing

This is a VERY important practical demonstration.

Initially source contains:

```text
1
2
3
```

Pipeline runs:

```text
1
2
3
 ↓
processed
```

Now add:

```text
4
5
6
```

Run the pipeline again.

LDP processes the **new records** rather than repeatedly processing all six records as new input.

```text
First run:
1 2 3 → processed

Second run:
4 5 6 → processed
```

The lecture verifies that the final table contains all six records after the second run.

This demonstrates the **incremental/streaming behavior** of the pipeline.

---

# 17. Very Important Rule from this lecture

The instructor emphasizes:

> **A Streaming Table must read from a streaming source.**

So:

```text
Streaming Table
      ↓
needs
      ↓
Streaming Source
```

For example:

```python
spark.readStream.table(...)
```

works for this pattern.

But if you try to feed it a normal batch view/source instead of a streaming source, the demonstrated pipeline would fail.

### Easy memory trick

```text
STREAMING TABLE
       ↓
STREAMING SOURCE
```

That's the rule to remember from this lecture.

---

# 18. What does `dry run` do?

Before actually running the pipeline, you can do a **dry run**.

Think:

> **"Show me what the pipeline would look like without actually processing the data."**

It is useful for checking:

```text
Source
  ↓
Flow
  ↓
View
  ↓
Target
```

and inspecting the DAG/dependencies before execution.

---

# 19. Normal Spark vs LDP

This is probably the most important conceptual comparison from the whole lecture.

| Normal Spark Streaming                | LDP                                                     |
| ------------------------------------- | ------------------------------------------------------- |
| `readStream`                          | `readStream`                                            |
| Transformations                       | Transformations                                         |
| `writeStream`                         | Usually not manually written in the pipeline definition |
| Checkpoint management                 | Managed by framework                                    |
| Streaming query management            | Managed by framework                                    |
| Manual workflow/dependency management | LDP can infer dependencies                              |
| More implementation code              | More declarative                                        |

The big difference is **not that PySpark disappears**.

You still write your transformations.

The difference is:

> **You describe what the pipeline should produce, while LDP handles much of the execution/orchestration infrastructure.**

---

# ⭐ CRUX — What you REALLY need to remember

Forget the 400 lines of transcript. Remember this:

### 1. LDP starts with a source

```text
Delta Table
   ↓
LDP
```

A Delta table can be a batch or streaming source.

### 2. For a Streaming Table

Use:

```python
spark.readStream
```

and:

```python
@dp.table
```

```text
readStream
    ↓
transform
    ↓
return df
    ↓
@dp.table
    ↓
Streaming Table
```

### 3. `@dp.table` is a decorator

It tells LDP:

> **"Treat this function as a table definition."**

### 4. You don't manually manage all the streaming machinery

LDP manages much of the:

```text
checkpointing
execution
pipeline management
```

instead of you writing all of that yourself.

### 5. For a Streaming View

Use:

```python
@dp.temporary_view
```

and read using:

```python
spark.readStream
```

```text
readStream
    ↓
transform
    ↓
@dp.temporary_view
    ↓
Streaming View
```

### 6. LDP automatically understands dependencies

```text
Table A
   ↓
View B
   ↓
Table C
```

You don't manually orchestrate every step.

That's **auto dependency tracking / auto orchestration**.

### 7. The entire lecture in ONE picture

```text
                 LDP PIPELINE
                      │
                      ↓
              Delta Source Table
                      │
                readStream
                      ↓
              @dp.table
                      ↓
            STREAMING TABLE
                      │
                readStream
                      ↓
          @dp.temporary_view
                      ↓
             STREAMING VIEW
                      │
                readStream
                      ↓
              @dp.table
                      ↓
          FINAL STREAMING TABLE
```

And LDP figures out:

```text
dependencies
     +
execution order
     +
incremental processing
```

### 🧠 One-line memory trick

> **`@dp.table` = make a table, `@dp.temporary_view` = make a view, `readStream` = streaming input, and LDP connects and manages the pipeline for you.**
