# Managed Tables vs. External Tables (Study Notes)

> Topic: The single most important practical decision you make every time you create a table in Unity Catalog — who "owns" the data, and what happens to it when the table is dropped.
> ⚠️ **Important context**: This concept is **NOT unique to Databricks** — it's a general data-platform concept used across the industry (Hive, Snowflake, BigQuery, etc. all have similar Managed/External distinctions). Databricks/Unity Catalog just implements its own version of it.
> Includes: Interview Questions & DP-750 style exam questions at the end.

---

## Simple Definitions First

> **Managed Table** = You hand your data over to Databricks completely. Databricks decides where it's stored, and Databricks "owns" it. If you delete the table, **the data is deleted too**.

> **External Table** = You keep ownership of your data yourself, in a location YOU choose. Databricks only stores the table's *definition* (schema, column names, etc.) — not the data itself. If you delete the table, **the data stays completely untouched**, safe in your own storage.

🌟 **One-line analogy for both**:
- **Managed** = dropping your clothes off at a laundromat and saying "you handle everything" — throw the ticket away, and your clothes go with it.
- **External** = adding your own book to a public library's search catalog — the book physically stays on your home shelf. Remove it from the catalog, and your book is still sitting right there.

---

## Part 1 — What Every Table Is Made Of (Two Pieces)

Regardless of Managed or External, **every table always has exactly two components**:

| Component | What it is | Where does it live? |
|---|---|---|
| **1. Metadata** | Table definition — schema, column names, data types, permissions, lineage | Always in the **Metastore** (Databricks' own backend — recall this from earlier notes, it's never in ADLS) |
| **2. Actual Data** | The real rows and values | **Depends on table type** — this is the ONLY thing that differs between Managed and External |

```
              EVERY TABLE (Managed OR External)
                          │
            ┌──────────────┴──────────────┐
            ▼                                ▼
      METADATA                        ACTUAL DATA
   (always in Metastore,         (location DEPENDS on
    regardless of table type)     Managed vs. External)
```
*Caption: Metadata storage never changes based on table type — only the data's physical location does.*

---

## Part 2 — Managed Table: Raju's First Choice

### The Worked Example (from the lecture)
Raju has a CSV file and wants to use it in Databricks. He decides to create a **Managed Table**.

### What happens, step by step:
1. Raju's CSV data gets uploaded.
2. **Table definition** (schema, columns, etc.) → stored in the **Metastore**.
3. **Actual data** → stored in the Metastore's **default storage location** (recall: this is the `metastore` container in your Data Lake — the exact same one you saw when you physically browsed into it in the previous lecture!).

```
   RAJU'S CSV FILE
         │
         ▼
   "Create MANAGED table"
         │
    ┌─────┴─────┐
    ▼             ▼
METASTORE      DEFAULT STORAGE LOCATION
(table          (the "metastore" container —
 definition:     Databricks decides this,
 schema, cols)   Raju has no say in it)
```
*Caption: For a Managed Table, BOTH the definition AND the data end up under Databricks' control — the data specifically lands in the metastore's default storage.*

### Technical Example — Creating a Managed Table
```sql
-- No LOCATION specified = Managed Table by default
CREATE TABLE my_catalog.raw.bookings (
  booking_id INT,
  customer_name STRING,
  booking_date DATE
);
-- Databricks automatically decides WHERE this data physically lives
-- (falls back through Schema → Catalog → Metastore's default storage)
```

### The Critical Consequence: Dropping a Managed Table
```sql
DROP TABLE my_catalog.raw.bookings;
```
**What happens**: 
- ✅ The table definition (metadata) is removed from the Metastore.
- ❌ **The actual data files are ALSO deleted** — permanently, from the default storage location.

⚠️ **Why does this happen?** Because with a Managed Table, **you are not the owner of the data — Databricks is.** You handed over full control the moment you created it as "managed." When Databricks manages something, it also manages its full lifecycle, including deletion.

⚠️ **Small caveat mentioned in the lecture**: There ARE ways to "undrop" a table in Databricks (e.g., using `UNDROP TABLE` within a retention window) — but that's a separate safety-net feature, not something to rely on as your primary strategy. The core lesson stands: dropping a managed table is a genuinely destructive action by default.

---

## Part 3 — External Table: The Alternative Choice

### The Worked Example, Modified
Same Raju, same CSV file — but this time, Raju chooses to create an **External Table** instead.

### What changes:
- Raju **explicitly specifies** where the data should be stored — in **his own container**, under his own control (recall: this requires an **External Location** to be registered first, from two lectures ago!).
- The **table definition** still goes into the Metastore (this part never changes — recall Part 1: metadata is ALWAYS in the Metastore, no matter what).
- The **actual data** stays exactly where Raju put it — Databricks does not take ownership of it.

```
   RAJU'S CSV FILE (already sitting in Raju's own container)
         │
         ▼
   "Create EXTERNAL table" + LOCATION = Raju's own path
         │
    ┌─────┴─────┐
    ▼             ▼
METASTORE      RAJU'S OWN CONTAINER
(table          (Raju decides this,
 definition:     via an External Location
 schema, cols)   he already registered)
```
*Caption: For an External Table, the definition still goes to the Metastore, but the data stays exactly where Raju (the owner) put it.*

### Technical Example — Creating an External Table
```sql
-- LOCATION is explicitly specified = External Table
CREATE TABLE my_catalog.raw.bookings_external (
  booking_id INT,
  customer_name STRING,
  booking_date DATE
)
LOCATION 'abfss://raw@azuredatabricksname.dfs.core.windows.net/bookings/';
-- This path must already be a registered EXTERNAL LOCATION
-- (from the "External Locations & Credentials" lecture)
```

