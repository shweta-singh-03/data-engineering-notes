# SQL Warehouse Compute — Classic vs. Pro (Study Notes)

> Topic: The core definition and purpose of SQL Warehouse compute, who it's meant for, and the difference between its two traditional types — Classic and Pro (Serverless SQL Warehouse to be covered in the next lecture).
> 🌟 **Cross-reference**: This directly confirms and extends your earlier **"Compute Types Complete Reference"** notes — this lecture is the official course source for that SQL Warehouse comparison table.
> Includes: Interview Questions & DP-750 style exam questions at the end.

---

## Why This Topic Matters

You've already lived through this concept firsthand — your "Starter Warehouse" quota troubles were entirely about **Classic-type SQL Warehouse compute**. This lecture gives you the formal definition and reasoning behind why this compute type exists at all, and why "Pro" costs more but is considered the better traditional option.

---

## Part 1 — What IS SQL Warehouse Compute? (The Simplest Definition)

⚠️ **Naming confusion addressed directly**: *"It is not your like SQL warehouse... it is a type of compute."* Don't confuse this with a data warehouse (a storage/modeling concept). **SQL Warehouse = a compute type**, full stop.

> **Simplest possible definition**: If you want to query any data in Databricks using **pure SQL** (not PySpark, not Python — actual SQL queries), you need **SQL Warehouse compute.**

```
   You want to run a SQL query in Databricks
                    │
                    ▼
        You need SQL WAREHOUSE COMPUTE
        (this is the ONLY resource type
         built for this exact purpose)
```

