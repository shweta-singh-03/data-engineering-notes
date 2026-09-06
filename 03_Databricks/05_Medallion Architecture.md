# Medallion Architecture (Study Notes)

> Topic: The 3-layer (Bronze, Silver, Gold) data organization practice used in modern data engineering — including why it's not technically an "architecture," and the optional Data Marts layer.
> Includes: Interview Questions & DP-750 style exam questions at the end.

---

## Why This Topic Matters

By now you've heard of Lakehouse, Delta Lake, and Databricks architecture. This lecture introduces **Medallion Architecture** — the standard way data is *organized* once it lands inside your Lakehouse. This is used constantly in Databricks (and data engineering in general), so once you understand this, terms like "bronze layer" or "gold table" will never confuse you again.

⚠️ **Important clarification made right at the start**: Despite the name, Medallion Architecture is **NOT actually a technical "architecture"** in the same sense as, say, the Databricks Control Plane/Compute Plane architecture. It's simply a **practice** — a recommended, standard way of organizing your data as it flows through your system.

---

## The Problem: Getting Data from Source to Lakehouse Isn't a Single Step

### Simple English: Setting up the scenario
Imagine Raju, a data engineer, has many different data **sources** — a SQL database, some APIs, an S3 bucket, and more. Raju's goal is to eventually serve clean, usable data to end users (business stakeholders, analysts, dashboards, etc.) — and to do that, he needs to build a **Lakehouse** (or data warehouse).

🌟 **Everyday example**: On paper, this sounds simple — like saying "just take groceries from the store and put them directly onto a dinner plate." But in reality, there are several steps in between: unpacking the groceries, washing them, cutting/preparing them, cooking them, and *then* plating them. You can't skip straight from "raw groceries" to "finished plated meal" — and the same is true for raw data becoming a finished, trustworthy report.

```
SOURCES  ──────────►  ???  ──────────►  LAKEHOUSE (ready for reporting)
(SQL DB, APIs, S3,       (this is NOT
 many different           a single, simple
 formats/systems)         "dump" step!)
```
*Caption: Moving data from raw sources to a usable Lakehouse involves multiple layers/steps in between — not a direct one-shot dump.*

### The Solution: A 3-Layer Architecture
In modern industry, this journey is broken into **three layers**. This 3-layer practice is called **Medallion Architecture**.

⚠️ **Simple English callout — Why "Medallion"?** Because the three layers are named after **medals**: **Bronze**, **Silver**, and **Gold** — just like an Olympic medal ranking, where each layer represents an "upgrade" in data quality over the previous one.

---

## The Three Layers, Explained

```
   SOURCES                BRONZE                SILVER                GOLD
 (SQL DB, APIs,    ──►   (raw, as-is,   ──►    (fully          ──►   (modeled:
  S3, etc.)                no changes)          transformed          facts, dims,
                                                  data)                SCDs, etc.)
```
*Caption: Data flows through three progressively "cleaner" and more usable layers — Bronze → Silver → Gold.*

### 🥉 Layer 1: Bronze Layer ("Raw Layer")

**Simple English**: This is where you dump your data **exactly as it came from the source** — no changes, no cleaning, no transformations whatsoever.

⚠️ **This is a hard rule to remember**: We should **never** make transformations directly in the Bronze layer. Its entire purpose is to preserve the data exactly as-is.

🌟 **Everyday example**: This is like the moment groceries first arrive at your kitchen counter, straight out of the delivery bag — nothing washed, nothing chopped, nothing cooked. You're just storing the raw ingredients exactly as they arrived, so you always have an unaltered original copy to go back to if needed.

**Why keep data completely unmodified here?** Having a raw, untouched copy means that if something goes wrong later in the pipeline (a bad transformation, a bug, a business rule change), you can always go back to this original, trustworthy source-of-truth copy and reprocess it — nothing was lost or altered at this stage.

---

### 🥈 Layer 2: Silver Layer (Transformed Layer)

**Simple English**: Here, you **fully transform** your data. This is where the actual cleaning, filtering, joining, standardizing, and general data-quality work happens.

🌟 **Everyday example**: This is the "washing, peeling, and chopping" stage in cooking — you're taking those raw ingredients from the counter (Bronze) and actually preparing them properly: removing bad parts, cutting them to the right size, making them ready to actually cook with.

---

### 🥇 Layer 3: Gold Layer (Modeled / Business-Ready Layer)

