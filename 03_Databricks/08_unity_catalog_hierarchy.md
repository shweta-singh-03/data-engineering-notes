# Unity Catalog Hierarchy (Study Notes)

> Topic: The structural hierarchy of Unity Catalog — Metastore → Catalog → Schema → Tables/Views/Volumes/Functions — plus External Locations and Credentials, and a quick tour of what you'll actually see in the Databricks UI.
> Includes: Interview Questions & DP-750 style exam questions at the end.

💰 **Cost note**: This lecture is purely conceptual/UI-viewing — nothing new was created or deployed. **No cost impact.** (Heads up: the *next* lecture is the actual Unity Catalog setup from scratch, which likely does involve creating real resources — I'll include a full Cost & Resource Management section for that one.)

---

## Why This Topic Matters

Now that you know **why** Unity Catalog matters (its 6 capabilities from the previous lecture), this lecture teaches you **how it's structured** — the actual hierarchy of objects you'll create and navigate. The great news: if you know basic SQL/database concepts (like PostgreSQL), you basically already know this hierarchy — Unity Catalog just reuses a familiar structure.

---

## The Core Hierarchy, Top to Bottom

```
                    UNITY METASTORE
                    (Level 1 — the TOP/highest level)
                          │
                          ▼
                    UNITY CATALOG
                    (Level 2 — like a "database")
                          │
                          ▼
                       SCHEMA
                    (Level 3 — same as a schema in Postgres)
                          │
            ┌─────────────┼─────────────┬──────────────┐
            ▼             ▼             ▼              ▼
         TABLES         VIEWS        VOLUMES        FUNCTIONS
       (Level 4 — the actual objects you work with day to day)
```
*Caption: Four main levels — Metastore is the top-level container, Catalog acts like a database, Schema organizes objects within it, and Tables/Views/Volumes/Functions are the actual working objects inside each schema.*

---

## Level 1: Unity Metastore

**Simple English**: This is the **very top, highest level** of the entire Unity Catalog hierarchy. Whenever someone says "metastore" in the context of Unity Catalog, they mean this — the **Unity Metastore**.

⚠️ Think of the Metastore as the outermost container that everything else (catalogs, and everything below them) lives inside.

---

## Level 2: Unity Catalog

**Simple English**: This is the **second level**. Within a Metastore, you create one or more **Unity Catalogs**.

🌟 **Everyday example / SQL comparison**: If you're coming from a SQL background (like PostgreSQL), think of a **Unity Catalog as equivalent to a "database"** in Postgres. That's literally the direct equivalent — same concept, different name.

This is where tables, schemas, and everything else gets managed.

---

## Level 3: Schema

**Simple English**: Inside a Unity Catalog, you create **Schemas** — and this is **exactly the same concept** as a "schema" in PostgreSQL. No new concept to learn here — it's a direct match.

🌟 **Everyday example**: If a Unity Catalog is like a whole database, a Schema is like one labeled section/folder within that database — grouping related tables together (e.g., a "sales" schema, a "hr" schema).

---

## Level 4: What Lives Inside a Schema

Just like in PostgreSQL, once you have a schema, you create your actual working objects inside it. In Unity Catalog, that's:

| Object | Simple English |
|---|---|
| **Tables** | The standard data tables you already know from any SQL database |
| **Views** | Saved queries that look like tables but don't store their own copy of data (same concept from your Data Warehousing notes earlier) |
| **Volumes** | ⚠️ A newer concept specific to Databricks — the lecture notes "you will learn about this" in a later, dedicated lecture. For now, just know it's one of the object types living at this level. |
| **Functions** | Reusable pieces of logic (functions) that can also be managed/governed within Unity Catalog |

```
   SCHEMA
     │
     ├── Tables      (standard data tables)
     ├── Views        (saved queries, no separate data copy)
     ├── Volumes      (newer concept — covered later)
     └── Functions    (reusable logic)
```
*Caption: These four object types are what you'll actually be creating and using day-to-day, all organized inside a Schema.*

---

## Two More Things at the Catalog Level: External Location & Credential

In addition to Catalogs, there are **two more object types** that sit **directly under the Metastore**, at the **same level as Catalog** (not inside a catalog — a sibling of it):

```
                    UNITY METASTORE
                          │
        ┌─────────────────┼─────────────────┐
        ▼                   ▼                   ▼
  UNITY CATALOG      EXTERNAL LOCATION      CREDENTIAL
  (Level 2)            (Level 2 — sibling)    (Level 2 — sibling)
```
*Caption: External Location and Credential are NOT inside a Catalog — they sit at the same hierarchy level as Catalog, directly under the Metastore.*

| Object | Simple English (brief preview — detailed lecture coming later) |
|---|---|
| **External Location** | A reference/pointer to a storage location outside of Databricks' own managed storage (e.g., pointing to a specific folder in your Azure Data Lake) |
| **Credential** | The security/authentication details used to actually access that external storage location |

⚠️ The lecture only briefly introduces these two here — just to show you where they sit structurally. Full detail comes in later, dedicated lectures.

---

## Full Combined Hierarchy Diagram

```
                              UNITY METASTORE
                     (Level 1 — top of the entire hierarchy)
                                     │
              ┌──────────────────────┼──────────────────────┐
              ▼                        ▼                        ▼
       UNITY CATALOG            EXTERNAL LOCATION           CREDENTIAL
      (= "database" in            (pointer to outside          (auth details for
       SQL terms)                  storage, e.g. ADLS)          external storage)
              │
              ▼
           SCHEMA
      (same concept as
       Postgres schema)
              │
     ┌────────┼────────┬─────────┐
     ▼        ▼         ▼         ▼
  TABLES   VIEWS    VOLUMES   FUNCTIONS
```
*Caption: The complete Unity Catalog hierarchy — Metastore at the top, with Catalog/External Location/Credential as siblings beneath it, and Schema → Tables/Views/Volumes/Functions nested inside each Catalog.*

---

## Seeing This Live in the Databricks UI

**Step 1** — Click **Catalog** in the left sidebar.

**Step 2** — You'll see a few pre-existing entries. Two important ones to recognize:

### `hive_metastore` (⚠️ Legacy — ignore this)
**Simple English**: This is the **old** metastore system that Databricks used **before** Unity Catalog existed. It's now considered **legacy/outdated**.

⚠️ **Instructor's advice**: You don't even need to look inside this. Simply close/ignore this tab — you won't be using it in this course, since we're working entirely with Unity Catalog going forward.

### The Default Unity Catalog
**Simple English**: You'll also see a catalog already present by default (under your organization), which — if you click into it — shows things like a "default" schema and an "information schema."

⚠️ **Important distinction**: 
- We will **never actually use** this pre-existing default catalog for real work in this course.
- We will instead **create our own, dedicated Unity Catalog** from scratch.
- But conceptually, this default one **is** a real example of the same "Unity Catalog" object type discussed above — useful just to see what one looks like.

### Why does a default Unity Catalog already exist for you?
⚠️ **Historical context**: Before 2024, Unity Catalog had to be **manually activated** in each Databricks workspace. **As of now, it's automatically enabled by default** — which is exactly why you already see this default catalog sitting there, even though you never manually set anything up.

---

## What's Coming Next: Setting Up Unity Catalog From Scratch

⚠️ Even though Unity Catalog is technically already "enabled" by default (as you just saw), that default setup isn't what you'll actually use for real project work. The **next section** of the course walks through **setting up your own Unity Catalog + Metastore from scratch**, including:
- Creating/connecting your own Metastore.
- Connecting it to your actual data (e.g., your Azure Data Lake).
- Multiple configuration steps tied together.

**The instructor emphasizes**: this setup process is described as **"the heart of the entire course"** — meaning you should follow it very closely, step by step, since everything else in the course depends on having this foundation correctly configured.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What is the top-level object in the Unity Catalog hierarchy?** → The Unity Metastore.
- **Q: What is the SQL/Postgres equivalent of a Unity Catalog?** → A database.
- **Q: What is the SQL/Postgres equivalent of a Schema in Unity Catalog?** → Exactly the same concept — a schema, no translation needed.
- **Q: What four object types live inside a Schema?** → Tables, Views, Volumes, and Functions.
- **Q: What sits at the same hierarchy level as Catalog, directly under the Metastore?** → External Location and Credential.
- **Q: What is `hive_metastore` in the Databricks Catalog UI?** → The legacy metastore system used before Unity Catalog existed — now outdated and safe to ignore.
- **Q: Why do you already see a default Unity Catalog without setting anything up?** → Since 2024, Unity Catalog is automatically enabled by default in new workspaces (previously it required manual activation).
- **Q: Will this course use the pre-existing default Unity Catalog?** → No — a dedicated Unity Catalog will be created from scratch in the next section.

### One-line mental model
```
Metastore (top)
  ├── Catalog        = "database"
  │     └── Schema   = same as Postgres schema
  │            ├── Tables
  │            ├── Views
  │            ├── Volumes
  │            └── Functions
  ├── External Location  (sibling of Catalog)
  └── Credential          (sibling of Catalog)
```

---

## Interview Questions & Answers

### 1. "Describe the Unity Catalog hierarchy from top to bottom."

**Answer:** At the very top is the Unity Metastore — the highest-level container. Within a Metastore, you create one or more Unity Catalogs, which are conceptually equivalent to a "database" in traditional SQL systems like PostgreSQL. Within each Catalog, you create Schemas — the same concept as a schema in Postgres. Within each Schema, you create the actual working objects: Tables, Views, Volumes, and Functions. Additionally, at the same level as Catalog (directly under the Metastore, not nested inside a Catalog), you also have External Locations and Credentials, which relate to referencing and authenticating to storage outside Databricks' own managed storage.

### 2. "If someone with a PostgreSQL background asks you to explain Unity Catalog's structure, how would you frame it for them?"

**Answer:** I'd map it directly onto what they already know: a Unity Catalog is equivalent to a "database" in Postgres, and a Schema within Unity Catalog is exactly the same concept as a schema in Postgres — no translation needed there. Within that schema, you create Tables and Views just like in Postgres. The main new concepts for them would be Volumes (a newer, Databricks-specific object type) and Functions being managed at this same governed level, plus the additional top-level Metastore layer that sits above everything, and External Locations/Credentials that don't have a direct Postgres equivalent since they relate to Databricks' cloud storage integration model.

### 3. "What is `hive_metastore`, and should new Databricks projects use it?"

**Answer:** `hive_metastore` is the legacy metastore system that Databricks used before Unity Catalog was introduced. It still appears in the Catalog UI for backward compatibility, but it's considered outdated. New projects should not use it — Unity Catalog is now the standard, and since Unity Catalog is automatically enabled by default in current workspaces, there's no reason to rely on the legacy Hive metastore for new work.

### 4. "Why might a new Databricks workspace already show a 'default' Unity Catalog, even if the user never explicitly set one up?"

**Answer:** Prior to 2024, Unity Catalog had to be manually activated within a Databricks workspace. As of current Databricks behavior, Unity Catalog is automatically enabled by default for new workspaces — which means a default catalog (along with things like a default schema and an information schema) is already present without any manual setup. However, this default catalog is typically not used for actual project work; teams generally create their own dedicated Unity Catalog(s) tailored to their organization's structure and needs.

### 5. "Where do External Locations and Credentials fit into the Unity Catalog hierarchy, and why does their placement matter?"

**Answer:** They sit at the same hierarchical level as Catalog — directly under the Metastore, rather than nested inside a specific Catalog. This placement matters because it reflects their role: External Locations and Credentials are about connecting Unity Catalog (at the Metastore level) to outside storage systems (like a Data Lake), and authenticating that connection — a concern that applies at a broader, Metastore-wide level rather than being scoped to just one individual Catalog.

---
