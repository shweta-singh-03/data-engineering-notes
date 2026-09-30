# LDP Real-World Project – Ride Sharing Pipeline

## 1. What is the goal of this project?

Now that the basic LDP concepts are understood, the course starts a **real-world end-to-end project** using a ride-sharing application.

Think of something like:

```text
Uber / Ola
```

The application generates lots of data:

```text
Trips
Drivers
Users
Vehicles
etc.
```

The goal is to build a complete data pipeline using:

* Bronze
* Silver
* Gold
* LDP
* Streaming
* Batch/static data
* Stream-to-static joins
* OBT
* Star Schema

The instructor describes this as the point where the previously learned LDP concepts are applied to a realistic end-to-end pipeline.

---

# 2. First understand the data

The project has multiple relational tables.

For example:

```text
                 RIDE-SHARING DATA
                       │
        ┌──────────────┼───────────────┐
        ↓              ↓               ↓
      Trips          Drivers          Users
                                         
                      +
                   Vehicles
                      +
                  Other data
```

But **not all tables behave the same way**.

This is the key idea of this lecture.

---

# 3. Which table will be streamed?

The main table is:

```text
TRIPS
```

Why?

Because trips are continuously being generated.

Imagine:

```text
10:00 → Trip 1
10:01 → Trip 2
10:02 → Trip 3
10:03 → Trip 4
...
```

So the trips table is **continuously growing**.

Therefore:

> **Trips = streaming data**

The design is:

```text
Trips
  ↓
Streaming
  ↓
LDP
  ↓
Streaming Table
```

This follows the earlier concept that streaming tables are appropriate for continuously growing/append-oriented data.

---

# 4. What about Drivers, Users, Vehicles?

These tables are different.

For example:

```text
Drivers
Users
Vehicles
```

They are not the continuously arriving event stream in this project.

The instructor treats these as **mapping data / mapping tables**.

Think of them as lookup information.

For example:

```text
Trips
trip_id = 101
driver_id = D25
user_id   = U100
vehicle_id = V50
```

Then:

```text
Drivers
D25 → Rahul

Users
U100 → Shweta

Vehicles
V50 → Toyota
```

These tables help us **understand/enrich the trip**.

That's why the instructor calls them **mappers**.

---

# 5. The important distinction

Remember this:

```text
Trips
→ continuously growing
→ STREAM

Drivers / Users / Vehicles
→ lookup/reference information
→ STATIC/BATCH
```

So the architecture intentionally uses **different processing styles for different types of data**.

---

# 6. Bronze Layer

The first layer we want is Bronze.

The instructor says the Bronze layer will store the source tables.

Conceptually:

```text
SOURCE DATA
     ↓
   BRONZE
```

For this project:

```text
Bronze
├── Trips
├── Drivers
├── Users
└── Vehicles
```

But the ingestion method is different.

---

# 7. Bronze ingestion for mapping tables

For:

```text
Drivers
Users
Vehicles
```

the instructor uses a normal **PySpark notebook**.

Why?

Because:

> We don't need to continuously stream these tables.

So:

```text
Drivers
   ↓
PySpark
   ↓
Bronze

Users
   ↓
PySpark
   ↓
Bronze

Vehicles
   ↓
PySpark
   ↓
Bronze
```

The instructor specifically says there is no need to use LDP for these mapping tables in this project.

---

# 8. Why not use Materialized View for these?

The instructor mentions that Materialized Views could technically be used, but they are not necessary for this particular design.

The simple reason is:

> These are just static/mapping tables that we need for lookup purposes.

So don't overcomplicate them.

---

# 9. Bronze ingestion for Trips

Trips are different.

Because Trips are continuously arriving:

```text
New Trip
New Trip
New Trip
New Trip
...
```

we use LDP.

```text
Trips
  ↓
LDP
  ↓
Streaming Table
  ↓
Bronze / pipeline processing
```

So the project now has **two ingestion patterns**:

```text
                 INGESTION
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
       Trips              Mappers
          ↓                   ↓
        LDP                PySpark
          ↓                   ↓
      Streaming            Batch
```

---

# 10. Why this architecture makes sense

This is the important reasoning.

Don't use streaming just because streaming is available.

Choose the processing method based on the nature of the data.

### Trips

```text
Continuously arriving events
        ↓
Streaming
```

### Drivers / Users / Vehicles

```text
Reference / lookup information
        ↓
Batch/static
```

So:

> **Use the processing method that matches how the data behaves.**

---

# 11. Silver Layer

After Bronze, we create the Silver layer.

But the instructor is focusing the Silver processing mainly on:

```text
TRIPS
```

So:

```text
Bronze Trips
      ↓
     LDP
      ↓
Silver Trips
```

Why?

Because Trips are the **main streaming dataset** driving the pipeline.

---

# 12. Where do the mapping tables come in?

Now we have:

