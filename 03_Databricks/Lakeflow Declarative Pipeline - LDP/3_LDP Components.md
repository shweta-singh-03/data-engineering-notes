# LDP – Core Components

## 1. Pipeline

A **Pipeline** is the **parent object** that contains the complete end-to-end data processing design.

```text
Pipeline
   │
   ├── Data processing
   ├── Flows
   ├── Streaming tables
   ├── Materialized views
   ├── Views
   ├── Data quality
   └── Governance
```

### Simple definition

> **Pipeline = the complete structure of your data pipeline in LDP.**

A pipeline can contain multiple processing steps and datasets.

---

# 2. Datasets

According to the lecture, LDP works with **three main types of datasets**:

1. Streaming Table
2. Materialized View
3. View

---

## 2.1 Streaming Table

A **Streaming Table** is a table created using **Spark Structured Streaming**.

```text
Source
  ↓
Structured Streaming
  ↓
Streaming Table
```

It is designed for **incremental processing** and continuously growing data.

### Typical use case

Use a streaming table when the source is **append-only**.

Example:

```text
New files arrive
      ↓
Auto Loader / Streaming
      ↓
Streaming Table
```

The lecture describes Auto Loader as using Spark Structured Streaming under the hood.

### Important point

The lecture emphasizes:

> Streaming tables are suitable when the source keeps **appending new data** rather than changing existing records.

If the source contains updates/deletes, other mechanisms such as CDC-related functionality are needed.

### Remember

**Streaming Table = streaming + incremental data**

---

# 3. Materialized View

A **Materialized View** is a dataset produced using **batch processing**.

For simple understanding:

> **Materialized View = batch-oriented table that stores data.**

Unlike a normal view, it **actually stores/materializes the result**.

### Important characteristic

The lecture explains that materialized views can perform **incremental processing automatically**, so you define your batch transformations and the framework handles incremental processing rather than requiring you to manually implement it.

```text
Source
  ↓
Batch Transformation
  ↓
Materialized View
```

### Simple comparison

| Dataset           | Processing  | Stores data? |
| ----------------- | ----------- | ------------ |
| Streaming Table   | Streaming   | Yes          |
| Materialized View | Batch       | Yes          |
| View              | Query-based | No           |

### Easy memory trick

> **Streaming Table → streaming target**
> **Materialized View → batch target**

---

# 4. View

A normal **View** is essentially a **query/result definition** rather than a stored physical dataset.

It is useful for **intermediate results** when you don't want to persist the final result as a table.

```text
Source
  ↓
Query
  ↓
View
```

## Types of Views

The lecture mentions:

* Normal View
* Streaming View

### Streaming View

A streaming view can incrementally read data and is created on top of a **streaming table**.

### Easy distinction

```text
View
→ Does not store the result

Materialized View
→ Stores the result
```

---

# 5. Flows — The Backbone of LDP

**Flow** is the foundational data-processing concept in LDP.

It supports both:

* Batch processing
* Streaming processing

### What does a flow do?

A flow:

```text
SOURCE
  ↓
Read data
  ↓
Transform data
  ↓
TARGET
```

So, a flow is essentially the **connection/process between the source and target**.

### Simple definition

> **Flow = reads data → applies transformations → writes the result to a target.**

Possible targets include:

* Streaming Table
* Materialized View
* View

---

# 6. Special Flows / Decorators

One major benefit of LDP is that Databricks provides special functionality through flows/decorators.

The lecture specifically mentions:

### Auto CDC

Used for scenarios such as:

* Upserts
* Change Data Capture
* Slowly Changing Dimensions

Instead of manually writing large amounts of code for these operations, LDP provides built-in functionality.

```text
CDC Data
   ↓
Auto CDC
   ↓
Target Table
```

The lecture specifically contrasts Auto CDC with Apache Spark, stating that this functionality is provided by Databricks LDP.

### Append Flow

Used for append-oriented processing.

---

# 7. Sinks

A **Sink** is used when you want to send/write the processed data to an external destination such as a **data lake**.

The lecture introduces sinks as another way to define where pipeline output should go.

```text
Source
  ↓
Flow
  ↓
Processed Data
  ↓
Sink
  ↓
Data Lake
```

### Simple definition

> **Sink = destination where pipeline output is written.**

---

# 8. Data Quality

LDP also provides functionality for **data-quality checks**.

Typical checks can include:

* NULL checks
* Duplicate checks
* Other validation rules

Example concept:

```text
Input Data
    ↓
Data Quality Checks
    ↓
Valid Data
    ↓
Downstream Tables
```

The goal is to prevent bad data from propagating downstream.

---

# 9. Governance

The lecture also highlights **governance through Unity Catalog**.

So LDP works together with the Databricks governance layer for managing data and pipeline assets.

---

# 10. Complete LDP Picture

Put everything together:

```text
                    LDP PIPELINE
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     Datasets          Flows            Other
        │                │                │
   ┌────┼────┐           │        ┌───────┼───────┐
   │    │    │           │        │       │       │
Streaming MV  View    Processing  Quality Governance Sinks
 Table       │
             │
        Streaming View
```

More practically:

```text
SOURCE
  ↓
FLOW
  ↓
TRANSFORMATION
  ↓
┌─────────────────────────────┐
│ Streaming Table             │
│ Materialized View           │
│ View                        │
└─────────────────────────────┘
  ↓
Data Quality / Governance
  ↓
Downstream consumers
```

---

# 11. Most Important Differences

| Concept               | Main idea                               | Processing            |
| --------------------- | --------------------------------------- | --------------------- |
| **Pipeline**          | Parent/container for the whole pipeline | Overall orchestration |
| **Streaming Table**   | Stores streaming/incremental data       | Streaming             |
| **Materialized View** | Stores result of batch processing       | Batch                 |
| **View**              | Query/intermediate result               | Query-based           |
| **Streaming View**    | Incrementally reads streaming data      | Streaming             |
| **Flow**              | Reads → transforms → writes             | Batch or streaming    |
| **Auto CDC**          | Simplifies CDC/upsert/SCD processing    | Incremental           |
| **Sink**              | Sends output to an external destination | Output                |

---

# 12. The Most Important Concept to Remember

Think of LDP like this:

```text
                PIPELINE
                    │
             ┌──────┴──────┐
             │             │
           FLOWS        DATASETS
             │             │
      Read → Transform   ├── Streaming Table
             ↓            ├── Materialized View
          Write            └── View
                    │
            ┌───────┴────────┐
            │                │
        Data Quality      Governance
            │                │
            └───────┬────────┘
                    ↓
                  SINK
                    ↓
               Data Lake
```

### Interview one-liners

**Pipeline:**

> A pipeline is the parent structure that contains the complete data-processing workflow in LDP.

**Streaming Table:**

> A streaming table is used for incrementally processing continuously growing, typically append-oriented data using streaming semantics.

**Materialized View:**

> A materialized view stores the result of batch transformations and, as described in the lecture, can process new data incrementally.

**View:**

> A view is a query definition that does not persist the final result as a physical table.

**Flow:**

> A flow reads data from a source, applies transformations, and writes the result to a target.

**Auto CDC:**

> Auto CDC is Databricks LDP functionality that simplifies change-data processing such as upserts and SCD scenarios.