**Simple English**: This is where you build your final, business-ready **data model** — this connects directly back to everything you learned in the Data Warehousing notes: dimensional data modeling, fact tables, dimension tables, and Slowly Changing Dimensions (SCDs) are all built here.

🌟 **Everyday example**: This is the finished, beautifully plated dinner — ready to be served directly to guests (your business stakeholders). No further prep work needed; it's ready for immediate consumption.

**What happens on top of the Gold layer?**
This is where all your **reports and dashboards** get built, and where **data-driven decisions** actually happen for the business:
- Tools like **Power BI** connect here.
- Data Analytics teams use this layer.
- Data Science teams can use this layer.
- Essentially, **anyone** consuming data for decision-making works from this Gold layer.

---

## The Optional Fourth Layer: Data Marts

Some organizations add one more, **optional** layer after Gold, called **Data Marts**.

### Simple English: What are Data Marts here?
Small, focused "mini Lakehouses," built for one **specific business purpose or department** (this directly connects to the "Data Mart" concept from the ETL/Data Warehousing notes earlier — same idea, just now placed at the end of the Medallion journey).

⚠️ **Important note**: This layer is **optional**. In roughly **90% of real-world cases**, organizations stop at the Gold layer and consider that sufficient — Data Marts are only added in specific situations where a business genuinely needs a separately curated, domain-specific slice of the Gold data.

```
SOURCES → BRONZE → SILVER → GOLD → (optional) DATA MARTS
                                ↓                    ↓
                         Power BI, Analytics,   Domain-specific
                         Data Science teams,     mini-Lakehouses
                         anyone consuming data   (e.g., just Finance,
                         for decisions            just HR, etc.)
```
*Caption: The full journey, including the optional Data Marts layer used by some (but not most) organizations.*

---

## Why Is This Called a "Practice," Not an "Architecture"?

Because Medallion Architecture doesn't dictate *specific technical components* (like servers, planes, or a particular tool) the way something like the Databricks Control Plane/Compute Plane architecture does. Instead, it's simply a **recommended pattern/practice** for organizing your data pipeline into three progressively refined stages — you can implement this practice using many different underlying tools and technologies (Databricks, or otherwise).

⚠️ **Alternative naming you should recognize**: Some people/organizations don't use the "Bronze/Silver/Gold" naming at all — they instead call the same three layers:
- **Raw** (= Bronze)
- **Enriched** (= Silver)
- **Curated** (= Gold)

**The names are different, but the underlying concept — three layers representing a data lifecycle from raw to business-ready — is exactly the same.**

---

## Full Recap Diagram

```
┌───────────┐   ┌──────────────┐   ┌──────────────────┐   ┌────────────────────────┐   ┌───────────────────┐
│  SOURCES    │──►│ 🥉 BRONZE      │──►│  🥈 SILVER          │──►│  🥇 GOLD                  │──►│  (optional) DATA MARTS │
│ SQL DB,     │   │ = "Raw"       │   │ = "Enriched"        │   │ = "Curated"                │   │ Small, domain-specific │
│ APIs, S3,    │   │ - as-is copy   │   │ - fully transformed  │   │ - dimensional data model     │   │ mini-Lakehouses         │
│ etc.         │   │ - NO           │   │ - cleaned, joined,   │   │   (facts, dims, SCDs)         │   │ (e.g., Finance-only)     │
│              │   │   transforms   │   │   standardized       │   │ - reports/dashboards built here│   │                         │
└───────────┘   └──────────────┘   └──────────────────┘   └────────────────────────┘   └───────────────────┘
                                                                        │
                                                                        ▼
                                                        Power BI, Data Analytics team,
                                                        Data Science team — anyone making
                                                        data-driven decisions
```

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What is Medallion Architecture, in one sentence?** → A 3-layer (Bronze, Silver, Gold) practice/pattern for organizing data as it moves from raw sources to a business-ready Lakehouse.
- **Q: Is Medallion Architecture technically an "architecture"?** → No — it's a practice/pattern, not a specific technical system design.
- **Q: What happens in the Bronze layer?** → Data is dumped exactly as-is from the source, with absolutely no transformations applied.
- **Q: What happens in the Silver layer?** → Data is fully transformed — cleaned, standardized, joined, and prepared.
- **Q: What happens in the Gold layer?** → The final business-ready data model is built here (dimensional modeling: fact tables, dimension tables, SCDs), and this is the layer reports/dashboards and analytics teams consume.
- **Q: What's the optional fourth layer, and how common is it?** → Data Marts — small, domain-specific mini-Lakehouses (e.g., just for Finance). Optional; used in roughly 10% of cases, since 90% of organizations stop at Gold.
- **Q: What are the alternative names for Bronze/Silver/Gold?** → Raw (Bronze), Enriched (Silver), Curated (Gold) — same underlying concept, different naming convention.
- **Q: Why is the Bronze layer kept completely untransformed?** → To always preserve an unaltered, trustworthy original copy of the data, so you can go back and reprocess it if anything goes wrong later in the pipeline.
- **Q: Who typically consumes data from the Gold layer?** → Power BI/reporting tools, Data Analytics teams, Data Science teams, and generally anyone in the business making data-driven decisions.

