# LDP – Creating a Pipeline

## 1. What can be used as an LDP source?

The lecture uses a **Delta table** as the source.

A Delta table can be used for both:

```text
Delta Table
   ├── Batch source
   └── Streaming source
```

So remember:

> **Delta table can act as both a batch source and a streaming source.**

---

# 2. Creating an LDP Pipeline

In Databricks, when the lecture says **Pipeline**, it is referring to an **LDP pipeline** in this context.

Think:

```text
LDP Pipeline
      ↓
contains your data-processing code
      ↓
creates your tables/views
```

---

# 3. Pipeline working directory

When you create an LDP pipeline, Databricks gives you a **working directory**.

Inside it, there is a folder called:

```text
transformations/
```

This is important.

### `transformations` = pipeline source-code folder

The Python/SQL files placed inside this folder are treated as part of the pipeline.

```text
LDP basics/
│
└── transformations/
      ├── customers.py
      ├── orders.py
      └── sales.sql
```

Think of it like:

> **`transformations` = "Where I write the actual pipeline code."**

---

# 4. Can I create multiple files?

Yes.

You **do not need to put your entire pipeline in one file**.

For example:

```text
transformations/
│
├── customers.py
├── orders.py
├── products.py
└── sales.sql
```

You can create dependencies between these files.

Both **Python and SQL files** can be used.

---

# 5. What is the `explorations` folder?

This is an important distinction.

The lecture creates an `explorations` folder as a **scratchpad**.

It is **NOT part of the pipeline**.

You can use it to test queries or inspect results while developing.

```text
LDP basics/
│
├── transformations/    ← REAL PIPELINE CODE
│
└── explorations/       ← SCRATCHPAD / TESTING
```

Example:

```text
transformations/
    customers.py

explorations/
    test_queries
```

You can experiment in `explorations` without that code becoming part of the actual pipeline.

### Easy memory trick

> **Transformations = actual work**

> **Explorations = practice/testing**

---

# 6. Pipeline location

The pipeline has a **root/working folder location**.

The lecture recommends moving the pipeline folder using the Databricks UI rather than manually moving/copying it, because Databricks needs to keep the configured location updated.

For your DE understanding, the main thing to remember is:

> **LDP needs to know where the pipeline's source code lives.**

---

# 7. Where are Streaming Tables and Materialized Views created?

Remember the previous lecture:

```text
Streaming Table
Materialized View
```

These are objects produced by the pipeline.

In the pipeline configuration, you specify the:

```text
Catalog
   +
Schema
```

where these objects should be created.

Think:

```text
LDP Pipeline
     │
     └── Output location
            │
        Catalog.Schema
            │
       ┌────┴─────┐
       ↓          ↓
 Streaming     Materialized
   Table          View
```

So the pipeline configuration basically says:

> **"Create my pipeline's output objects here."**

---

# 8. Why use Catalog + Schema?

You already learned Unity Catalog.

The hierarchy is:

```text
Catalog
   ↓
Schema
   ↓
Tables / Views
```

So an LDP pipeline can be configured to create its output under a particular:

```text
catalog.schema
```

For example:

```text
my_catalog
   ↓
ldp_basics
   ↓
customers
orders
sales
```

---

# 9. Why create the schema using SQL/DDL?

The lecture recommends managing DDL through scripts rather than relying only on the UI.

Example:

```sql
CREATE SCHEMA IF NOT EXISTS my_catalog.ldp_basics;
```

The reason given is that managing it through scripts is better for deployment and avoids some UI-related issues.

For your notes:

> **Prefer managing database objects such as schemas through DDL/scripts when building deployable pipelines.**

---

# 10. Compute

The pipeline also has a **compute** configuration.

The lecture shows:

```text
Serverless
```

and mentions that job compute/all-purpose compute can also be selected depending on the setup.

For now, don't overthink this.

You already learned about Databricks compute separately.

Just remember:

> **Compute = the resources used to execute the pipeline.**

---

# 11. Other pipeline settings

The lecture briefly shows:

### Environment

Defines the pipeline environment/dependencies.

### Configuration

Used for things such as **parameterization**.

### Tags

Can be used for governance/organization.

### Notifications

Can notify people when the pipeline fails or other events occur.

These are supporting configurations, not the core LDP concept.

---

# 12. The most important architecture from this lecture

Keep this mental picture:

```text
                    LDP PIPELINE
                         │
              ┌──────────┴──────────┐
              │                     │
       transformations/       explorations/
              │                     │
        REAL PIPELINE CODE       SCRATCHPAD
              │
       ┌──────┴───────┐
       │              │
     Python           SQL
       │              │
       └──────┬───────┘
              ↓
          DATA FLOW
              ↓
       ┌──────────────┐
       │              │
 Streaming Table   Materialized View
       │              │
       └──────┬───────┘
              ↓
        Catalog.Schema
```

---

# ⭐ What you actually need to memorize

### Source

> **Delta table can be used as both batch and streaming source.**

### `transformations/`

> **Contains the Python/SQL code that belongs to the LDP pipeline.**

### `explorations/`

> **Scratchpad for testing; not part of the pipeline.**

### Pipeline

> **The parent object that runs the data-processing workflow.**

### Catalog + Schema

> **Defines where pipeline-generated tables/views are created.**

### Compute

> **Resources used to execute the pipeline.**

### One very important distinction

```text
transformations/
      ↓
Actual pipeline

explorations/
      ↓
Testing / scratchpad
```

The rest of this lecture is mostly **Databricks UI/configuration**, so you don't need to memorize every click. The concepts above are the useful part for your Data Engineering notes.
