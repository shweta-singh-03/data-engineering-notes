# Managed vs. External Catalogs & Schemas (Study Notes)

> Topic: Extending the Managed vs. External concept one level UP — from tables to Catalogs and Schemas themselves — and the exact resolution order Databricks uses to decide where a new table's data lands when no location is specified.
> ⚠️ **Terminology note**: The instructor calls this "not very very important, but kind of important" — it's more about building strong intuition than being a heavily tested exam term. See the clarification callout near the end regarding official vs. informal terminology.

---

## Quick Recap: Where This Builds From

You already know:
- **Managed Table** = no `LOCATION` given → Databricks decides storage → drop = data deleted.
- **External Table** = `LOCATION` given → you decide storage → drop = data safe.

This lecture asks: *what if we apply this SAME idea one level higher — to the Catalog and Schema objects themselves, not just Tables?*

---

## Part 1 — The Metastore Already Has a Data Lake Attached

Recall from your Unity Metastore setup notes: when you created your Metastore, you attached a Data Lake to it (the `metastore` container). This becomes the **default fallback location** for anything below it that doesn't specify its own location.

```
UNITY METASTORE
      │
      │ (attached Data Lake — the "metastore" container)
      ▼
DEFAULT LOCATION
```

---

## Part 2 — Managed Catalog vs. "External" Catalog

### Scenario 1: Catalog created WITHOUT its own location
```sql
CREATE CATALOG azure_databricks_catalog;
-- No location specified!
```
🌟 Since you didn't attach any data lake at the catalog level, this catalog simply **uses whatever the Metastore already has attached.** In this lecture's terminology, this is called a **Managed Catalog**.

### Scenario 2: Catalog created WITH its own explicit location
```sql
CREATE CATALOG azure_databricks_catalog
MANAGED LOCATION 'abfss://bronze@storageaccount.dfs.core.windows.net/';
```
🌟 Now this catalog has its **own dedicated data lake location**, separate from the Metastore's default. In this lecture's terminology, this is called an **External Catalog**.

⚠️ **Simple English callout — the keyword `MANAGED LOCATION`**: Don't let the word "managed" here confuse you with "Managed Table"! In this context, **"Managed Location" is just the literal SQL syntax/property name** used to tell a Catalog (or Schema) where its default storage should be. It does **NOT** mean the tables inside it become "External" — tables created without their own `LOCATION` inside this catalog are still perfectly normal **Managed Tables** — they just now default to THIS catalog's location instead of the Metastore's.

```
SCENARIO 1: Managed Catalog                SCENARIO 2: "External" Catalog
(no location at catalog level)              (explicit MANAGED LOCATION given)

UNITY METASTORE                             UNITY METASTORE
   │ (default location)                        │
   ▼                                            │
CATALOG ──uses metastore's location──►      CATALOG ──has its OWN location──►
                                                  (bronze container, separate
                                                   from metastore's default)
```

---

## Part 3 — Same Logic Applies to Schema

### Scenario A: Schema created WITHOUT its own location
```sql
CREATE SCHEMA azure_databricks_catalog.dummy;
-- No location specified — this is a "Managed Schema"
```
It falls back to whatever location its **parent Catalog** uses (which itself might be falling back to the Metastore).

### Scenario B: Schema created WITH its own explicit location
```sql
CREATE SCHEMA azure_databricks_catalog.dummy
MANAGED LOCATION 'abfss://silver@storageaccount.dfs.core.windows.net/';
```
This Schema now has its own dedicated storage, independent of both its parent Catalog AND the Metastore.

---

## Part 4 — The Core Rule: "Closest Location Wins" (Resolution Order)

This is the single most important takeaway from this lecture.

> **When you create a table WITHOUT specifying a `LOCATION`, Databricks checks — starting from the CLOSEST level to the table, moving outward — and uses the FIRST location it finds.**

```
   Step 1: Does the SCHEMA have its own location?  ──Yes──► USE IT (closest, wins)
              │ No
              ▼
   Step 2: Does the CATALOG have its own location?  ──Yes──► USE IT
              │ No
              ▼
   Step 3: Fall back to the METASTORE's default location
```
*Caption: Proximity determines the winner — Schema beats Catalog, Catalog beats Metastore. Whichever is defined AND closest to the table gets used.*