```text
Streaming Trips
```

and:

```text
Static Drivers
Static Users
Static Vehicles
```

We want to combine them.

For example:

```text
Trip
trip_id = 101
driver_id = D25
user_id = U100
```

We want:

```text
Trip
+
Driver information
+
User information
+
Vehicle information
```

This requires a join.

---

# 13. Stream-to-Static Join

This is one of the **most important concepts introduced in this lecture**.

We have:

```text
STREAM
Trips
  +
STATIC
Drivers / Users / Vehicles
```

Therefore:

> **Stream-to-Static Join**

Diagram:

```text
             STREAM
             Trips
               │
               │
               ├───────────┐
               │           │
               ↓           ↓
                         STATIC
                         Drivers
                         
               ↓
            JOIN
```

More realistically:

```text
Streaming Trips
       │
       │
       ├──────── JOIN ──────── Static Drivers
       │
       ├──────── JOIN ──────── Static Users
       │
       └──────── JOIN ──────── Static Vehicles
                    ↓
               Enriched Trips
```

This is different from a **stream-to-stream join**, where both sides are streams.

The lecture says there are two broad streaming join patterns:

```text
1. Stream → Stream
2. Stream → Static
```

This project uses:

> **Stream-to-Static Join**

---

# 14. Why do we need the join?

Because the Trips table may only contain IDs.

Example:

```text
Trips
---------------------------------
trip_id | driver_id | user_id
101     | D25       | U100
```

Drivers:

```text
driver_id | driver_name
D25       | Rahul
```

Users:

```text
user_id | user_name
U100    | Shweta
```

After joining:

```text
trip_id | driver | user
101     | Rahul  | Shweta
```

Now the trip is much more useful.

---

# 15. OBT – One Big Table

After the Silver processing and joins, the next step is to create an:

> **OBT = One Big Table**

The OBT combines the useful information into one wide dataset.

Conceptually:

```text
Trips
  +
Drivers
  +
Users
  +
Vehicles
  ↓
   JOIN
  ↓
 OBT
```

For example:

```text
trip_id
driver_id
driver_name
user_id
user_name
vehicle_id
vehicle_type
trip_date
fare
distance
...
```

Everything related to the trip is brought together.

---

# 16. Why is this OBT special?

The instructor specifically points out:

> **This OBT is append-only.**

Why?

Because the OBT is being created from a **streaming process**.

New trip arrives:

```text
Trip 101
Trip 102
Trip 103
```

Then later:

```text
Trip 104
Trip 105
```

The OBT receives the new trip records.

So conceptually:

```text
Existing OBT
    +
New Trips
    ↓
Append
```

This is different from an OBT design where you might repeatedly update/merge existing rows.

---

# 17. Complete architecture so far

This is the picture you should understand:

```text
                    RIDE-SHARING SOURCES
                             │
             ┌───────────────┴───────────────┐
             │                               │
          TRIPS                         MAPPING DATA
       (streaming)                  Drivers / Users / Vehicles
             │                               │
             ↓                               ↓
            LDP                          PySpark
             │                               │
             ↓                               ↓
        Bronze Trips                 Bronze Mapping Tables
             │
             ↓
         Silver Trips
             │
             │
             ├──────────────┐
             │              │
             ↓              ↓
         Drivers          Users
         (static)         (static)
             │              │
             └──────┬───────┘
                    ↓
              Stream-to-Static
                    JOIN
                    ↓
                  OBT
                    ↓
             Append-Only OBT
```

---

# 18. Gold Layer – Star Schema

After creating the OBT, we finally build the **Gold layer**.

The target is:

> **Star Schema**

A star schema normally contains:

```text
Fact Table
   +
Dimension Tables
```

Example:

```text
                 Dim Driver
                     │
                     │
Dim User ───── Fact Trips ───── Dim Vehicle
                     │
                     │
                 Dim Date
```

The **Fact Trips** table contains measurable/business events.

The dimensions provide descriptive information.

The course will explain facts and dimensions in more detail later.

---

# 19. Why OBT before Star Schema?

The architecture is:

```text
Bronze
  ↓
Silver
  ↓
OBT
  ↓
Star Schema
  ↓
Gold
```

Think of OBT as a **fully enriched dataset** from which the dimensional model can be created.

So:

```text
OBT
= everything about the trip in one place

Star Schema
= organize that information properly into
  Fact + Dimension tables
```

---

# 20. Full project architecture

This is the most important diagram from the lecture:

