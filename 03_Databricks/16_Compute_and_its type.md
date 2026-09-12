# What is Compute? & Types of Compute in Databricks (Study Notes)

> Topic: The fundamentals of what "compute" actually means (CPU, RAM, disk), and the three types of compute in Databricks — Classic Compute, SQL Warehouse, and Serverless (which isn't really a separate "third type," but a flavor that applies to both of the other two).
> Includes: Interview Questions & DP-750 style exam questions at the end.

---

## Why This Topic Matters

Everything you've done hands-on so far — running notebooks, creating tables, querying data — was only possible because of **compute** running silently behind the scenes. This lecture makes that invisible engine visible, and sets up the compute-type vocabulary (Classic, SQL Warehouse, Serverless) you'll be configuring for the rest of the course.

🌟 **Personal connection**: This is exactly the topic behind everything you've been troubleshooting recently — your Starter Warehouse's slow starts and quota errors were all about **Classic-type SQL Warehouse compute**, and the cluster you're about to create for your notebooks is **Classic-type general-purpose compute**. This lecture gives you the vocabulary to describe what you've already been doing hands-on.

---

## Part 1 — What IS "Compute," Fundamentally?

### Simple English: Setting the scene
When Raju uses Databricks, he's really just interacting with a nice **web application** (the Control Plane, from your Architecture notes). But behind the scenes, Databricks automatically sends Raju's data and code to a **cluster** to actually get processed. That cluster — the actual machines doing the real work — is what "compute" refers to.

⚠️ **Simple English callout — Cluster**: A group of machines (or "nodes" — machine = node, especially in distributed computing contexts) working together.

```
   RAJU (using the Databricks web app)
         │
         │  "process this data for me"
         ▼
   DATABRICKS (Control Plane)
         │
         │  automatically sends the work to...
         ▼
   COMPUTE (a CLUSTER — group of machines/nodes)
         │
         ▼
   Actual data engineering / data science / analytics work happens HERE
```
*Caption: Compute is the invisible engine behind every action you take in the Databricks UI — this is where your data actually gets processed.*

⚠️ **Why compute is described as "the backbone of everything"**: Every single type of work you'd do in Databricks — data engineering, data science, data analytics — ultimately depends on compute to actually execute. Without compute, Databricks is just an empty interface.

### What compute is physically made of

| Component | Simple English | Why it's needed |
|---|---|---|
| **CPU (Processor)** | The actual chip that processes/crunches your data (e.g., Intel i5/i7, AMD Ryzen — could be literally any processor brand, depending on the machine) | This is the "worker" doing the actual computation |
| **RAM (Main Memory)** | Fast, temporary memory the CPU uses while working | ⚠️ **Critical point**: A CPU chip has only tiny internal storage (small "registers" built into the chip itself) — nowhere near enough to hold real datasets. It NEEDS external RAM to actually have room to work with meaningful amounts of data. |
| **Disk / Storage** | Where data sits when not actively being processed | Cheap, and can even be attached externally if needed |
| **Cores / Threads** | Subdivisions within a CPU that let it do multiple things in parallel | More cores/threads = more parallel processing capacity |

🌟 **Everyday example**: Think of the CPU as a chef, RAM as the kitchen counter space where the chef actively works with ingredients, and Disk as the pantry/fridge where ingredients are stored until needed. A brilliant chef (fast CPU) with no counter space (RAM) to actually lay out ingredients can't cook efficiently, no matter how skilled they are — this is exactly why CPU and RAM always go hand in hand.

⚠️ **Why CPU and RAM are described as inseparable partners**: The CPU alone can't "remember" or hold onto large amounts of data — its internal registers are extremely small. RAM is what gives the CPU enough working space to actually process real datasets.

---

## Part 2 — The Types of Compute in Databricks

⚠️ **Historical context**: This is a relatively recent expansion — Databricks didn't always have this many compute types/options. The landscape has grown as the platform matured.

```
                         DATABRICKS COMPUTE
                                 │
                  ┌───────────────┴───────────────┐
                  ▼                                   ▼
          CLASSIC COMPUTE                      SQL WAREHOUSE
        (the traditional,                    (a dedicated compute
         standard option)                      ENGINE specifically
                  │                             for SQL workloads)
                  │                                   │
                  └───────────────┬───────────────┘
                                   ▼
                          SERVERLESS
                   (a FLAVOR that applies to
                    BOTH of the above — not a
                    separate third category)
```
*Caption: There are really just two core "families" of compute (Classic and SQL Warehouse) — Serverless is a modern flavor/variant available within EITHER family, not a standalone third type.*

### 1. Classic Compute
**Simple English**: The traditional, standard type of compute — this is what data engineers have used for years, and it's still the mainstream choice for most real data engineering work today.

### 2. SQL Warehouse
⚠️ **Naming clarification straight from the lecture**: *"SQL Warehouse is not your warehouse SQL"* — meaning, don't confuse this term with a data warehouse! **SQL Warehouse is a compute ENGINE** — a dedicated type of compute specifically built to run SQL workloads efficiently (this is exactly what you've been configuring/troubleshooting as your "Starter Warehouse").