### Worked Example
```
Metastore default location:  metastore@storageaccount/
Catalog "azure_databricks_catalog" location:  bronze@storageaccount/
Schema "dummy" (inside that catalog):  NO location specified

CREATE TABLE azure_databricks_catalog.dummy.my_table (...);
-- No LOCATION given for the table either

RESULT: Data lands in → bronze@storageaccount/
(because Schema had none, so it fell back to the CATALOG's location,
 which WAS defined — Catalog wins over Metastore in this case)
```

🌟 **Everyday analogy**: Think of it like asking "where should I mail this package?" You first check if there's a specific desk address (Schema). If not, check if there's a department address (Catalog). If that's not set either, fall back to the company's main headquarters address (Metastore). Whichever specific address exists closest to the actual recipient is the one used.

---

## Part 5 — What Real-World Practice Actually Looks Like

⚠️ **Directly from the lecture**: *"In the real world, we simply create the data lake at the Metastore level, and then we use a Managed Catalog and Managed Schema."*

```
REAL-WORLD RECOMMENDED PATTERN:

UNITY METASTORE ──has the ONLY data lake attached──► ONE default location
      │
      ├── Catalog (Managed — no own location)  ──► uses Metastore's default
      │      └── Schema (Managed — no own location) ──► uses Metastore's default
      │
      └── Catalog (Managed — no own location)  ──► uses Metastore's default
             └── Schema (Managed — no own location) ──► uses Metastore's default
```

⚠️ **Why this simplicity is preferred in practice**: You don't need to keep track of/manage multiple separate storage accounts or locations — everything cleanly cascades down from one single, well-governed attachment point (the Metastore). "External Catalogs" and "External Schemas" **do exist as a capability**, but are rarely used in practice — most teams simply attach the data lake once, at the top, and let everything flow down from there.

⚠️ **But you should still KNOW this capability exists** — for those rarer cases where a specific catalog genuinely needs its own dedicated, isolated storage location (e.g., strict compliance separation between business units), you now know exactly how to do it: `CREATE CATALOG ... MANAGED LOCATION '...'`.

---

## ⚠️ Terminology Clarification (Important for Exam-Safety)

Databricks' **official documentation** formally defines "Managed" and "External" specifically for **Tables** (and mentions "Managed storage locations" as a general concept for Catalogs/Schemas) — but it does **not** commonly use the exact phrase **"External Catalog"** as an official, standardized term the way it does for "External Table." 

This lecture's "Managed Catalog vs. External Catalog" framing is a **useful, intuitive teaching simplification** — extending the same mental model you already understand for tables, up one level — but if you see exam language, expect it phrased more like:
- *"a catalog with its own managed storage location"* (= what this lecture calls "External Catalog")
- *"a catalog using the metastore's default managed storage location"* (= what this lecture calls "Managed Catalog")

The underlying **behavior and resolution logic are 100% accurate and exam-relevant** — just be aware the exact label "External Catalog" is this instructor's simplification, not necessarily verbatim official terminology.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What makes a Catalog "Managed" (per this lecture's terminology)?** → It has no explicit location of its own — it uses the Metastore's default location.
- **Q: What makes a Catalog "External" (per this lecture's terminology)?** → It has its own explicit `MANAGED LOCATION` specified at creation.
- **Q: Does the same logic apply to Schemas?** → Yes — identical pattern: no location = uses parent Catalog's (or ultimately Metastore's) location; explicit location = has its own dedicated storage.
- **Q: What is the exact resolution order when creating a table with no `LOCATION`?** → Schema (closest) → Catalog → Metastore (farthest/default fallback) — whichever is closest AND defined wins.
- **Q: Does giving a Catalog/Schema its own `MANAGED LOCATION` make TABLES inside it "External Tables"?** → No — tables created without their own `LOCATION` are still Managed Tables; they just default to that Catalog/Schema's specific location instead of the Metastore's.
- **Q: What does real-world practice usually look like?** → One data lake attached at the Metastore level; Catalogs and Schemas are typically left as "Managed" (no individual locations), letting everything cascade from the single Metastore attachment.
- **Q: What is the SQL syntax for giving a Catalog its own location?** → `CREATE CATALOG name MANAGED LOCATION 'abfss://...'`

### One-line mental model
```
No location at Schema → check Catalog → no location at Catalog → check Metastore → use its default
Closest defined location ALWAYS wins.
"MANAGED LOCATION" keyword = just syntax for "here's this object's default storage" — NOT related to Managed vs External TABLES.
```

---

*End of notes. This closes the loop on the full Metastore → Catalog → Schema → Table storage resolution story — you now understand exactly how Databricks decides where every single piece of managed data physically lands, at every level of the hierarchy.*