⚠️ **Prerequisite reminder**: You can't just type any random path here — that path must already be covered by a registered **External Location** (with an associated Storage Credential), or Databricks will reject the command with a permissions error — exactly like the errors you troubleshot in the External Locations lecture.

### The Critical Consequence: Dropping an External Table
```sql
DROP TABLE my_catalog.raw.bookings_external;
```
**What happens**:
- ✅ The table definition (metadata) is removed from the Metastore.
- ✅ **The actual data files remain completely untouched**, safely sitting in Raju's own container.

⚠️ **Why does this happen?** Because Raju never handed over ownership of the data — he only asked Databricks to "look at" and register this existing data as a queryable table. Removing that registration doesn't affect the underlying files at all.

---

## Part 4 — Side-by-Side Comparison

| Aspect | Managed Table | External Table |
|---|---|---|
| **Who owns the data?** | Databricks | You |
| **Where does metadata live?** | Metastore (always) | Metastore (always — same as managed) |
| **Where does the actual data live?** | Metastore's default storage location (e.g., the `metastore` container) | Wherever YOU specify, via a registered External Location |
| **`DROP TABLE` behavior** | Data is **deleted** along with the definition | Data is **preserved** — only the definition is removed |
| **How do you specify it?** | Just omit the `LOCATION` clause | Add an explicit `LOCATION` clause pointing to a registered External Location |
| **Best used when...** | You want Databricks to fully manage lifecycle/optimization of a table you're creating fresh | Data already exists elsewhere, needs to be shared with other tools, or you want strict control over deletion/retention |

---

## Interview Questions & Answers

### 1. "Explain the fundamental difference between a Managed Table and an External Table."

**Answer:** Both table types store their metadata (schema, column definitions, permissions) in the same place — the Metastore. The difference is entirely about the **actual data files**: for a Managed Table, Databricks decides where the data lives (typically the Metastore's default storage location) and takes full ownership of its lifecycle. For an External Table, the data lives wherever the user explicitly specifies (via a registered External Location), and Databricks only registers/references it — it never takes ownership.

### 2. "What happens when you run `DROP TABLE` on each type, and why does the behavior differ?"

**Answer:** Dropping a Managed Table deletes both the table definition AND the underlying data files, because Databricks owns the data's full lifecycle for managed tables. Dropping an External Table only removes the table definition from the Metastore — the actual data files remain completely untouched in their original location, because the user (not Databricks) owns that data; Databricks was simply referencing it.

**Example**: If a Finance team stores critical raw source files in a container also used by other internal tools, they'd want an External Table — accidentally dropping the Databricks-side table registration wouldn't wipe out data that other systems still depend on.

### 3. "Scenario: A teammate accidentally runs `DROP TABLE` on what turns out to be a Managed Table containing important data. What are their options?"

**Answer:** Databricks does provide an `UNDROP TABLE` safety-net feature within a certain retention window, which can recover a recently dropped managed table. However, this shouldn't be relied upon as a primary data protection strategy — the real lesson is to be deliberate about choosing Managed vs. External based on how critical it is that dropping the table registration should NOT delete the underlying data, and to have proper access controls/review processes around DROP operations on sensitive managed tables.

### 4. "Why might a data engineering team deliberately choose External Tables even though Managed Tables seem simpler to set up?"

**Answer:** A few common reasons: (1) the data already exists in a specific location and is also used by other tools/teams outside Databricks, so it can't just be "handed over"; (2) the team wants explicit control over retention and deletion — ensuring a table registration mistake in Databricks never risks the underlying data; (3) compliance/governance requirements may mandate that certain data stays in a specifically audited, access-controlled location rather than Databricks' own managed storage.

### 5. "If both Managed and External tables store their metadata in the same Metastore, what does 'ownership' actually mean in this context?"

**Answer:** "Ownership" here specifically refers to who controls the **data files' lifecycle** — not the metadata. For a Managed Table, Databricks' internal processes control creation, updates, and deletion of the underlying files as part of managing the table object itself. For an External Table, those file-lifecycle operations are the user's/organization's responsibility — Databricks only maintains a "pointer" (the table definition + location) to data that continues to be independently managed outside of Databricks' direct control.

---


## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: Managed Table — who owns the data?** → Databricks.
- **Q: External Table — who owns the data?** → You (the user/organization).
- **Q: Does metadata storage location ever change based on table type?** → No — always in the Metastore, for both types.
- **Q: What determines whether a table is Managed or External?** → Whether a `LOCATION` clause is explicitly provided at creation.
- **Q: `DROP TABLE` on a Managed Table — what happens to the data?** → Deleted along with the definition.
- **Q: `DROP TABLE` on an External Table — what happens to the data?** → Data remains untouched; only the definition is removed.
- **Q: What must exist before creating an External Table at a given path?** → A registered External Location (backed by a Storage Credential) covering that exact path.
- **Q: Is the Managed vs. External concept unique to Databricks?** → No — it's a general industry data-platform concept, implemented by Databricks/Unity Catalog in its own way.

### One-line mental model
```
Managed Table  = No LOCATION specified → Databricks owns data → DROP TABLE = data GONE
External Table = LOCATION specified (registered External Location) → YOU own data → DROP TABLE = data SAFE
Metadata (schema/columns) → ALWAYS in the Metastore, regardless of type
```

---