### 3. Serverless (a flavor, not a separate type)
**Simple English**: Serverless isn't its own standalone category sitting alongside Classic and SQL Warehouse — it's more like a **modifier/flavor** that can apply to EITHER of them:
- You can have **Serverless (for general-purpose/notebook) compute**.
- You can have **Serverless SQL Warehouse compute**.

⚠️ **Databricks officially recommends Serverless** as the modern, forward-looking direction — but real-world adoption is more mixed, for practical reasons covered next.

---

## Part 3 — Why Do Organizations Still Use Classic Compute, If Serverless Is Recommended?

Two real, practical reasons given in the lecture:

1. **Legacy investment**: Many organizations have been using Classic compute for years, with hundreds of existing pipelines already built and running on it. Migrating all of that isn't trivial or risk-free.
2. **Need for more control**: Classic compute gives organizations more granular control over their compute environment (e.g., specific VM configurations, networking setup) — something that matters for certain security/compliance/performance requirements that Serverless's more "hands-off, Databricks-managed" model doesn't offer in the same way.

🌟 **Personal connection**: This is also, practically speaking, exactly why YOU are currently using Classic compute for both your cluster and your SQL Warehouse — not by choice of "control," but because Serverless simply isn't available in your region (South India) yet. Real organizations sometimes choose Classic deliberately; you're currently using it out of regional necessity — but the compute itself behaves the same way either way.

---

## 🤔 Common Doubts — Quick Recap

### Doubt: "Is Serverless a completely different, third type of compute?"
**Answer**: No — think of Classic and SQL Warehouse as the two "base" compute families, and Serverless as an optional flavor/mode that can be layered onto either one. So really, at a fundamental level, you're choosing: (1) Classic or SQL Warehouse, and (2) within that choice, whether to run it in its traditional form or its Serverless form (if available in your region).

### Doubt: "Why can't a CPU just store all the data it needs internally, without needing RAM?"
**Answer**: A CPU chip only has extremely small internal storage areas called "registers," built directly into the chip. These are nowhere near large enough to hold meaningful datasets — they're designed for tiny, ultra-fast intermediate calculations, not for holding gigabytes of working data. RAM exists specifically to give the CPU a much larger (though still fast) space to actively work with real data.

### Doubt: "If Databricks recommends Serverless, why would anyone deliberately choose Classic?"
**Answer**: Because "recommended" doesn't mean "mandatory" or "always better for every situation" — organizations with large existing Classic-based investments, or specific control/configuration needs, have legitimate reasons to stick with Classic, even as the industry gradually shifts toward Serverless as the newer standard.

---

## Interview Questions & Answers

### 1. "Explain what 'compute' means in Databricks, and what it's physically made of."

**Answer:** Compute refers to the actual processing infrastructure — a cluster of machines (nodes) — that Databricks automatically uses behind the scenes to execute your code, queries, and pipelines, whenever you interact with the Databricks web application (Control Plane). Physically, compute consists of a CPU (the processor that does the actual computation), RAM (fast working memory the CPU needs since its own internal registers are far too small to hold real datasets), and disk/storage (for data at rest, which can also be attached externally).

### 2. "What are the two core 'families' of compute in Databricks, and how does Serverless relate to them?"

**Answer:** The two core families are Classic Compute (the traditional, standard option) and SQL Warehouse (a dedicated compute engine specifically for SQL workloads). Serverless is not a third, separate family — it's a modern flavor/mode that can be applied to either Classic-style compute or SQL Warehouse compute, meaning you can have Serverless general-purpose compute AND Serverless SQL Warehouses as two distinct applications of the same underlying "serverless" concept.

### 3. "Why might a large organization continue using Classic compute despite Databricks officially recommending Serverless?"

**Answer:** Two main reasons: first, many organizations have years of existing infrastructure and hundreds of pipelines already built and tuned for Classic compute, making migration a significant undertaking with real risk. Second, Classic compute offers more granular control over the compute environment — specific VM types, networking configuration, etc. — which some organizations need for compliance, security, or specialized performance requirements that a more Databricks-managed Serverless model doesn't expose in the same way.

### 4. "Why is 'SQL Warehouse' a potentially confusing name, and what does it actually refer to?"

**Answer:** The name can be mistaken for a data warehouse (a storage/data modeling concept covered in earlier data warehousing topics), but a SQL Warehouse in Databricks is actually a compute engine — a dedicated type of compute infrastructure specifically optimized to run SQL queries efficiently (e.g., for the SQL Editor, dashboards, or BI tool connections), not a place where data is stored.

### 5. "Scenario: A new data engineer, working in a region where Serverless compute isn't yet available, asks whether their pipelines will behave differently than a colleague's pipelines running on Serverless in a supported region. How would you answer?"

**Answer:** Functionally, their Classic compute-based pipelines should produce the same correct results as their colleague's Serverless-based pipelines — the core data processing logic doesn't change based on compute type. The differences would mainly be operational: Classic compute typically takes longer to start up (provisioning real VMs from scratch each time) compared to Serverless's near-instant, pre-warmed pool of capacity, and Classic compute usage is also subject to the customer's own Azure subscription quotas/limits, which Serverless bypasses since it runs on Databricks-managed infrastructure instead.

---
