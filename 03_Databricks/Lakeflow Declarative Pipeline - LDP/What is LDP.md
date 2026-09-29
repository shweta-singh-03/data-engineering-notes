# Lakeflow Declarative Pipelines (LDP)

## 1. What is Lakeflow Declarative Pipelines?

> **Lakeflow Declarative Pipelines is a declarative framework for building batch and streaming data pipelines using Python and SQL.**

The three key words are:

```text
Declarative
Batch + Streaming
Python + SQL
```

---

# 2. What does "Declarative" mean? ⭐⭐⭐

This is the **most important concept** in this lecture.

### Declarative = tell the system **WHAT you want**

You describe:

> "I want this data transformation / this resulting table."

You don't focus on manually controlling every execution step.

### Simple example

Suppose you want:

```text
Orders
  ↓
Filter cancelled orders
  ↓
Clean data
  ↓
Final table
```

In a declarative approach, you primarily define the desired data logic.

```text
YOU:
"I want this final transformed dataset."

        ↓

LDP:
"Okay, I'll manage the pipeline execution."
```

### Compare with procedural thinking

**Procedural:**

```text
1. Read data
2. Run transformation
3. Write result
4. Run next task
5. Manage dependencies
6. Handle execution
```

**Declarative:**

```text
"I want this dataset to exist
with these transformations."
```

### Memory trick

> **Imperative/procedural → HOW**
> **Declarative → WHAT**

---

# 3. Why is the declarative approach useful?

It lets the Data Engineer focus more on:

```text
What data should be produced?
What transformations should happen?
What should the final tables look like?
```

rather than manually managing every execution detail.

The framework handles much of the pipeline orchestration/execution behavior behind the scenes.

---

# 4. Batch AND Streaming ⭐⭐⭐

LDP is intended for both:

```text
Batch pipelines
       +
Streaming pipelines
```

### Batch

Data arrives periodically:

```text
Every hour
Every day
Every run
```

Example:

```text
SQL/Files
   ↓
Batch pipeline
   ↓
Delta table
```

### Streaming

Data continuously arrives:

```text
Events → continuously → pipeline
```

The lecture specifically highlights support for both batch and streaming as an important aspect of LDP.

### Memory

```text
LDP
├── Batch
└── Streaming
```

---

# 5. Python and SQL

You don't need to learn a completely new programming language.

The lecture's key point is that LDP pipelines can be built using:

```text
Python
SQL
```

And the Python side uses the familiar Spark/PySpark programming model.

So your existing PySpark knowledge remains useful.

```text
You already know:

DataFrame
filter()
select()
join()
withColumn()
groupBy()
etc.

        ↓

You can use this knowledge in LDP.
```

---

# 6. LDP vs SDP terminology

The lecture introduces two terms:

```text
LDP
→ Lakeflow Declarative Pipelines
→ Databricks context

SDP
→ Spark Declarative Pipelines
→ open-source Spark context
```

For your notes:

> **LDP is the Databricks terminology; the lecture also refers to Spark Declarative Pipelines (SDP) in the open-source Spark context.**

Don't get confused if you see both abbreviations.

---

# 7. Why is LDP important?

The lecture presents LDP as a framework for modern pipeline development because it brings together:

```text
Declarative pipeline development
        +
Batch processing
        +
Streaming processing
        +
Python
        +
SQL
```

So you can think:

```text
             LDP
              │
      ┌───────┼───────┐
      │       │       │
    Batch  Streaming Python/SQL
```

---

# 8. What happens to PySpark?

Your existing PySpark knowledge is still useful.

For example, you already know:

```python
df.filter(...)
df.select(...)
df.withColumn(...)
df.join(...)
```

The lecture's point is that you don't suddenly have to abandon this knowledge and learn an entirely different transformation language.

So:

```text
Existing Spark/PySpark knowledge
            ↓
Lakeflow Declarative Pipelines
```

---

# 9. High-level architecture

Think of LDP like this:

```text
             Source
          /          \
       Batch       Streaming
          \          /
           \        /
            ▼      ▼
       Lakeflow Declarative
             Pipeline
                 │
          Transformations
          Python / SQL
                 │
                 ▼
           Data Tables
```

---

# 10. What this lecture does NOT cover yet

This is only the **10,000-foot overview**, so don't add detailed implementation notes yet.

The lecture has not yet covered in detail:

```text
❌ Pipeline syntax
❌ Pipeline configuration
❌ Streaming implementation
❌ Data quality expectations
❌ Dependencies
❌ Materialized views
❌ Streaming tables
❌ Pipeline execution details
```

Those should come from the upcoming lectures.

---

# ⭐ Notes-ready Cheat Sheet

```text
LAKEFLOW DECLARATIVE PIPELINES (LDP)

Definition:
→ Declarative framework for building
  batch + streaming data pipelines.

Languages:
→ Python
→ SQL

Declarative means:
→ Define WHAT data/pipeline you want
→ Framework handles much of the execution/orchestration.

Supports:
→ Batch
→ Streaming

Terminology:
→ LDP = Lakeflow Declarative Pipelines
→ SDP = Spark Declarative Pipelines
  (open-source Spark terminology mentioned in lecture)

Python:
→ Uses familiar Spark/PySpark transformation concepts.

Mental model:

              LDP
               │
       ┌───────┴───────┐
       │               │
     Batch          Streaming
       │               │
       └───────┬───────┘
               ↓
        Python / SQL
               ↓
          Data Products
```

### ⭐ Most important 3 points

> **1. LDP is a declarative framework.**
> **2. It supports both batch and streaming pipelines.**
> **3. It uses Python and SQL, so your existing Spark/PySpark knowledge remains relevant.**

### ⭐ One-line interview answer

> **Lakeflow Declarative Pipelines is a Databricks declarative framework for building batch and streaming data pipelines using Python and SQL, where you define the desired data processing logic rather than manually managing every execution step.**

