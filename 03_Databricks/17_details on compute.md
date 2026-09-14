# Databricks Compute Types — Complete Reference (Classic, SQL Warehouse, Serverless)

> A consolidated reference note clarifying every compute type in Azure Databricks, their subtypes, and how they all relate to each other. Built to resolve the "Classic vs. All-Purpose" and "does SQL Warehouse have types too?" doubts in one place.

---

## The Big Picture First

```
                         DATABRICKS COMPUTE
                                 │
              ┌───────────────┴───────────────┐
              ▼                                   ▼
     GENERAL-PURPOSE COMPUTE                 SQL WAREHOUSE
   (for notebooks, Python, Spark,          (for SQL-only workloads:
    ML, pipelines — anything)               SQL Editor, dashboards,
              │                              BI tool connections)
              │                                   │
    ┌─────────┼─────────┐              ┌─────────┼─────────┐
    ▼          ▼          ▼              ▼          ▼          ▼
CLASSIC    CLASSIC    CLASSIC        CLASSIC      PRO      SERVERLESS
All-       Jobs       Lakeflow       SQL          SQL      SQL
Purpose    Compute    Pipelines      Warehouse    Warehouse Warehouse
Compute               Compute
    │
    └── (Serverless general-purpose compute also exists,
         as an alternative to Classic — where region-supported)
```
*Caption: Two top-level compute families (General-Purpose and SQL Warehouse), each with their own sub-types — and "Serverless" cuts across both families as an alternative deployment mode, not a separate family of its own.*

---

## PART 1 — Classic Compute (General-Purpose)

### Definition
**Classic Compute** = an umbrella term for **any compute that YOU deploy, configure, and manage, running inside YOUR OWN cloud account (Azure subscription)** — as opposed to Serverless, which runs on Databricks-managed infrastructure.