⚠️ **Important distinction**: This is specifically for **pure SQL** querying — not for running PySpark code or general Python-based data engineering work (that's what your **cluster / All-Purpose compute** is for, from earlier notes).

---

## Part 2 — Who Actually Uses SQL Warehouse Compute?

### Worked Example from the Lecture
Imagine your company has:
- An **Analytics team**
- A **Reporting team** (e.g., building **Power BI** dashboards/reports)

Neither of these teams necessarily needs to write PySpark code or manage clusters — they just need to **run SQL queries** against your Databricks data. So, as the data engineer/admin, you:
1. Create a SQL Warehouse.
2. **Hand it over** to these teams as the resource they'll use.
3. They connect their tools (SQL Editor, Power BI, any BI tool via JDBC/ODBC) to this SQL Warehouse and query away.

```
                    ┌─────────────────┐
                    │   SQL WAREHOUSE     │
                    │   (compute you       │
                    │    create & hand      │
                    │    over)              │
                    └────────┬────────┘
          ┌────────────────┼────────────────┐
          ▼                    ▼                    ▼
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │ Analytics team  │   │ Reporting team  │   │ Power BI /      │
  │ (SQL Editor)     │   │ (dashboards)     │   │ any BI tool      │
  └──────────────┘   └──────────────┘   └──────────────┘
```
*Caption: SQL Warehouse is the ONE resource type you provide to any team/tool that needs to query Databricks data using pure SQL, rather than code.*

⚠️ **Key takeaway phrase from the lecture**: *"This is the only resource that you can just provide to anyone who wants to query the data."*

---

## Part 3 — Classic vs. Pro: The Two Traditional SQL Warehouse Types

⚠️ Just like Classic general-purpose compute had Standard vs. Dedicated access modes, **SQL Warehouse compute has its own further breakdown** — currently: **Classic** and **Pro** (with **Serverless** to be covered as a third type in the next lecture).

### Classic SQL Warehouse
**Simple English**: The basic, traditional SQL Warehouse type — behaves just like Classic general-purpose compute, with **no special optimization** beyond Photon acceleration (which is enabled on BOTH types, so it's not a differentiator between them).

### Pro SQL Warehouse
**Simple English**: Everything Classic has, PLUS one extra capability: **Predictive I/O.**

### What is Predictive I/O?
⚠️ **Simple English callout**: Predictive I/O is a module that **automatically predicts your SQL workload patterns** and uses that prediction to **scale your compute more efficiently** as query load increases or decreases.

🌟 **Everyday example**: Imagine a restaurant manager who's gotten really good at predicting exactly when the lunch rush will hit, so they can proactively call in extra staff *just before* the rush arrives — instead of scrambling to react only *after* customers are already lining up. Predictive I/O works similarly for your compute scaling — trying to anticipate demand rather than purely reacting to it after the fact.

⚠️ **Honest limitation acknowledged in the lecture**: *"It is not the best one... we still have better approaches."* Predictive I/O is a genuine improvement over Classic's lack of any such optimization, but it's not presented as the ultimate/most advanced solution — that distinction goes to Serverless (covered next lecture), which has even more advanced capabilities (recall from your Compute Types reference: **Intelligent Workload Management**, exclusive to Serverless).

### Doubt: "If both Classic and Pro have Photon, why does that matter at all?"
**Answer**: It matters because it clarifies that **Photon is NOT what separates Classic from Pro** — both get the same performance boost from Photon. The *actual* differentiator specifically is **Predictive I/O**, which only Pro has.

---

## Part 4 — The Quick-Check Question: Where Do Classic & Pro Actually Run?

### Doubt (posed directly in the lecture): "In case of BOTH Classic and Pro, where will the virtual machines/compute actually be created?"
**Answer**: **In YOUR Azure account.** Neither Classic nor Pro is Serverless — both are genuine Classic-family compute, meaning both **draw from your Azure subscription's vCPU quota** and take the "several minutes to start" path — exactly matching your own real experience with your "Starter Warehouse" (which was specifically the Classic type).

```
   CLASSIC SQL Warehouse  →  VMs created in YOUR Azure account  →  draws YOUR vCPU quota
   PRO SQL Warehouse       →  VMs created in YOUR Azure account  →  draws YOUR vCPU quota
   (SERVERLESS SQL Warehouse → NOT covered in this lecture — runs on Databricks' own infrastructure instead)
```

⚠️ This directly confirms and reinforces what you already personally experienced and documented in your Compute Types reference notes — your `standardEDSv4Family` quota error came specifically from choosing Classic, which behaves exactly as described here.

---

## Full Summary Comparison

| Feature | Classic SQL Warehouse | Pro SQL Warehouse |
|---|---|---|
| Runs in your Azure account? | ✅ Yes | ✅ Yes |
| Draws your vCPU quota? | ✅ Yes | ✅ Yes |
| Photon acceleration | ✅ Yes | ✅ Yes |
| Predictive I/O (smart scaling prediction) | ❌ No | ✅ Yes |
| Generally considered... | The basic option | The "better" traditional option |

---

## 🤔 Common Doubts — Quick Recap

### Doubt: "Is SQL Warehouse the same thing as a data warehouse?"
**Answer**: No — despite the confusingly similar name, SQL Warehouse is purely a **compute type/engine**, specifically for running SQL queries. A data warehouse is a data storage/modeling concept (covered extensively in your earlier Data Warehousing notes) — completely different topic.

### Doubt: "Should Data Engineers use SQL Warehouse for their regular ETL/pipeline work?"
**Answer**: Not typically — data engineers usually work with **general-purpose compute** (Classic clusters, or Serverless-for-notebooks) to run PySpark/Python-based pipelines. SQL Warehouse is specifically aimed at **SQL-only** consumers — analytics teams, reporting teams, BI tool connections.

### Doubt: "Why would anyone choose Classic over Pro, if Pro is 'better'?"
**Answer**: This lecture doesn't explicitly cover cost differences, but logically: Pro's extra Predictive I/O capability likely comes at a higher price point than Classic. Teams with simple, predictable, lower-stakes SQL query needs might reasonably stick with the cheaper Classic tier rather than pay extra for optimization they may not heavily benefit from.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What is SQL Warehouse compute, in the simplest terms?** → The compute type you use whenever you want to run pure SQL queries against Databricks data.
- **Q: Who typically uses SQL Warehouse compute?** → Analytics teams, reporting teams, and any BI tool (like Power BI) connecting to query Databricks data.
- **Q: What are the two traditional SQL Warehouse types covered in this lecture?** → Classic and Pro (Serverless to be covered separately).
- **Q: Do both Classic and Pro have Photon acceleration?** → Yes — Photon is not the differentiator between them.
- **Q: What is the key feature that ONLY Pro has (not Classic)?** → Predictive I/O.
- **Q: What does Predictive I/O do?** → Automatically predicts SQL workload patterns to help scale compute more efficiently as query load changes.
- **Q: Where do Classic and Pro SQL Warehouses actually run?** → Inside YOUR Azure account, drawing from your subscription's vCPU quota — neither is Serverless.
- **Q: Is Predictive I/O described as the "best possible" scaling solution?** → No — the lecture explicitly notes better approaches exist (hinting at Serverless's more advanced Intelligent Workload Management, covered separately).

### One-line mental model
```
SQL Warehouse = compute specifically for SQL queries (not PySpark/Python)
Classic = basic + Photon only
Pro     = Classic + Predictive I/O (smarter scaling)
BOTH run in YOUR Azure account, drawing YOUR vCPU quota (this is what caused your earlier errors)
```

---

## Interview Questions & Answers

### 1. "What is SQL Warehouse compute, and how is it different from general-purpose (Classic) compute?"

**Answer:** SQL Warehouse is a dedicated compute type specifically designed to run pure SQL queries — powering the SQL Editor, dashboards, and BI tool connections (like Power BI). General-purpose (Classic) compute, by contrast, is meant for broader workloads including PySpark, Python, and general data engineering code. If a team only needs to run SQL queries and doesn't need to write Python/Spark code, SQL Warehouse is the appropriate resource to provide them, rather than a general-purpose cluster.

### 2. "Explain the difference between Classic and Pro SQL Warehouse types."

**Answer:** Both Classic and Pro run inside the customer's own Azure subscription (drawing from its vCPU quota) and both have Photon acceleration enabled. The key differentiator is that Pro additionally includes Predictive I/O — a capability that predicts SQL workload patterns to enable more efficient, proactive scaling as query demand changes. Classic lacks this predictive scaling capability, making Pro the generally "better" (though likely costlier) traditional option between the two.

### 3. "A reporting team wants to build Power BI dashboards pulling data from Databricks. What compute resource should they be given, and why?"

**Answer:** They should be given access to a SQL Warehouse, since Power BI (like other BI tools) connects via JDBC/ODBC to run SQL queries — this is exactly the use case SQL Warehouse compute is built for. They wouldn't need or use general-purpose compute, since they're not writing PySpark/Python code.

### 4. "Scenario: A team using a Classic SQL Warehouse reports inconsistent query performance during sudden spikes in usage. Would switching to Pro necessarily solve this, and why?"

**Answer:** Switching to Pro would likely help, since Pro's Predictive I/O is specifically designed to anticipate workload changes and scale more efficiently in response — addressing exactly this kind of "sudden spike" scenario better than Classic (which lacks this predictive capability). However, it's worth noting the lecture itself acknowledges Predictive I/O "is not the best" approach available — if the team needs the most advanced scaling behavior, a Serverless SQL Warehouse (with Intelligent Workload Management) would be an even stronger solution, assuming it's available in their region.

---

## DP-750 Style Exam Questions & Answers

### Q1.
Which statement BEST describes what a SQL Warehouse is in Azure Databricks?

A. A physical data warehouse used for dimensional modeling and star schemas.
B. A compute type specifically designed to run SQL queries, used by analytics/reporting teams and BI tools.
C. A Unity Catalog object used to store table metadata.
D. A type of Azure Data Lake Storage container optimized for SQL file formats.

**✅ Correct Answer: B**

**Explanation:** Despite the potentially confusing name, a SQL Warehouse is a compute engine/type dedicated to running SQL workloads — not a data storage, modeling, or governance concept.

---

### Q2.
What is the key capability that differentiates a Pro SQL Warehouse from a Classic SQL Warehouse?

A. Only Pro supports Photon acceleration.
B. Only Pro includes Predictive I/O, which helps predict SQL workload patterns for more efficient scaling.
C. Only Classic can be used by BI tools like Power BI.
D. Only Pro runs inside the customer's Azure subscription.

**✅ Correct Answer: B**

**Explanation:** Both Classic and Pro support Photon acceleration and both run inside the customer's Azure subscription (option A and D are false). Predictive I/O is specifically the differentiating feature exclusive to Pro, enabling more efficient, workload-aware scaling compared to Classic.

---

### Q3.
Where do the virtual machines for BOTH Classic and Pro SQL Warehouses get provisioned?

A. Entirely within Databricks' own managed infrastructure, with no impact on the customer's cloud subscription.
B. Within the customer's own Azure subscription, drawing from that subscription's vCPU quota.
C. Only within Azure regions that support Unity Catalog.
D. Provisioning location depends solely on the Databricks Runtime version selected.

**✅ Correct Answer: B**

**Explanation:** Both Classic and Pro SQL Warehouse types are Classic-family compute, meaning their underlying VMs are provisioned inside the customer's own Azure subscription and are subject to that subscription's vCPU quota limits — unlike Serverless SQL Warehouses, which run on Databricks-managed infrastructure instead.

---

### Q4. (Scenario-based)
An organization's data engineering team writes PySpark-based ETL pipelines, while a separate analytics team only needs to run ad-hoc SQL queries and build dashboards. Which compute assignment reflects best practice based on this lecture's guidance?

A. Both teams should share a single SQL Warehouse for all their work.
B. The data engineering team should use general-purpose (Classic or Serverless) compute for their PySpark pipelines; the analytics team should use a SQL Warehouse for their SQL-only workloads.
C. Both teams should use only Serverless general-purpose compute, since SQL Warehouses are being deprecated.
D. The analytics team should use general-purpose compute, since SQL Warehouses cannot support dashboard tools.

**✅ Correct Answer: B**

**Explanation:** SQL Warehouse compute is specifically built for SQL-only workloads (ideal for the analytics team's needs), while general-purpose compute (Classic or Serverless) is needed for the data engineering team's PySpark-based ETL work, which SQL Warehouses cannot run. Matching compute type to actual workload type is the core best practice illustrated in this lecture.

---

*End of notes. Next lecture: Serverless SQL Warehouse — the third type, and how it compares to Classic and Pro.*