```text
                         SOURCE DATA
                             │
            ┌────────────────┴────────────────┐
            │                                 │
       TRIPS DATA                       MAPPING DATA
      (continuously                  Drivers / Users /
       growing)                         Vehicles
            │                                 │
            ↓                                 ↓
          LDP                              PySpark
            │                                 │
            ↓                                 ↓
     ┌─────────────┐                ┌─────────────────┐
     │    BRONZE   │                │     BRONZE      │
     │    TRIPS    │                │ Drivers/Users/  │
     └──────┬──────┘                │ Vehicles        │
            │                       └────────┬────────┘
            ↓                                │
     ┌─────────────┐                         │
     │   SILVER    │                         │
     │    TRIPS    │◄────────────────────────┘
     └──────┬──────┘
            │
            │ Stream-to-Static Join
            ↓
     ┌─────────────────┐
     │       OBT       │
     │   Append-only   │
     └────────┬────────┘
              ↓
        ┌─────────────┐
        │    GOLD     │
        │ Star Schema │
        └──────┬──────┘
               │
          ┌────┴────┐
          ↓         ↓
       Fact       Dimensions
```

---

# 21. Follow-along — What is actually being done?

For your practical notes, write the project setup like this.

### Step 1 — Prepare source data

The instructor has prepared ride-sharing data.

Tables include things like:

```text
Trips
Drivers
Users
Vehicles
```

---

### Step 2 — Identify streaming vs static data

```text
Trips
→ Streaming

Drivers
→ Static / Mapping

Users
→ Static / Mapping

Vehicles
→ Static / Mapping
```

This decision determines how we ingest/process each dataset.

---

### Step 3 — Build Bronze

For mapping tables:

```text
Drivers / Users / Vehicles
        ↓
     PySpark
        ↓
Bronze tables
```

For Trips:

```text
Trips
 ↓
LDP
 ↓
Streaming processing
 ↓
Bronze/Spark streaming table
```

---

### Step 4 — Build Silver

Process the streaming Trips data:

```text
Bronze Trips
     ↓
Transformations
     ↓
Silver Trips
```

---

### Step 5 — Join static data

Bring in:

```text
Drivers
Users
Vehicles
```

using:

```text
Stream-to-Static Join
```

---

### Step 6 — Build OBT

Combine the enriched trip information:

```text
Silver Trips
     +
Drivers
     +
Users
     +
Vehicles
     ↓
     OBT
```

The OBT is **append-only** in this design because it is part of the streaming pipeline.

---

### Step 7 — Build Gold Star Schema

Finally:

```text
OBT
 ↓
Fact Table
+
Dimension Tables
 ↓
Gold
```

---

# 22. What concepts are being introduced here?

This lecture is preparing you for several important DE concepts:

| Concept                   | Meaning                                                     |
| ------------------------- | ----------------------------------------------------------- |
| **Streaming data**        | Data continuously arriving                                  |
| **Static data**           | Reference/lookup data                                       |
| **Mapping table**         | Table used to look up additional information                |
| **Stream-to-Static Join** | Streaming data joined with static data                      |
| **OBT**                   | One Big Table containing combined/enriched data             |
| **Append-only OBT**       | New records are added rather than updating existing records |
| **Star Schema**           | Fact + Dimension model                                      |
| **Bronze**                | Initial stored data                                         |
| **Silver**                | Transformed/enriched data                                   |
| **Gold**                  | Business-ready model                                        |

---

# 23. Why this is a good real-world project

The project deliberately combines several things you've already learned:

```text
Spark
 +
PySpark
 +
Streaming
 +
LDP
 +
Bronze/Silver/Gold
 +
Joins
 +
OBT
 +
Star Schema
```

So you're no longer learning these concepts separately.

You're putting them together into **one complete data engineering system**.

---

# ⭐ CRUX — What you MUST remember

Don't memorize the instructor's entire explanation.

Remember this story:

### 🟠 Trips = moving data

Trips keep coming:

```text
Trip → Trip → Trip → Trip → ...
```

So:

```text
Trips
 ↓
STREAM
 ↓
LDP
```

### 🔵 Drivers / Users / Vehicles = lookup data

These help us understand the trip:

```text
Driver
User
Vehicle
```

So:

```text
Batch / Static
```

### 🟢 Then combine them

```text
Streaming Trips
       +
Static Drivers/Users/Vehicles
       ↓
Stream-to-Static Join
       ↓
Enriched Trips
```

### 🟡 Then create OBT

```text
Enriched Trips
      ↓
     OBT
      ↓
Append-only
```

### 🔵 Finally Star Schema

```text
OBT
 ↓
Fact + Dimensions
 ↓
GOLD
```

## 🧠 One-line memory trick

> **Trips move → LDP streams them → static tables enrich them → OBT combines everything → Star Schema organizes it for Gold.**

And the **whole project** can be remembered as:

```text
SOURCE
  ↓
BRONZE
  ↓
SILVER
  ↓
STREAM + STATIC JOIN
  ↓
OBT
  ↓
GOLD STAR SCHEMA
```

**Important:** this lecture is primarily the **architecture/design phase**. The actual transformations, joins, OBT construction, and star-schema implementation come in the following practical lectures, so don't try to memorize code from this one.