⚠️ **Key identifying trait**: If it draws from **your Azure vCPU quota** (like the errors you've been troubleshooting), it's Classic compute.

### The THREE types of Classic Compute

| Type | What it's for | Termination behavior | Sharing |
|---|---|---|---|
| **All-Purpose Compute** | Interactive work — notebooks, ad-hoc exploration, data engineering development | Auto-terminates based on **inactivity** (the "15-20 min idle" setting) | Often **shared** across a whole team |
| **Jobs Compute** | Automated, scheduled jobs/workflows | Terminates **immediately once the job finishes** — no idle waiting | Typically dedicated to just that one job run |
| **Lakeflow Pipelines Compute** | Powers Lakeflow Declarative Pipelines (the modern ETL/DLT-style pipelines) | Managed automatically as part of the pipeline's lifecycle | Dedicated to that pipeline |

🌟 **Simple analogy for the three types**:
- **All-Purpose** = your own car sitting in the driveway, ready anytime, shared by the whole family, running whenever someone's actively using it.
- **Jobs Compute** = a rental car booked for exactly one delivery trip — picked up, used, and returned immediately after, never left idling.
- **Lakeflow Pipelines Compute** = a dedicated delivery van that comes with its own driver and route, automatically managed as part of a bigger, ongoing delivery service.

⚠️ **This is what YOU currently have**: The cluster you created earlier (single node, smallest VM, 15-20 min auto-termination, attached to your notebook) is specifically **All-Purpose Compute** — one type of Classic Compute.

### Why Databricks recommends against using All-Purpose Compute for scheduled Jobs
- Billed at a **different (higher) rate** than dedicated Jobs Compute.
- All-Purpose is often shared with other users → your scheduled job could face delays waiting for resources.
- Optimizations meant for "ad-hoc, interactive" work don't suit automated, repeated job runs well.

---

## PART 2 — SQL Warehouse

### Definition
A **SQL Warehouse** is a **dedicated compute engine built specifically to run SQL queries** — powering the SQL Editor, Dashboards, and any BI tool (like Power BI) connecting via JDBC/ODBC. ⚠️ It **cannot run Python or general-purpose code** — SQL only.

### YES — SQL Warehouse has THREE types too: Classic, Pro, Serverless

This is exactly the dropdown you saw showing "Classic" and "Pro" as your available options (with Serverless greyed out/missing due to your region).

| Feature | **Classic** | **Pro** | **Serverless** |
|---|---|---|---|
| **Where compute runs** | Inside YOUR Azure subscription | Inside YOUR Azure subscription | Databricks-managed infrastructure (NOT your subscription) |
| **Draws from your Azure vCPU quota?** | ✅ Yes | ✅ Yes | ❌ No |
| **Startup time** | Several minutes (~4 min typical) | Several minutes (~4 min typical) | ~4-6 **seconds** |
| **Photon** (fast vectorized query engine) | ✅ Supported | ✅ Supported | ✅ Supported |
| **Predictive I/O** (speeds up selective scans) | ❌ Not supported | ✅ Supported | ✅ Supported |
| **Intelligent Workload Management (IWM)** (smart autoscaling for bursty query loads) | ❌ Not supported | ❌ Not supported | ✅ Supported |
| **Best for** | Basic interactive/exploratory queries, lowest cost among the two Classic-family options | Custom networking needs (connecting to on-prem/hybrid networks, event buses, etc.), better performance than Classic | Almost all use cases, per Databricks' own recommendation — least operational overhead, fastest, most scalable |

⚠️ **This is EXACTLY what you've been experiencing**: your "Starter Warehouse" is a **Classic-type SQL Warehouse** (confirmed by its detail page showing `Type: Classic`) — which is precisely why it draws from your Azure vCPU quota and hit those `standardEDSv4Family` errors.

### Simple English — what each performance feature means
- **Photon**: A faster, rewritten query engine (think "turbocharged engine") that makes your existing SQL run faster without you changing anything.
- **Predictive I/O**: Smart techniques to avoid scanning data you don't actually need for a query — like skimming only the relevant chapters of a book instead of reading the whole thing.
- **Intelligent Workload Management (IWM)**: An AI-driven system that automatically scales resources up/down based on how many queries are hitting the warehouse at once — handling sudden bursts of activity gracefully.

---

## PART 3 — Serverless (the mode that cuts across both families)

### Definition
**Serverless** = compute that is **fully managed by Databricks itself**, running on Databricks' own shared infrastructure pool — **not inside your Azure subscription at all.**

### Where Serverless applies
```
SERVERLESS is available as an option for:
  ✅ General-purpose compute (notebooks, jobs) → "Serverless compute"
  ✅ SQL Warehouses → "Serverless SQL Warehouse"
  ✅ Lakeflow Pipelines → "Serverless pipelines"
```
*It's not one single product — it's a deployment MODE that several different Databricks compute products can each offer.*

### Why Databricks recommends it (when available)
- **Startup time**: seconds, instead of minutes.
- **No vCPU quota headaches**: doesn't touch your Azure subscription's limits at all.
- **No infrastructure to configure**: no VM sizing, no cluster policies to maintain, no manual scaling decisions.
- **Best performance features unlocked**: as shown in the SQL Warehouse table above, Serverless is the ONLY tier with full Intelligent Workload Management.

### Why it's still not universal
- ⚠️ **Region availability**: Not every Azure region supports it yet (confirmed: your region, South India, currently doesn't — while nearby Central India does).
- Some organizations deliberately avoid it for **custom networking requirements** (e.g., needing to connect to on-premises systems) or because of **existing infrastructure investment** in Classic.

---

## Full Comparison Table — Every Type, Side by Side

| Compute | Family | Runs in your Azure account? | Typical startup time | Draws your vCPU quota? |
|---|---|---|---|---|
| All-Purpose Compute | Classic (General-Purpose) | ✅ Yes | Minutes | ✅ Yes |
| Jobs Compute | Classic (General-Purpose) | ✅ Yes | Minutes | ✅ Yes |
| Lakeflow Pipelines Compute (Classic mode) | Classic (General-Purpose) | ✅ Yes | Minutes | ✅ Yes |
| Serverless (General-Purpose) | Serverless | ❌ No | Seconds | ❌ No |
| Classic SQL Warehouse | SQL Warehouse | ✅ Yes | ~4 minutes | ✅ Yes |
| Pro SQL Warehouse | SQL Warehouse | ✅ Yes | ~4 minutes | ✅ Yes |
| Serverless SQL Warehouse | SQL Warehouse | ❌ No | ~4-6 seconds | ❌ No |

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: Is "Classic Compute" the same as "All-Purpose Compute"?** → No. Classic is the umbrella category (compute in your own Azure account); All-Purpose is one specific TYPE of Classic compute, alongside Jobs Compute and Lakeflow Pipelines Compute.
- **Q: What are the three types of Classic (general-purpose) compute?** → All-Purpose, Jobs, and Lakeflow Pipelines compute.
- **Q: Does SQL Warehouse have sub-types too?** → Yes — Classic, Pro, and Serverless.
- **Q: What's the main difference between Classic and Pro SQL Warehouses?** → Pro adds Predictive I/O support (faster selective scans) that Classic lacks; both still run inside your own Azure subscription and draw from your vCPU quota.
- **Q: What's the ONLY SQL Warehouse tier with Intelligent Workload Management?** → Serverless.
- **Q: What determines whether compute draws from YOUR Azure vCPU quota?** → Whether it's Classic (yes, always) or Serverless (no, never) — regardless of whether it's general-purpose compute or a SQL Warehouse.
- **Q: Is Serverless its own separate compute family?** → No — it's a deployment MODE available within both the General-Purpose compute family and the SQL Warehouse family.

### One-line mental model
```
CLASSIC = runs in YOUR Azure account, uses YOUR quota, takes minutes to start
  ├── General-Purpose: All-Purpose / Jobs / Lakeflow Pipelines compute
  └── SQL Warehouse: Classic / Pro tiers

SERVERLESS = runs on DATABRICKS' infrastructure, no quota impact, starts in seconds
  ├── Available for General-Purpose compute (where region supports it)
  └── Available as SQL Warehouse's "Serverless" tier (where region supports it)
```

---

*This note consolidates everything from the "What is Compute" lecture notes with the SQL Warehouse type details confirmed directly against current Databricks documentation, and connects each concept to what you've personally already configured/troubleshot in this course.*