### One-line mental model
```
Bronze (Raw)     = exact copy of source data, untouched
Silver (Enriched) = fully cleaned/transformed data
Gold (Curated)    = final business-ready model (facts, dims, SCDs) → reports & decisions
(optional) Data Marts = small, domain-specific slices built on top of Gold
```

---

## Interview Questions & Answers

### 1. "What is Medallion Architecture, and why is it described as a 'practice' rather than a true architecture?"

**Answer:** Medallion Architecture is a widely-adopted, three-layer pattern (Bronze, Silver, Gold) for organizing data as it moves from raw sources into a usable, business-ready Lakehouse. It's called a "practice" rather than a strict architecture because it doesn't prescribe specific technical infrastructure or components (like a particular storage system or compute layer) — it's simply a recommended way of structuring your data pipeline's stages, and it can be implemented using many different underlying tools and technologies, including but not limited to Databricks.

### 2. "Walk me through what happens at each layer of the Medallion Architecture, with an example."

**Answer:**
- **Bronze (Raw)**: Data is ingested exactly as it comes from the source — no transformations. Example: raw JSON logs from an API, stored exactly as received.
- **Silver (Enriched)**: Data gets fully transformed — cleaned, deduplicated, joined with other datasets, standardized. Example: those raw JSON logs get parsed, bad records filtered out, and fields standardized into a clean tabular format.
- **Gold (Curated)**: The final, business-ready data model is built — dimensional modeling with fact tables, dimension tables, and slowly changing dimensions as needed. Example: a `fact_sales` table joined with `dim_customers`, `dim_products`, etc., ready for direct use in Power BI dashboards.

### 3. "Why is it considered a strict rule to avoid applying transformations directly in the Bronze layer?"

**Answer:** The Bronze layer's entire purpose is to serve as an untouched, trustworthy copy of the original source data. If transformations were applied here, you'd risk losing the ability to go back to a truly raw, unaltered version of the data if something later in the pipeline turns out to be wrong (a bug, an incorrect business rule, a data quality issue discovered later). Keeping Bronze completely raw means you can always reprocess from a reliable starting point without needing to re-extract from the original source system again.

**Example**: If a transformation bug in the Silver layer is discovered a month later, having an untouched Bronze layer means engineers can simply re-run the corrected transformation against the original raw data — rather than needing to re-pull potentially unavailable historical data from the source system.

### 4. "When would an organization choose to add an optional Data Marts layer on top of Gold, versus just using the Gold layer directly?"

**Answer:** Data Marts are typically added when a specific business domain or department (e.g., Finance, HR) needs a separately curated, focused subset of the data — often for reasons like simplified access control, domain-specific performance tuning, or providing that team with a smaller, more relevant dataset rather than the entire Gold layer. In practice, most organizations (roughly 90% of cases) find the Gold layer sufficient on its own and skip this additional layer, adding it only when there's a clear, specific business need for that extra separation.

### 5. "Scenario: A new team member is confused because your organization calls its layers 'Raw, Enriched, and Curated' instead of 'Bronze, Silver, and Gold.' How would you explain this to them?"

**Answer:** I'd explain that these are just two different naming conventions for the exact same underlying concept — a three-layer data organization pattern. "Raw" = "Bronze" (untouched, as-is data), "Enriched" = "Silver" (fully transformed/cleaned data), and "Curated" = "Gold" (the final, business-ready modeled data). Different organizations and teams sometimes prefer different terminology, but the intent and structure behind both naming schemes is identical — three progressively refined stages taking data from raw source form to business-ready output.

---

*End of notes. This 3-layer (Bronze/Silver/Gold) mental model will show up constantly for the rest of this course — every time you build a pipeline, ingest data, or design a Databricks workflow, you'll be placing that work into one of these three layers.*
