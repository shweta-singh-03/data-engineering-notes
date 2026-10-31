# Data Engineering Fundamentals Class: Complete Study Notes


## How to Use These Notes

- Read in order. Each section follows the same recipe: **Big idea → Analogy → Diagram → Worked example → Interview questions**.
- Legend: 🌟 = real-life analogy or example, 💡 = “Simple English” jargon buster, ⚠️ = common mistake or trap, ✅ = checkpoint (you should be able to say it out loud before moving on).
- This video is a **concept (theory) class**, not a click-along project. So instead of project steps you will find a **build-order checklist** near the end that you can use to design a data platform from scratch.
- Presenter’s tip: draw the analogies in your own notebook. Silly drawings are far easier to remember than formal definitions.
- Where I add something that was **not** in the video (extra examples, SQL, corrections), I mark it as *(extra)* so you know the difference.


## The Big Picture (Read This First)

```
 UPSTREAM                          YOU                            DOWNSTREAM
 (data is born and stored)         (data engineer)                (data is used)

 +----------------+          +----------------------+         +--------------------+
 | Apps, websites |          |  ETL / data pipeline |         | Dashboards (BI)    |
 | OLTP databases | -------> |  Staging -> Core     | ------> | Data analysts      |
 | CSV, JSON, API |          |  (or Bronze -> Silver|         | Data scientists    |
 | Streams (IoT)  |          |   -> Gold)           |         | Managers           |
 +----------------+          +----------------------+         +--------------------+
   1. PRODUCTION               2. TRANSFORMATION                3. SERVING
```

*Caption: the entire video in one picture. Data is born upstream, you clean and reshape it in the middle, and downstream people use it.*

| # | Topic | One-line meaning |
| --- | --- | --- |
| 1 | Data engineering | Move data from where it is created to where it is used, and clean it on the way |
| 2 | Three pillars | Production, transformation, serving |
| 3 | Upstream / downstream | Who gives you data / who receives it from you |
| 4 | OLTP vs OLAP | Write-friendly source database vs read-friendly analytics database |
| 5 | ETL and pipelines | Extract, transform, load, automated |
| 6 | Warehouse layers | Staging layer first, then core layer |
| 7 | Incremental loading | Load only the new data, not everything again |
| 8 | Dimensional modeling | Facts + dimensions; star and snowflake schemas |
| 9 | Slowly changing dimensions | What to do when dimension data changes (types 0, 1, 2, 3) |
| 10 | Data lake, warehouse, lakehouse | Cheap flexible storage + warehouse-style tables |
| 11 | File formats | Row-based vs column-based storage |
| 12 | Delta format | Parquet + transaction log = database powers on a lake |
| 13 | Big data, Spark | Many computers working as one |
| 14 | Cloud computing | Renting computers instead of buying them |
| 15 | Medallion architecture | Bronze, silver, gold layers |
| 16 | End-to-end Azure architecture | Which Azure tool does which job |

---

## 1. What Is Data Engineering, and Why Do Companies Need Data Engineers?

### 1.1 The definition used in the video

> **Data engineering = taking raw, messy data, refining it with transformations, and serving it to stakeholders in the form of clean data models.**

```
  RAW DATA             TRANSFORM                  DATA MODELS             STAKEHOLDERS
 (messy, no    --->  (clean, fix, join,   --->  (tidy tables built  --->  (analysts, managers,
  links)                reshape)                 for a purpose)           data scientists)
```

*Caption: the one-line journey behind every data engineering job.*

💡 **Simple English**

- **Raw data**: data exactly as it was captured, with typos, duplicates, gaps and no links between sources.
- **Transformation**: any change that makes data cleaner or more useful (fix typos, remove duplicates, join two tables, calculate totals).
- **Data model**: a planned layout of tables built for a purpose, so people can find answers quickly.
- **Stakeholder**: anyone who needs the data to do their job or make a decision (clients, managers, analysts, scientists).

🌟 **Analogy: the data engineer is a chef.**

| Kitchen world | Data world |
| --- | --- |
| Farm / market that supplies vegetables | Upstream sources (apps, databases, APIs) |
| Raw potatoes, onions, carrots | Raw data |
| The chef | **You, the data engineer** |
| Washing, chopping, seasoning, cooking | Transformation (cleaning, joining, aggregating) |
| One big pot of cooked food | Transformed data before modeling |
| Small plates (half plate, full plate, as ordered) | Data models (tables shaped for each type of user) |
| Hungry customers | Stakeholders |

The chef does not care *who* grew the carrots. The chef only cares that carrots, potatoes and spices are in the pantry. In the same way, you do not care *who clicked* on the app; you care that the data is sitting in a source you can read.

> Don’t memorize a definition. Google shows thousands of them. Understand the concept: **move data from where it is created to where it is used, and improve its quality while it travels.**

### 1.2 Worked example: a pizza-delivery app *(extra)*

**Raw table `raw_orders` (what the app saved):**

| order\_id | customer | city | qty | price |
| --- | --- | --- | --- | --- |
| 101 | Aman | Mumbai | 2 | 300 |
| 101 | Aman | Mumbai | 2 | 300 |
| 102 | Riya | mumbai | 1 | 450 |
| 103 | Sam | MUMBAI | NULL | 200 |

Problems hiding in there:

1. Order 101 appears **twice** (duplicate), so revenue would be double counted.
2. “Mumbai”, “mumbai” and “MUMBAI” look like **three different cities** to a computer.
3. Order 103 has no quantity (**missing value**).

**Transformation (SQL):**

```sql
-- Keep one copy of each order, standardise the city, calculate revenue
SELECT DISTINCT
       order_id,
       customer,
       UPPER(TRIM(city))  AS city,      -- Mumbai / mumbai / MUMBAI -> MUMBAI
       qty,
       qty * price        AS revenue    -- new useful column
FROM   raw_orders
WHERE  qty IS NOT NULL;                 -- row 103 goes to a review (quarantine) table instead
```

**Curated table `curated_orders` (what the dashboard reads):**

| order\_id | customer | city | qty | revenue |
| --- | --- | --- | --- | --- |
| 101 | Aman | MUMBAI | 2 | 600 |
| 102 | Riya | MUMBAI | 1 | 450 |

⚠️ **Common mistake:** silently “fixing” the missing quantity by guessing 1. Guessing hides a real data problem. Send bad rows to a quarantine table and tell the upstream team.

### 1.3 Why are data engineers in such demand?

1. **Data exploded.** Every click, search, payment, phone call and movie rating creates data.
2. **Businesses want data-driven decisions** instead of gut feeling.
3. **Someone has to organise it.** Raw data is basically garbage until it is transformed.
4. Demand is high, so jobs are plentiful and pay is high.

🌟 **Analogy: raw potato and salt.** If you walk into a restaurant and the waiter hands you a raw potato, a raw carrot and some salt and says “enjoy”, you *can* eat it, but it is very hard to digest. Raw data is the same: technically usable, practically painful. Clean, structured data is the plated meal.

```
  Amount of data  =  demand for data engineers
   ^                                         *
   |                                    *
   |                              *
   |                       *
   |               *
   |     *    *
   +--------------------------------------------> time
```

*Caption: data volume climbs steeply, and so does the need for people who can handle it.*

### 1.4 Why fundamentals matter

- Tools come and go (new ones appear every year). **Fundamentals stay the same.**
- The presenter says that roughly **50% of data engineering interview questions** come from fundamentals (OLTP/OLAP, ETL, modeling, SCD, lakes, and so on). Treat this as a rough guide, but it matches what interviews usually feel like.
- If your fundamentals are strong, learning any new tool takes days instead of months.

|  | Raw data | Curated data |
| --- | --- | --- |
| Quality | Messy, duplicates, typos | Clean, consistent |
| Relationships | None | Linked through keys |
| Who can use it easily | Almost nobody | Analysts, scientists, managers |
| Speed of reports | Slow and error-prone | Fast and trusted |

✅ **Checkpoint:** Can you explain data engineering in two sentences using the chef analogy?

### Interview Questions

**Q1. What is data engineering, in your own words?** **A:** It is the job of collecting data from different sources, cleaning and reshaping it, and delivering it in well-organised models so analysts, scientists and managers can trust it and use it for decisions. Think of a chef turning raw ingredients into plated dishes.

**Q2. Why can’t analysts simply work on raw data directly?** **A:** Raw data has duplicates, inconsistent formats, missing values and no relationships between sources. Every analyst would have to clean it separately, producing different answers. A data engineer cleans it once, centrally, so everyone gets one consistent version.

**Q3. Scenario: the sales dashboard shows three separate bars for “Mumbai”, “mumbai” and “MUMBAI”. What went wrong and how do you fix it?** **A:** The transformation step did not standardise text values. Fix it by trimming and upper-casing (or mapping to a reference list) in the transformation layer, re-run the pipeline, and add a data-quality check so inconsistent spellings are flagged in future.

**Q4. Scenario: total revenue in the dashboard is exactly double the finance team’s number. Where do you look first?** **A:** Duplicates. Check whether rows are loaded twice (a pipeline re-run without de-duplication, or a bad join that multiplies rows). Compare row counts and distinct key counts between source and target.

**Q5. Why is it said that data engineers spend 70–80% of their time on transformation?** **A:** Source data is almost never in the shape the business needs. Turning messy raw data into curated, reliable data is the core value a data engineer adds.

---

## 2. The Data Engineering Workflow: The Three Pillars

```
 +-------------------+      +-----------------------+      +------------------+
 | 1. DATA           | ---> | 2. DATA               | ---> | 3. DATA          |
 |    PRODUCTION     |      |    TRANSFORMATION     |      |    SERVING       |
 |  (data is born)   |      |  (cook the data)      |      |  (plate the data)|
 +-------------------+      +-----------------------+      +------------------+
   Source systems             ETL, cleaning, modeling        Data models,
   (apps, DBs, APIs)          (70-80% of your time)          reports, dashboards
```

*Caption: if anyone asks “what are the three pillars of data engineering?”, this is the answer.*

⚠️ The presenter briefly wrote “data transformation” as the third pillar by mistake and corrected it. The three pillars are **production, transformation, serving**.

### 2.1 Pillar 1: Data Production (data generation)

**Big idea:** Data is created whenever *anything* happens on a device or website. You, as the data engineer, usually do **not** create this data; you consume it.

🌟 **Everyday examples of data being produced**

- **Online shopping:** clicking an item, choosing quantity, picking an address, paying, getting a confirmation message, getting shipping details. *Each* step is a data record.
- **Streaming platform:** you search for a movie, watch it, rate it. All of it is stored.
- **Phone calls:** each call you dial appears later in your monthly bill. That is data.
- **Google searches:** even searching “what is data engineering” is data about you.

💡 **Simple English: API.** An API is a **connector between two software systems**. Your program asks the API for information and it brings the information back. 🌟 *Analogy:* an API is a **waiter**. You (a program) tell the waiter what you want, the waiter walks to the kitchen (the website’s system) and brings the food (data) back. You never enter the kitchen.

💡 **Simple English: web scraping.** Pulling information that is displayed on a website, usually with code.

All this data has to be **saved somewhere**, normally a database. As the data engineer you read from that storage.

```
   Person               App / Website                Database (storage)
  +------+  clicks    +----------------+  saved to  +-------------+
  | User | ---------> | Shop / OTT app | ---------> |  SOURCE DB  |
  +------+            +----------------+            +-------------+
                                                         |
                                         you (data engineer) read from here
```

*Caption: the user clicks, the app records it, the database stores it, and the data engineer reads it from the database.*

**Types of sources you will meet**

| Source type | What it holds | Examples |
| --- | --- | --- |
| **SQL / relational database** | **Structured** data in tables, with relationships between tables | PostgreSQL, MySQL, MS SQL Server, Oracle |
| **NoSQL database** (“not only SQL”) | **Unstructured or semi-structured** data that doesn’t fit neat rows and columns | MongoDB, Cassandra, Redis *(extra examples)* |
| **Files** | CSV, JSON, etc. | exports from apps |
| **APIs** | Data pulled from websites/apps | REST APIs |
| **Streams** | Continuous real-time data | IoT sensors, click streams |

💡 **Simple English: structured, semi-structured, unstructured**

- *Structured:* neat rows and columns, like an Excel sheet or SQL table.
- *Semi-structured:* has some organisation but not fixed columns, like JSON (a name-and-value text format).
- *Unstructured:* no fixed layout, like photos, videos, PDFs, free text.

⚠️ The presenter calls CSV and JSON “semi-structured”. Strictly speaking CSV is flat, table-like text and JSON is the truly semi-structured one. For interviews, just remember that **file-based data in a lake does not come with an enforced schema**.

**Who manages the source?** Usually a **DBA (database administrator)**, or a software/web developer in small companies. That is not you. This matters for the upstream/downstream idea in Section 3.

### 2.2 Pillar 2: Data Transformation

**Big idea:** This is where you turn **raw data into curated data**. It is the favourite part of the job, and the place you will spend around 70–80% of your time.

💡 **Simple English: curated data** = data that has been cleaned, organised and checked, so people can trust it.

Typical transformation jobs *(extra list, the video says the details come later)*:

- Removing duplicates and fixing typos
- Standardising formats (dates, currencies, city names)
- Handling missing values
- Joining tables together (customers + orders)
- Aggregating (daily totals, monthly averages)
- Reshaping into facts and dimensions (Section 8)

```
   RAW (messy)                          CURATED (clean)
 +----------------+   transformations  +------------------+
 | dup rows       |  ===============>  | unique rows      |
 | MUMBAI/mumbai  |  (clean, join,     | standard city    |
 | no links       |   reshape)         | linked tables    |
 +----------------+                    +------------------+
```

*Caption: before vs after transformation.*

### 2.3 Pillar 3: Data Serving (data modeling)

**Big idea:** Cooked data in one big container is still not usable. You must serve it in **small, purpose-built portions**. Those portions are **data models**.

🌟 **Analogy:** you cooked a huge pot of curry. You cannot say “here is the pot, help yourselves”. You serve a half plate to one customer, a full plate to another, and something extra to a third. Different customers (analyst, scientist, manager) need different plates.

```
   Big pot of cooked data                 Small plates (data models)
  +----------------------+            +-------------+  -> Sales dashboard (analyst)
  |  all transformed     |  ------->  | sales model |
  |  data together       |            +-------------+  -> Customer history (scientist)
  +----------------------+            | customer    |
                                      | model       |  -> Monthly KPIs (manager)
                                      +-------------+
```

*Caption: serving = shaping transformed data into models that match each user’s need.*

| Pillar | Kitchen version | Data version |
| --- | --- | --- |
| 1. Production | Farmers grow vegetables | Apps and users generate data |
| 2. Transformation | Chef cooks | Data engineer cleans and reshapes |
| 3. Serving | Plates go to customers | Data models feed dashboards and ML |

✅ **Checkpoint:** Name the three pillars and say which one you spend most of your time on.

### Interview Questions

**Q1. What are the three pillars of data engineering?** **A:** Data production (where data is generated and stored), data transformation (cleaning and reshaping raw data into curated data) and data serving (delivering it as data models to users).

**Q2. What is an API and why does a data engineer care?** **A:** An API is a connector that lets one system request data from another. Data engineers use APIs as a **source**, for example pulling weather, payment or social media data into a pipeline.

**Q3. SQL vs NoSQL: how do you decide?** **A:** SQL (relational) suits structured data with clear relationships, such as orders and customers. NoSQL suits flexible, semi-structured or unstructured data, such as JSON documents or key-value data. “NoSQL” means “not only SQL”, not “no SQL”.

**Q4. Scenario: a data scientist says every table has a different date format and she can’t combine them. Which pillar failed?** **A:** Transformation. Dates should have been standardised before serving. Fix it in the pipeline (convert all dates to one format such as YYYY-MM-DD) and document it.

**Q5. Scenario: the source app team adds a new column and your pipeline suddenly fails. Why, and how do you prevent it?** **A:** The pipeline expected a fixed set of columns (a schema). Prevent this with schema-change alerts, agreements with the upstream team (data contracts), and pipelines that handle new columns gracefully.

---

## 3. Upstream and Downstream

### 3.1 The idea

Imagine a river. Water flows in one direction. If you stand in the middle, whatever is **before** you is **upstream**, whatever is **after** you is **downstream**.

```
 UPSTREAM  ------------------>   YOU   ------------------>  DOWNSTREAM
 (data comes FROM them)    (data engineer)           (data goes TO them)

 DBAs                                                 Data analysts
 Software / web developers                            Data scientists
 Source systems (OLTP, CSV, API)                      Analytics managers
```

*Caption: data flows left to right. Requirements flow the other way, from downstream back to you.*

⚠️ **Not a rank:** downstream does **not** mean “lower in the company”. It only describes the direction the data flows.

🌟 **Analogy: a water-filtering plant.** The dam and the river are upstream. The treatment plant (you) cleans the water. Households that drink it are downstream. If the river is polluted or the households want softer water, the plant has to talk to both sides.

|  | Upstream | Downstream |
| --- | --- | --- |
| Who | DBAs, software developers, source owners | Analysts, scientists, analytics managers |
| What they give you | Raw data | Requirements (“what do we need?”) |
| What you give them | Requests for source changes | Clean, modeled data |
| Typical conversation | “Can you add the region column to the orders table?” | “I need weekly revenue by region.” |

### 3.2 Why you must keep both relationships healthy

1. **Requirements come from downstream.** You can’t build useful models if you don’t know how they will use the data.
2. **Data comes from upstream.** If a project needs a change in the source system, you must ask them nicely and agree on it.
3. You are responsible for **syncing both ends**. You need a basic understanding of how each side works, not deep detail.

**Worked example *(extra)*:**

1. A marketing manager (downstream) says: “I need revenue by region by week.”
2. You look at the source (upstream) and see the orders table has **no region column**.
3. You talk to the software team: “Can you add `region` to the orders table, or give me a customer-to-region mapping?”
4. They agree. You update the pipeline, build the model, serve it. The manager gets her report.

Without those conversations, you would guess region from addresses, get it wrong, and lose trust.

✅ **Checkpoint:** Who is upstream of you? Who is downstream? Which direction do requirements travel?

### Interview Questions

**Q1. Define upstream and downstream with an example.** **A:** Upstream is where your data comes from (for example the DBA or app team managing the OLTP database). Downstream is who consumes what you produce (analysts, data scientists, managers). Data flows upstream to downstream.

**Q2. Scenario: the upstream team renames the column `cust_id` to `customer_id` without telling you. Your nightly pipeline fails. What happened and how do you stop it happening again?** **A:** A schema change upstream broke a pipeline that expected the old name. Short term: update the mapping and re-run. Long term: agree on change notifications or data contracts, add schema validation checks, and set up monitoring and alerts so failures are visible quickly.

**Q3. Scenario: an analyst complains that last month’s revenue “looks wrong”. How do you investigate?** **A:** Trace backwards: compare dashboard numbers with the curated model, then with the staging data, then with the source. Check filters, joins, duplicates and late-arriving data. Confirm the business definition of “revenue” with the analyst. Fix the root cause and communicate the outcome.

**Q4. Why should a data engineer talk regularly to both upstream and downstream teams?** **A:** Downstream tells you what is needed, upstream controls what is available. Without both conversations you build the wrong thing or you break when sources change.

**Q5. Is a data analyst “below” a data engineer because they are downstream?** **A:** No. Upstream/downstream only describes the direction of data flow, not seniority.

---

## 4. OLTP vs OLAP: The Two Kinds of Databases

The presenter says this confused him for a long time. Both are called “databases”, but they are built for **opposite jobs**. Once you see that, everything else (ETL, warehouses, modeling) clicks.

### 4.1 Full forms

- **OLTP** = **O**n**l**ine **T**ransactional **P**rocessing
- **OLAP** = **O**n**l**ine **A**nalytical **P**rocessing

💡 **Simple English**

- **Transaction**: one recorded event, such as a payment, an order, a click, a bank transfer.
- **Transactional**: dealing with lots of small events, one at a time.
- **Analytical**: looking at a huge pile of data to find patterns and answers (“which region sold the most last quarter?”).

### 4.2 OLTP: the source database

**What it is:** the database an app or website writes into while people use it. Websites, blogs and OTT platforms all dump their data here. For you, it is the **source**.

**Key properties**

- Stores data as **transactions**, one after another. Think of a banking app: every transfer is written down immediately.
- Data arrives in **small chunks** (for example, 10 users just clicked, so add 10 rows).
- Built for **fast writes and updates**.
- Popular examples: **PostgreSQL, MySQL, MS SQL Server, Oracle**.
- Usually **managed by a DBA** (or a software developer in a small company). It is **not** your job to design it; you treat it as a source.
- Modeled with **relational modeling and normalization**.

🌟 **Analogy: the cashier at a busy supermarket.** The billing system must record each sale instantly, hundreds of times an hour. It is designed to *write quickly*, not to answer “how did we do in the last 3 years?”

#### Normalization in plain English

💡 **Simple English: normalization** = organising tables so that **the same fact is stored only once**. If a customer’s phone number lives in one place, changing it takes one update and nothing can disagree.

**Before normalization (one big table):**

| order\_id | customer\_name | customer\_phone | customer\_city | product | price |
| --- | --- | --- | --- | --- | --- |
| 1 | Aman | 99999 | Pune | Pen | 10 |
| 2 | Aman | 99999 | Pune | Book | 50 |
| 3 | Aman | 99999 | Pune | Bag | 700 |

If Aman changes his phone number you must edit **three** rows. Miss one and your data contradicts itself.

**After normalization (two linked tables):**

`customers`

| customer\_id | name | phone | city |
| --- | --- | --- | --- |
| 1 | Aman | 99999 | Pune |

`orders`

| order\_id | customer\_id | product | price |
| --- | --- | --- | --- |
| 1 | 1 | Pen | 10 |
| 2 | 1 | Book | 50 |
| 3 | 1 | Bag | 700 |

One phone number, one place, linked by `customer_id`.

**Normal forms (1NF, 2NF, 3NF)** *(extra explanation)*

| Form | Simple rule |
| --- | --- |
| **1NF** | One value per cell, no repeating groups (no “Pen, Book, Bag” crammed into one cell) |
| **2NF** | Every non-key column depends on the *whole* key |
| **3NF** | Non-key columns depend only on the key, not on other non-key columns |

- There are 4th, 5th and 6th normal forms, but they are hard to manage, so real systems stop at **3NF**.
- As a data engineer you only need the basics. The DBA builds this; you just need to understand it enough to join tables correctly.

### 4.3 OLAP: the data warehouse

**What it is:** a database designed so that **reading and analysing** huge amounts of data is fast. **An OLAP database is a data warehouse.**

**Why do we even need it? (the presenter’s story)**

1. The OLTP database receives data every second, every millisecond. It becomes **huge**.
2. If reports query that giant, busy database directly, the reports are painfully slow (the presenter jokes the reports would be “dying”).
3. Those heavy reports would also slow down the live app.
4. Solution: build a **separate database** that holds a cleaned copy of the data, organised for reading. Reports query *that* instead.

**Key properties**

- Optimised for **fast reads** and large queries.
- Modeled with **dimensional modeling** (facts and dimensions), not normalization. Covered in Section 8.
- **You, the data engineer, own it.** If something breaks here, it is your responsibility.
- Popular tools: **Snowflake, Azure Synapse, Amazon Redshift, Google BigQuery** (cloud), plus on-premise tools such as **Teradata** *(the caption says “wcape red”; verify)*.

🌟 **Analogy: the cashier’s notebook vs the accountant’s yearly summary.** The shop keeps a messy running notebook of every sale (OLTP). At the end of each week the accountant makes a tidy summary book (OLAP) so the owner can answer questions in two minutes instead of reading 10,000 notebook lines.

```
  Website / OTT app / Blog
          |  writes: many small transactions
          v
  +----------------+     ETL pipeline      +--------------------+
  | OLTP DATABASE  | --------------------> | OLAP DATABASE      |
  | (the SOURCE)   |  extract, transform,  | (DATA WAREHOUSE)   |
  | managed by DBA |  load                 | managed by YOU     |
  | fast WRITES    |                       | fast READS         |
  +----------------+                       +--------------------+
                                                     |
                                              Reports, dashboards
```

*Caption: OLTP is the source; OLAP is the analytics copy that reports read from.*

### 4.4 Side-by-side comparison

|  | **OLTP** | **OLAP (data warehouse)** |
| --- | --- | --- |
| Full form | Online Transactional Processing | Online Analytical Processing |
| Main job | Record day-to-day transactions | Analyse large volumes of data |
| Optimised for | **Writes and updates** | **Reads (queries)** |
| Data per operation | Small (a few rows) | Huge (millions of rows) |
| Managed by | DBA / software developer | **Data engineer** |
| Modeling technique | Normalization (1NF, 2NF, 3NF) | **Dimensional modeling** (facts and dimensions) |
| Examples | PostgreSQL, MySQL, SQL Server, Oracle | Snowflake, Synapse, Redshift, BigQuery |
| Role for you | **Source** | **Target** you build |
| Everyday analogy | Cashier’s notebook | Accountant’s summary book |

**Two queries that show the difference** *(extra)*

```sql
-- OLTP style: touch ONE row, very fast, happens thousands of times a minute
UPDATE accounts SET balance = balance - 500 WHERE account_id = 42;

-- OLAP style: scan MILLIONS of rows and summarise
SELECT region, SUM(amount) AS total_sales
FROM   fact_sales
GROUP  BY region;
```

⚠️ **Common mistake:** running heavy analytical reports directly on the OLTP database. It slows down the live app for real customers.

✅ **Checkpoint:** Fill in the blanks. OLTP is for \_\_\_\_ and updates and is a \_\_\_\_ for you. OLAP is for \_\_\_\_ and is built by \_\_\_\_.

### Interview Questions

**Q1. What is the difference between OLTP and OLAP?** **A:** OLTP systems record day-to-day transactions and are optimised for fast writes and updates (PostgreSQL, MySQL). OLAP systems, i.e. data warehouses, hold analysis-ready data and are optimised for fast reads over large volumes (Snowflake, Synapse). OLTP is normalised; OLAP uses dimensional modeling.

**Q2. Why shouldn’t we run reports directly on the OLTP database?** **A:** It is large, busy and designed for writes. Heavy analytical queries would be slow and would also slow the live application. A separate warehouse isolates reporting load.

**Q3. Who manages the OLTP database and who manages the data warehouse?** **A:** The OLTP database is usually managed by a DBA or application developers; the data warehouse is the data engineer’s responsibility.

**Q4. Scenario: reports take 20 minutes to run on the production database, and the shop’s app becomes sluggish at lunch time. What do you recommend?** **A:** Build a data warehouse. Use an ETL pipeline (scheduled off-peak) to copy data from the OLTP source, model it dimensionally, and point reports at the warehouse. Production then only handles app traffic.

**Q5. Why do we normalise OLTP tables, and why only up to 3NF?** **A:** Normalisation avoids duplicate facts and update errors, which is vital when data is constantly written. Beyond 3NF the design becomes hard to manage with little practical benefit, so 3NF is the usual stopping point.

---

## 5. ETL and Data Pipelines

### 5.1 What is ETL?

**ETL = Extract, Transform, Load.** It is *the process* that gets data from the OLTP source into the OLAP warehouse. It is not magic and there is no “create warehouse” button.

| Letter | Step | Simple meaning | Example |
| --- | --- | --- | --- |
| **E** | Extract | Copy data **out of** the source | Read yesterday’s orders from PostgreSQL |
| **T** | Transform | Clean, fix, join, reshape | Remove duplicates, standardise cities, calculate revenue |
| **L** | Load | Write into the target | Insert into the warehouse fact and dimension tables |

```
   SOURCE (OLTP)            YOUR LOGIC                 TARGET (OLAP)
  +-------------+  E   +------------------+    L    +----------------+
  | PostgreSQL  | ---> | clean, join,     | -------> | Data warehouse |
  | MySQL, API  |      | reshape (T)      |          | facts + dims   |
  +-------------+      +------------------+          +----------------+
```

*Caption: ETL moves data from source to warehouse, improving it on the way.*

### 5.2 Why do we need pipelines?

You build the warehouse once. But the source keeps changing every hour. Would you repeat the whole thing by hand every day? No. You build an **ETL pipeline** (also called a **data pipeline**) that runs by itself.

🌟 **Analogy: water pipelines.** A big tank is far from your house. You do not carry buckets from the tank every morning. You open the tap and water arrives, because pipes already connect the tank to your home. A data pipeline is the same: once built, data flows from source to warehouse without manual effort.

|  | Manual work | Pipeline |
| --- | --- | --- |
| Run by | A person, each time | A scheduler or trigger |
| Frequency | When someone remembers | Every hour, every night, etc. |
| Risk of mistakes | High | Low (same logic every time) |
| Scales to many tables | Painful | Easy |

**A tiny pipeline in code** *(extra, pseudo-code to show the shape)*

```python
def extract():
    # E: read the new rows from the source database
    return read_sql('SELECT * FROM orders WHERE order_date > last_loaded_date')

def transform(df):
    # T: clean and reshape
    df = df.drop_duplicates()
    df['city'] = df['city'].str.strip().str.upper()
    df['revenue'] = df['qty'] * df['price']
    return df

def load(df):
    # L: write to the warehouse
    write_to_warehouse(df, table='fact_orders')

# A scheduler (Airflow, Azure Data Factory, cron) runs this every hour:
load(transform(extract()))
```

💡 **Simple English: ETL vs ELT** *(extra, a popular follow-up question)*. In **ETL** you transform *before* loading. In **ELT** you load the raw data first (into a lake or cloud warehouse) and transform it *afterwards* using the target’s power. The medallion architecture in Section 15 is ELT-flavoured.

✅ **Checkpoint:** Say E, T and L out loud with one example each.

### Interview Questions

**Q1. What is ETL?** **A:** Extract data from sources, transform it (clean, join, aggregate, reshape) and load it into a target such as a data warehouse, usually automated through pipelines.

**Q2. Why do we build pipelines instead of running ETL manually?** **A:** Sources keep changing. Pipelines automate the process on a schedule, give consistent logic, reduce human error and scale to many tables.

**Q3. Scenario: your nightly pipeline accidentally ran twice and revenue doubled. What happened and how do you prevent it?** **A:** The load was not **idempotent** (safe to re-run). Prevent it with upserts or truncate-and-reload of staging, de-duplication on business keys, and checks that compare row counts or totals after each run.

**Q4. Scenario: the transform step fails at 2 AM. How do you handle it?** **A:** Pipelines should have logging, alerts and retries. Investigate the error log, fix the cause (bad data, schema change, resource issue), and re-run from the failed step instead of the whole pipeline if possible.

**Q5. What is the difference between ETL and ELT?** **A:** ETL transforms before loading into the target. ELT loads raw data first and transforms inside the target (a lake or cloud warehouse), which suits big data and cheap storage.

---

## 6. Data Warehouse Layers: Staging and Core

### 6.1 The two layers

When you pull data from the source, it does **not** go straight into the finished warehouse. It travels through **layers**.

💡 **Simple English: layer** = think of it as a **folder** (a zone) where data lives at a certain stage of cleaning.

```
  SOURCE                STAGING LAYER                 CORE LAYER
  (OLTP DB)             (landing folder)              (final warehouse)
 +----------+  extract +----------------+ transform  +----------------------+
 | orders   | -------> | stg_orders     | ---------> | fact_orders          |
 | customers|          | stg_customers  |            | dim_customer         |
 +----------+          | (raw copy)     |            | dim_product          |
                       +----------------+            | (dimensional model)  |
                                                     +----------------------+
```

*Caption: source to staging to core. Staging is the raw landing area; core holds the facts and dimensions.*

- **Staging layer**: you first **extract** (copy) data here. It is a raw copy of what the source had.
- **Core layer**: you **transform** the staged data and store it as a **dimensional data model** (facts and dimensions).

🌟 **Analogy: a grocery delivery.** Boxes arrive at the shop’s **receiving area** (staging). Staff check, unpack and sort them, then place them neatly on **shelves** (core). Customers never shop from the delivery boxes.

### 6.2 Why do we need a staging layer? (classic interview question)

You should **not query the source system directly again and again** during transformation because:

1. It can **slow down the production database** (which real users depend on).
2. You get one stable copy to work with, even if the source changes while you transform.
3. If a transformation fails, you can **re-run it from staging** without hitting the source again. *(extra)*
4. It makes debugging easier because you can compare staging vs core. *(extra)*

### 6.3 Transient vs persistent staging

|  | **Transient staging** | **Persistent staging** |
| --- | --- | --- |
| Meaning | **Temporary.** Data is deleted (truncated) after use | **Permanent.** Data is kept, history preserved |
| What happens next day | Staging is emptied, new data is loaded | New data is added or updated; old stays |
| Storage use | Low | Grows over time |
| How common | **About 99% of real projects** | Rare; project-specific |
| Use when | You only need the latest increment | You must keep the raw history in the warehouse itself |

```
  TRANSIENT STAGING (daily cycle)

  Day 1:  Source --> [Staging: Day 1 data] --> Core (adds Day 1)   then staging is TRUNCATED
  Day 2:  Source --> [Staging: Day 2 data] --> Core (adds Day 2)   then staging is TRUNCATED
  Day 3:  Source --> [Staging: Day 3 data] --> Core (adds Day 3)   ...

  Core keeps growing. Staging is always empty between runs.
```

*Caption: with transient staging, staging is a temporary waiting room; core is the permanent home.*

🌟 **Analogy:** transient staging is a **whiteboard** you wipe clean every day; persistent staging is a **notebook** where you keep every page.

⚠️ **Common mistake:** forgetting to truncate a transient staging table. Yesterday’s rows get loaded into core again and your numbers double.

✅ **Checkpoint:** Which type do you use 99% of the time, and why?

### Interview Questions

**Q1. What are the layers in a data warehouse?** **A:** At least a staging layer (raw landing copy of source data) and a core layer (cleaned, modeled facts and dimensions that reports use).

**Q2. Why do we use a staging layer instead of loading directly into the core layer?** **A:** To avoid repeatedly querying and slowing the source, to work on a stable copy, to enable re-runs and debugging, and to keep raw landing separate from modeled data.

**Q3. Transient vs persistent staging?** **A:** Transient staging is truncated after each load, so it only holds the current batch (used about 99% of the time). Persistent staging retains history over time and is used only when a project needs it.

**Q4. Scenario: after a failed load you notice staging contains yesterday’s and today’s data and core now has duplicate records. What went wrong?** **A:** The transient staging table was not truncated before today’s load. Fix: truncate staging at the start of each run, de-duplicate core using business keys, and add a check that compares staging row counts with loaded rows.

**Q5. Scenario: the business wants to re-process raw data from three months ago after a bug was found in the transformation. Does transient staging help?** **A:** Not by itself, since it is wiped each run. You would need persistent staging or a raw/bronze layer in a data lake (Section 15) that retains the raw history.

---

## 7. Incremental Loading

### 7.1 The idea

💡 **Simple English: incremental loading** = loading **only the new (or changed) data** since the last run, instead of reloading everything.

🌟 **Analogy: copying a diary.** You keep a backup of your friend’s diary. Each day you could re-copy the whole diary (365 pages). Or you could copy **only today’s new page**. The second way is incremental loading.

**The presenter’s example**

1. The source holds data from **Jan 2023 to Jan 1, 2024**. You load all of it into staging, then core. This first big load is called the **full load** or **initial load**.
2. Next day, the source has one more day: **Jan 2, 2024**.
3. Do you pull all of Jan 2023 to Jan 2024 again? **No.** That wastes computation.
4. You load **only Jan 2, 2024** into staging, then into core. Core now has data up to Jan 2.
5. The cycle repeats every day.

```
 SOURCE (all history)                STAGING (transient)           CORE (growing)

 Day 1 (initial load)
 [Jan 2023 ... Jan 1 2024] ------> [Jan 2023 ... Jan 1 2024] --> [Jan 2023 ... Jan 1 2024]

 Day 2 (incremental)
 [Jan 2023 ... Jan 2 2024]  ------> [ Jan 2 2024 only ]       --> [Jan 2023 ... Jan 2 2024]
  ^ old part is skipped              ^ small, fast                 ^ only the new day was added

 Day 3 (incremental)
 [... Jan 3 2024]           ------> [ Jan 3 2024 only ]       --> [... Jan 3 2024]
```

*Caption: after the first full load, each run moves only the new slice of data.*

### 7.2 How do you actually know what is new? *(extra: the “watermark” technique)*

You remember **how far you have already loaded**, then ask the source for anything after that point.

```sql
-- A tiny control table remembers the high-water mark (how far we have loaded)
CREATE TABLE etl_control (
    table_name        VARCHAR(50),
    last_loaded_date  DATE
);

-- Step 1: read the watermark
SELECT last_loaded_date FROM etl_control WHERE table_name = 'orders';   -- e.g. 2024-01-01

-- Step 2: extract only newer rows from the source into staging
INSERT INTO staging.orders
SELECT * FROM source.orders
WHERE  order_date > '2024-01-01';

-- Step 3: after core is loaded successfully, move the watermark forward
UPDATE etl_control SET last_loaded_date = '2024-01-02' WHERE table_name = 'orders';
```

⚠️ **Gotchas to know for interviews** *(extra)*

- **Updates and deletes:** a date filter finds *new* rows but not *changed* old ones. Use a `last_modified` column or Change Data Capture (CDC) to catch updates and deletes.
- **Late-arriving data:** a row dated Jan 1 that reaches the source on Jan 3 could be missed. Many teams re-pull a small overlap window and de-duplicate.
- **Move the watermark only after success.** Otherwise a failed run causes missing data.

|  | **Full load** | **Incremental load** |
| --- | --- | --- |
| Data moved each run | Everything, every time | Only new or changed data |
| Time and compute cost | High | Low |
| Complexity | Simple | Needs watermark logic |
| Best for | First load, small tables, rebuilds | Large, growing tables (the industry norm) |

The presenter stresses: this is the practice followed in data engineering, we **do not pull all the data again and again**. It is also a favourite interview question.

✅ **Checkpoint:** Explain the Jan 2023 to Jan 2, 2024 example in your own words, including what happens to staging.

### Interview Questions

**Q1. What is incremental loading and why use it?** **A:** It loads only data that is new or changed since the previous run. It saves time, compute and cost compared with reloading everything, and it scales as data grows.

**Q2. How would you implement incremental loading?** **A:** Store a watermark (last loaded timestamp or ID) in a control table. Each run extracts rows beyond the watermark into staging, loads them into core, and updates the watermark only after a successful load.

**Q3. Scenario: existing orders in the source get edited (status changes from “placed” to “shipped”). A date filter on `order_date` doesn’t see these. What do you do?** **A:** Filter on a `last_modified` timestamp instead, or use CDC. Then upsert the changed rows into core so existing records are updated rather than duplicated.

**Q4. Scenario: the pipeline failed after staging loaded but before core loaded. How do you avoid losing data on the next run?** **A:** Only advance the watermark after core loads successfully, and make the load idempotent (upsert or de-duplicate), so re-running the same increment is safe.

**Q5. Scenario: this is the very first run and the core table is empty. What do you load?** **A:** A full (initial) load of all history. Incremental runs start afterwards using the watermark from the full load.

---

## 8. Dimensional Modeling: Facts, Dimensions, Star and Snowflake

### 8.1 The big idea

In OLTP you organise tables with **normalization** (1NF, 2NF, 3NF). In an OLAP data warehouse you use a different technique: **dimensional modeling**. You store data as **one fact table in the middle, with dimension tables linked to it**.

🌟 **Analogy: a shopkeeper’s diary plus an address book and a catalogue.**

- The **diary line** says: *Customer 5 bought Product 12, quantity 2, total 600.* It is full of **numbers and IDs**. This is the **fact table**.
- The **address book** explains who “Customer 5” is (name, city, phone). This is a **customer dimension**.
- The **catalogue** explains what “Product 12” is (name, category). This is a **product dimension**.

The diary stays short and fast to add up. The books give meaning to the IDs.

### 8.2 The rules: what goes where?

|  | **Fact table** | **Dimension table** |
| --- | --- | --- |
| Holds | **Numeric measurements** (the things you add up or average) plus keys that point to dimensions | **Descriptive, categorised, non-numeric context** (names, categories, addresses) |
| Examples | price, bill amount, MRP, quantity, weight | customer name, address, product name, product category |
| Question it answers | **How much? How many?** | **Who? What? Where? When?** |
| Size | Very tall (millions or billions of rows) | Usually much smaller |
| How many | **One** per model (in the simple case) | **Several**, one per business concept |

💡 **Simple English**

- **Measure**: a number you calculate with (quantity, revenue).
- **Key (ID)**: a column that identifies a row, or links to another table.
- **Dimension**: a table of descriptions you use to slice and filter the numbers (“revenue **by** city, **by** product category”).
- **Denormalized**: the opposite of normalized. Some repeated data is accepted so queries need fewer joins.

**How to build dimensions:** group columns by business concept. All customer details go together into a **customer dimension** (`dim_customer`). All product details go together into a **product dimension** (`dim_product`). If the same description appears many times, you still keep it once in the dimension. The presenter calls the result “semi-normalized” or clustered by business use case.

⚠️ **Nuance** *(extra)*: “fact = numbers” really means **numeric measures you aggregate**. A number like `customer_age` is numeric but descriptive, so it belongs in a dimension. IDs are numeric but are keys, not measures.

### 8.3 Worked example: from a flat table to a dimensional model *(extra)*

**One flat table from a sales app:**

| order\_id | cust\_id | cust\_name | cust\_city | prod\_id | prod\_name | prod\_category | qty | amount |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 | Aman | Pune | 1 | Honey | Food | 2 | 600 |
| 2 | 11 | Riya | Delhi | 2 | Shirt | Clothing | 1 | 450 |
| 3 | 10 | Aman | Pune | 2 | Shirt | Clothing | 3 | 1350 |

**Split it:**

`fact_sales` (numbers and keys)

| order\_id | customer\_key | product\_key | qty | amount |
| --- | --- | --- | --- | --- |
| 1 | 10 | 1 | 2 | 600 |
| 2 | 11 | 2 | 1 | 450 |
| 3 | 10 | 2 | 3 | 1350 |

`dim_customer` (descriptions)

| customer\_key | name | city |
| --- | --- | --- |
| 10 | Aman | Pune |
| 11 | Riya | Delhi |

`dim_product` (descriptions)

| product\_key | name | category |
| --- | --- | --- |
| 1 | Honey | Food |
| 2 | Shirt | Clothing |

```sql
-- A typical warehouse question: revenue by city and product category
SELECT  c.city,
        p.category,
        SUM(f.amount) AS revenue
FROM    fact_sales   f
JOIN    dim_customer c ON f.customer_key = c.customer_key
JOIN    dim_product  p ON f.product_key  = p.product_key
GROUP BY c.city, p.category;
```

### 8.4 Star schema

A **star schema** has one fact table in the **centre** and each dimension attached **directly** to it. Drawn out, the shape looks like a star, hence the name.

```
                      +----------------+
                      |  dim_customer  |
                      +-------+--------+
                              |
  +----------------+   +------+-------------+   +----------------+
  |  dim_product   +---+    FACT_SALES      +---+    dim_date    |
  +----------------+   |  customer_key (FK) |   +----------------+
                       |  product_key  (FK) |
                       |  date_key     (FK) |
                       |  quantity          |
                       |  amount            |
                       +------+-------------+
                              |
                      +-------+--------+
                      |   dim_store    |
                      +----------------+
```

*Caption: star schema. Every dimension is one hop away from the fact table.*

💡 **FK** = **foreign key**, a column that points to the ID of a row in another table.

### 8.5 Snowflake schema

A **snowflake schema** is the same idea, with one difference: **dimensions are linked to other dimensions** (a hierarchy). The whole chain eventually connects to the fact table. Drawn out, the branches look like a snowflake.

```
  dim_department
        |
  dim_category
        |
  dim_product -----> FACT_SALES <----- dim_customer -----> dim_city -----> dim_country
  (dimension)                          (dimension)         (sub-dimension)  (sub-sub-dim)
```

*Caption: snowflake schema. Dimensions branch into sub-dimensions, so a query needs more joins to reach the details.*

|  | **Star schema** | **Snowflake schema** |
| --- | --- | --- |
| Shape | Fact in centre, dimensions directly around it | Dimensions linked to other dimensions (hierarchy) |
| Joins needed | Fewer | More |
| Query speed | **Faster (performant)** | Slower |
| Ease of management | **Easy** | Harder |
| Repeated data | Some repeated values in dimensions | Less repetition (more normalized) |
| Used in practice | **About 99% of the time** | Rare, but you should know it |

⚠️ Don’t confuse **snowflake schema** (a design shape) with **Snowflake** (the cloud data warehouse product mentioned in Section 4). They are different things that share a name.

✅ **Checkpoint:** Draw a star schema from memory with one fact and three dimensions. Then draw how it changes into a snowflake.

### Interview Questions

**Q1. What is dimensional modeling?** **A:** A warehouse modeling technique where data is stored as a central fact table of numeric measures linked to surrounding dimension tables of descriptive attributes. It is designed for fast, easy reporting, unlike normalization, which is designed for fast writes.

**Q2. What is the difference between a fact table and a dimension table?** **A:** Fact tables hold measures (quantity, price, amount) and keys; they are tall and answer “how much?”. Dimension tables hold descriptive context (customer, product, date) and answer “who, what, where, when?”.

**Q3. Star schema vs snowflake schema: which do you choose and why?** **A:** Star in nearly all cases, since it needs fewer joins, queries faster and is easier to maintain. Snowflake normalises dimensions into hierarchies, saving some repetition at the cost of more joins and complexity.

**Q4. Scenario: you inherit a snowflake schema where dashboards are slow because every query joins six tables. What would you do?** **A:** Flatten (denormalise) the dimension hierarchies into single dimensions, turning it into a star schema, so each query joins the fact table with just one hop per dimension. Check that indexes or partitioning on the fact table are sensible too.

**Q5. Scenario: a flat table has `order_amount`, `customer_name`, `product_category`, `discount_percent` and `customer_age`. Classify each.** **A:** `order_amount` is a fact (measure). `customer_name` goes to the customer dimension, `product_category` to the product dimension. `customer_age` is numeric but descriptive, so it belongs in the customer dimension. `discount_percent` depends: if it is a per-transaction value you aggregate or analyse, store it as a fact; if it is a fixed attribute of a promotion, put it in a promotion dimension.

**Q6. What does “grain” of a fact table mean?** *(extra)* **A:** The level of detail of one row, for example “one row per order line per day”. Deciding the grain first prevents double counting later.

---

## 9. Slowly Changing Dimensions (SCD)

The presenter ranks this in his **top three most important topics**, because you use it in almost every project.

### 9.1 The problem

Dimensions hold descriptive data, and descriptive data **changes slowly over time**: a customer moves city, a product is moved to a different category, an employee gets promoted. When the source changes, the dimension must reflect it. But *how* to reflect it is a design choice. That choice is the **SCD type**.

💡 **Simple English: SCD** = **S**lowly **C**hanging **D**imension = a dimension whose values change occasionally, plus the rule for how you record each change.

**The presenter’s running example: `dim_product`**

| product\_id | name | category |
| --- | --- | --- |
| 1 | Honey | Food |
| 2 | Shirt | Clothing |
| 3 | Comb | Clothing |

*(The transcript says “com”, which is most likely “comb”.)*

**The change in the source:** product 3 (Comb) is no longer “Clothing”. Its category becomes **Hair Accessories**. How should the dimension handle this? There are four common answers, Types 0, 1, 2 and 3. (Types 4 and 6 exist but the presenter says we don’t deal with them.)

### 9.2 Type 0: never change

The dimension is **fixed**. Once a value is stored, it is never updated. It is called Type 0 because it is basically “not a type”.

🌟 **Analogy:** your **birth certificate**. Even if the information later turns out to be wrong in real life, the original record is kept as it is.

*Use for:* attributes that truly never change, such as date of birth or original sign-up date *(extra examples)*.

### 9.3 Type 1: overwrite (also called UPSERT)

**Rule:** replace the old value with the new value. **No history is kept.**

💡 **Simple English: UPSERT** = **UP**date + in**SERT**.

- If the record already exists, **update** it.
- If the record is new, **insert** it.

🌟 **Analogy:** editing a **phone contact**. When your friend changes number you overwrite the old one. The old number is gone.

**Before**

| product\_id | name | category |
| --- | --- | --- |
| 1 | Honey | Food |
| 2 | Shirt | Clothing |
| 3 | Comb | Clothing |

**After Type 1** (Comb overwritten, and a brand-new product 4 inserted)

| product\_id | name | category |
| --- | --- | --- |
| 1 | Honey | Food |
| 2 | Shirt | Clothing |
| 3 | Comb | **Hair Accessories** |
| 4 | Shoes | Footwear |

**What the UPSERT does behind the scenes**

1. For product 4: “Do I have product 4?” No, so **INSERT**.
2. For product 3: “Do I have product 3?” Yes, so **UPDATE** it.
3. Products 1 and 2 are also “updated”, but with values identical to what they already had, so you never notice any change.

```sql
-- Type 1 as a MERGE statement (works in SQL Server, Snowflake, Synapse, Databricks/Delta)
MERGE INTO dim_product AS t
USING stg_product AS s                 -- s = the incoming data from staging
   ON t.product_id = s.product_id      -- how we decide “same product”
WHEN MATCHED THEN                      -- exists already -> UPDATE (overwrite)
     UPDATE SET t.name = s.name,
                t.category = s.category
WHEN NOT MATCHED THEN                  -- new product -> INSERT
     INSERT (product_id, name, category)
     VALUES (s.product_id, s.name, s.category);
```

**Pros:** simple, easy to manage, performant; the presenter says it is used roughly **70–80% of the time**. **Cons:** **history is lost.**

⚠️ **Hidden trap** *(extra)*: with Type 1, last year’s sales of the Comb are now reported under “Hair Accessories”, even though back then it was classified as “Clothing”. If the business needs old reports to stay as they were, Type 1 is the wrong choice.

🎯 **Interview trick:** if an interviewer says **“upsert”**, they mean **Type 1**.

### 9.4 Type 2: keep full history by adding rows

**Rule:** never overwrite. When a value changes, **expire the old row and insert a new row**. You can see every version and the dates it was valid. This is rarer than Type 1 but important.

🌟 **Analogy:** an **HR job-history record**. “Priya: Analyst, 2020 to 2022. Senior Analyst, 2022 to now.” Both rows stay, each with its dates.

**What you add to the dimension:** three extra columns.

| New column | Meaning |
| --- | --- |
| `start_date` | When this version became valid |
| `expiry_date` | When it stopped being valid. For a still-current row, use a very distant date (the presenter uses year **3000**; many teams use 9999-12-31) |
| `is_current` (in-use flag) | Y if this is the version in use right now, N if it is old |

**Before the change** (every row current since 1 Jan 2024)

| product\_key | product\_id | name | category | start\_date | expiry\_date | is\_current |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | Honey | Food | 2024-01-01 | 3000-01-01 | Y |
| 2 | 2 | Shirt | Clothing | 2024-01-01 | 3000-01-01 | Y |
| 3 | 3 | Comb | Clothing | 2024-01-01 | 3000-01-01 | Y |

**After the change on 2 Jan 2024**

| product\_key | product\_id | name | category | start\_date | expiry\_date | is\_current |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | Honey | Food | 2024-01-01 | 3000-01-01 | Y |
| 2 | 2 | Shirt | Clothing | 2024-01-01 | 3000-01-01 | Y |
| 3 | 3 | Comb | Clothing | 2024-01-01 | **2024-01-02** | **N** |
| **4** | 3 | Comb | **Hair Accessories** | **2024-01-02** | 3000-01-01 | **Y** |

The old row is closed (expiry date set, flag set to N). A **new row** is inserted for the new truth.

```sql
-- Type 2, step 1: close the old version
UPDATE dim_product
SET    expiry_date = '2024-01-02',
       is_current  = 'N'
WHERE  product_id = 3
  AND  is_current = 'Y';

-- Type 2, step 2: insert the new version as a NEW row (new surrogate key = 4)
INSERT INTO dim_product
       (product_key, product_id, name, category,           start_date,   expiry_date,  is_current)
VALUES (4,           3,          'Comb', 'Hair Accessories', '2024-01-02', '3000-01-01', 'Y');

-- Reading the data:
SELECT * FROM dim_product WHERE is_current = 'Y';                        -- today’s truth only
SELECT * FROM dim_product
WHERE  product_id = 3 AND '2023-06-15' >= start_date AND '2023-06-15' < expiry_date;  -- truth on a past date
```

💡 **Simple English: surrogate key** *(extra, essential for Type 2)*. `product_id` (the source’s own ID, also called the **business key**) now repeats, because product 3 has two rows. So the warehouse creates its own unique ID, `product_key`. Each fact row points to the **version** that was true when the sale happened. That is how old sales stay linked to “Clothing” while new sales link to “Hair Accessories”.

**Pros:** full history, fully accurate old reports. **Cons:** more rows, more complex loading logic, more joins to filter versions.

### 9.5 Type 3: keep only the previous value in an extra column

**Rule:** add a column for the **previous value**. You get the current and the one before, but no dates and no longer timeline.

🌟 **Analogy:** a messaging app showing your friend’s **“new number” and “old number”** side by side. Two numbers only. If they change number a third time, the oldest one drops off.

**Before**

| product\_id | name | current\_category | previous\_category |
| --- | --- | --- | --- |
| 1 | Honey | Food | Food |
| 2 | Shirt | Clothing | Clothing |
| 3 | Comb | Clothing | Clothing |

**After the change**

| product\_id | name | current\_category | previous\_category |
| --- | --- | --- | --- |
| 1 | Honey | Food | Food |
| 2 | Shirt | Clothing | Clothing |
| 3 | Comb | **Hair Accessories** | **Clothing** |

Unchanged rows keep the same value in both columns (some teams use NULL instead).

```sql
-- Type 3: shift the old value into the “previous” column, then write the new value
UPDATE dim_product
SET    previous_category = current_category,
       current_category  = 'Hair Accessories'
WHERE  product_id = 3;
```

**Pros:** performant, no date columns to manage, keeps one level of history. **Cons:** only **one** previous value; a second change erases the original.

### 9.6 All four types side by side

|  | **Type 0** | **Type 1** | **Type 2** | **Type 3** |
| --- | --- | --- | --- | --- |
| What happens on change | Nothing, value stays fixed | **Overwrite** (upsert) | **Insert a new row**, expire the old one | Move old value to a “previous” column, overwrite current |
| History kept? | Original only | **No** | **Full history** | **One** previous value |
| Extra columns | None | None | start\_date, expiry\_date, is\_current | previous\_value |
| Complexity | Lowest | Low | **Highest** | Low |
| Everyday analogy | Birth certificate | Edit a phone contact | HR job-history | New number + old number |
| Interview keyword | “fixed” | **“upsert”, “overwrite”** | **“keep history”** | “keep previous value” |
| Typical usage | Rare, for fixed attributes | **Most common (70–80%)** | When history matters | Rare |

```
  Does the attribute ever change?
     |
     +-- No  --> TYPE 0
     |
     +-- Yes --> Do we need old values at all?
                    |
                    +-- No  --> TYPE 1  (overwrite / upsert)
                    |
                    +-- Yes --> Do we need the full timeline?
                                   |
                                   +-- Yes --------------> TYPE 2 (new row per version)
                                   +-- Only the last one -> TYPE 3 (previous-value column)
```

*Caption: a quick decision guide for choosing an SCD type.*

✅ **Checkpoint:** Without looking, say what each type does to the Comb row, and name the interview keyword for each.

### Interview Questions

**Q1. What is a slowly changing dimension, and what are the types?** **A:** A dimension whose attribute values change occasionally. The types define how changes are recorded: Type 0 retains the original (no change), Type 1 overwrites (upsert, no history), Type 2 adds a new row with start date, expiry date and current flag (full history), Type 3 adds a column for the previous value (limited history).

**Q2. Which SCD type is meant by “upsert”?** **A:** Type 1. If the record exists it is updated (overwritten), otherwise it is inserted.

**Q3. Scenario: a customer moves from Delhi to Pune. Finance insists that last year’s sales must still appear under Delhi. Which type do you use?** **A:** Type 2. Expire the Delhi version and insert a Pune version. Sales facts keep pointing at the version that was current at the time, so last year’s sales stay in Delhi.

**Q4. Scenario: you implemented Type 1 and an analyst says last year’s “Clothing” sales dropped when the Comb moved to Hair Accessories. Explain.** **A:** Type 1 overwrites history, so all facts linked to product 3, including old ones, now show the new category. To preserve the original classification, change the dimension to Type 2 and re-link facts to the correct versions.

**Q5. In a Type 2 dimension, how do you fetch only today’s records, and the records as they were on a past date?** **A:** For today, filter `is_current = 'Y'` (or expiry\_date = the far-future date). For a past date, filter rows where the date falls between start\_date and expiry\_date.

**Q6. Why do you need surrogate keys with Type 2?** **A:** The business key repeats across versions of the same entity. A surrogate key uniquely identifies each version, so facts can link to the exact version that was valid when the event occurred.

**Q7. Scenario: your Type 2 pipeline creates a new version of every customer every night, even though nothing changed. What is the likely bug?** **A:** The change-detection compares columns that always differ (such as a load timestamp or an auto-updated column). Compare only the tracked business attributes (or a hash of them) and create a new version only when one of them actually changed.

**Q8. When would you choose Type 3 over Type 2?** **A:** When the business only needs to compare the current value with the immediately previous one (for example, before and after a one-off reorganisation) and wants simplicity and speed without date management.

---

## 10. Data Lake, Data Warehouse and Lakehouse

### 10.1 Why was the data lake invented?

The data warehouse was great, but it only handled **structured data** (tables with rows and columns). Then data exploded in **volume and variety**: logs, JSON, CSV exports, images, sensor streams. Forcing all of it into neat tables first was slow and expensive. So the **data lake** appeared: a place where you can **store data of any shape, as it is**.

🌟 **Analogy: library vs storage shed.**

- A **data warehouse** is a **library**. Every book must be catalogued and placed on the right shelf *before* it is allowed in. Finding things is quick, but intake is strict and space is costly.
- A **data lake** is a **huge cheap storage shed**. You throw boxes in as they arrive (books, photos, receipts, videos). Storing is easy and cheap, but if you want to find something you need some organising first.

💡 **Simple English: structured / semi-structured / unstructured** (recap from Section 2): tables / JSON-like files / free-form files such as images and PDFs.

### 10.2 Data warehouse vs data lake

The presenter compares them using a Microsoft Learn comparison. Here are the core differences:

|  | **Data warehouse** | **Data lake** |
| --- | --- | --- |
| **Data types** | Only **structured** | **Structured, semi-structured and unstructured** |
| **When is the schema defined?** | **Before** storing (**schema-on-write**), like running a `CREATE TABLE` before `INSERT` | **After** storing (**schema-on-read**): dump raw data first, define structure on top later |
| **Storage cost** | Higher | **Much cheaper** (the presenter says you could store many times more data for the same money) |
| **Typical use** | BI reports, dashboards | Big data, data science, raw archives, plus reporting |

💡 **Simple English: schema** = the blueprint of a table: column names, data types, rules.

- **Schema-on-write** = decide the blueprint *before* the data enters (strict).
- **Schema-on-read** = store the data first and decide the blueprint *when you read it* (flexible).

⚠️ The presenter says lakes also beat warehouses on query cost and performance. In practice, a **plain lake with raw files can be slower and less reliable** for BI than a warehouse, because it has no transactions and no table structure. That gap is exactly why the lakehouse (next) was invented.

### 10.3 So is the data warehouse dead? No: enter the Lakehouse

The presenter asks the scary question: “we learned warehouses, ETL, facts and dimensions. Is all that useless now?” **No. It is all still used.** We simply **combine the best of both worlds**:

> **Lakehouse = Data Lake + Data Warehouse** (the name takes *Lake* from data lake and *house* from ware**house**).

- **Storage:** keep the data in the **lake** because it is cheap.
- **Structure:** add a **metadata layer** on top (also called the **abstraction layer**, **logical layer** or **tabular-format layer**). It stores the schema and table information.
- **Modeling:** build **dimensional models (facts and dimensions)** on top, exactly like a warehouse.
- **Querying:** analysts use **normal SQL**, even though underneath there are just files in a lake.

```
    Reports (Power BI)     Data scientists      Managers      <- use normal SQL
            |                    |                  |
   +-----------------------------------------------------+
   |  METADATA / ABSTRACTION LAYER                       |  <- gives tables, schema,
   |  (a tabular format such as Delta)                   |     transactions
   +-----------------------------------------------------+
   |  DATA LAKE (cheap cloud storage)                    |
   |  JSON files | CSV files | Parquet files | images    |
   +-----------------------------------------------------+
```

*Caption: the lakehouse. Cheap files at the bottom, a metadata layer in the middle that makes them behave like tables, SQL users at the top.*

🌟 **Analogy:** you build a **library inside the cheap storage shed**. The boxes stay where they are (cheap), but you add a **card catalogue** (metadata layer) so any visitor can find a book as easily as in a normal library.

**What changed and what did not?**

| Still the same | What changed |
| --- | --- |
| ETL and pipelines | Data is stored as **files in a lake** (JSON, CSV, Parquet), not inside a traditional database |
| Incremental loading | A **metadata layer** gives file-based data table-like behaviour |
| Facts, dimensions, star schema | Storage is far cheaper and can hold any data type |
| SCD Type 1, 2, 3 | Reports still query using ordinary SQL |

```
  Time -->
  Traditional warehouse  ->   Data lake (cheap, flexible)   ->   LAKEHOUSE (best of both)
  strict tables, costly       raw files, little structure        files + metadata layer + SQL
```

*Caption: the evolution that leads to the lakehouse.*

**Three-way comparison**

|  | Data warehouse | Data lake | **Lakehouse** |
| --- | --- | --- | --- |
| Data it holds | Structured | All types | All types |
| Storage cost | High | Low | **Low** |
| Reliability (transactions) | Strong | Weak by default | **Strong** (via Delta, Section 12) |
| Dimensional models | Yes | Awkward | **Yes** |
| Plain SQL access | Yes | Limited | **Yes** |

```sql
-- Lakehouse in practice (Databricks / Spark SQL, extra):
-- the data are Delta files sitting in the lake; this makes them a SQL table
CREATE TABLE gold_sales USING DELTA LOCATION '/mnt/lake/gold/sales';

-- Analysts query it exactly like a warehouse table
SELECT region, SUM(amount) AS revenue FROM gold_sales GROUP BY region;
```

✅ **Checkpoint:** Explain in one breath why a lakehouse is cheaper than a warehouse yet still works with SQL.

### Interview Questions

**Q1. Data lake vs data warehouse?** **A:** A warehouse stores structured data with a schema defined up front (schema-on-write) and is optimised for BI. A lake stores any data type as raw files cheaply, with the schema applied later (schema-on-read).

**Q2. What is a lakehouse and why did it emerge?** **A:** A lakehouse combines a data lake’s cheap, flexible storage with a warehouse’s structure and reliability by adding a metadata layer (for example Delta) over lake files. It emerged because lakes alone were unreliable for BI and warehouses were costly and limited to structured data.

**Q3. Do we still need dimensional modeling in a lakehouse?** **A:** Yes. Dimensional models (facts, dimensions, star schemas, SCDs) are still the best way to organise data for reporting. Only the storage layer changes.

**Q4. Scenario: you receive 5 TB per day of raw JSON clickstream logs, and you need cheap storage but also dashboards for the business. What architecture would you suggest?** **A:** Land the raw JSON in a data lake (cheap), process it through bronze, silver and gold layers into Delta tables (lakehouse), and expose the gold facts and dimensions to BI tools via SQL.

**Q5. Scenario: data scientists complain that tables in the lake sometimes show half-written data after a failed job. What is missing?** **A:** Transactional guarantees. Adopt a table format with ACID transactions such as Delta, so failed writes are rolled back and readers only see committed data.

**Q6. What does schema-on-read mean and what is its trade-off?** **A:** The schema is applied when data is read, not when it is stored. It is very flexible for ingesting raw data, but bad data can slip in unnoticed and errors appear later at query time.

---

## 11. File Formats: Row-Based vs Column-Based

### 11.1 The one idea you need

When a table is saved on a disk, the computer must decide the **order in which the values are physically written**. There are two choices.

**Sample table**

| product\_id | name | category |
| --- | --- | --- |
| 1 | Honey | Food |
| 2 | Shirt | Clothing |
| 3 | Comb | Clothing |

**Row-based**: write **record by record**.

```
 DISK:  [1 Honey Food] [2 Shirt Clothing] [3 Comb Clothing]
          row 1           row 2              row 3
```

**Column-based**: write **column by column**.

```
 DISK:  [1 2 3] [Honey Shirt Comb] [Food Clothing Clothing]
        id col   name col           category col
```

*Caption: the same data, stored two different ways on disk.*

🌟 **Analogy: a class register.**

- **Row-based** = a register with **one line per student** (name, maths, English, science together). Great if you want **one student’s complete record**. Great for **adding or editing** a student.
- **Column-based** = **separate sheets per subject**: one sheet has *all* students’ maths marks. Great if you want the **class average in maths**. You don’t have to read English or science at all.

### 11.2 Which is better for what?

|  | **Row-based** | **Column-based** |
| --- | --- | --- |
| Examples | **CSV** (very common and popular), **Avro** (newer, don’t spend much time on it) | **Parquet** (very popular), **ORC** |
| Strong at | **Writing** and **updating** whole records quickly | **Reading** (querying) lots of rows for a few columns |
| Why | A record’s values sit together, so it is easy to find a record and change the other columns | A column’s values sit together, so one column can be fetched in one go |
| Fits | **OLTP** side (transactions) | **OLAP** side, big data, analytics |
| Compression *(extra)* | Weaker | **Stronger** (similar values sit together) |

**Worked example *(extra numbers)*:** you have a table with **100 columns and 1 billion rows**, and you run `SELECT SUM(price) FROM sales`.

- **Row-based (CSV):** the engine must walk through *every row*, skipping past 99 unwanted columns each time. It reads roughly the **whole file**.
- **Column-based (Parquet):** the engine jumps straight to the `price` column and reads **only that one column**, roughly 1/100th of the data. Much faster and cheaper.

This is why Parquet and ORC became the standard in big data, and why the data lakehouse stores Parquet underneath.

```python
# Converting a CSV (row-based) into Parquet (column-based) with PySpark (extra)
df = spark.read.csv('/data/sales.csv', header=True, inferSchema=True)
df.write.mode('overwrite').parquet('/data/sales_parquet')
```

⚠️ **Common mistake:** keeping big analytical tables as CSV. They are slow to query, big on disk and carry no reliable data types.

✅ **Checkpoint:** For each of these jobs say row-based or column-based: (a) a banking app saving every transfer; (b) a dashboard summing sales by region over 3 years.

### Interview Questions

**Q1. Row-based vs column-based file formats?** **A:** Row-based formats (CSV, Avro) store each record contiguously and suit fast writes and updates. Column-based formats (Parquet, ORC) store each column contiguously and suit analytical reads that touch a few columns across many rows.

**Q2. Why is Parquet popular for big data analytics?** **A:** Queries read only the columns they need, which cuts I/O, and column storage compresses well. That makes large scans faster and cheaper.

**Q3. Scenario: analysts query only 2 columns from a 200-column CSV and it takes minutes. What do you change?** **A:** Convert the data to Parquet (or store it as a Delta table). The engine then reads only the two columns instead of the whole file.

**Q4. Scenario: a service must append single records thousands of times per second and read each full record back. Which format fits?** **A:** A row-based approach (such as a row-oriented database or Avro) is better, because writes and whole-record reads are the priority.

**Q5. Which formats go with OLTP and which with OLAP, and why?** **A:** OLTP favours row-based storage for fast writes and updates. OLAP favours column-based storage for fast analytical reads.

---

## 12. Delta Format (Delta Lake)

### 12.1 What it is

The presenter says Delta is the most in-demand file format right now. In his words it is an **open table format built on top of Parquet** that also acts as a **transaction layer**.

💡 **Simple English**

- **Open table format**: a public, vendor-neutral way of organising files in a lake so that they behave like a database table.
- **Transaction log**: a **diary of every change** made to the table (who added, updated or deleted what, and when).
- **Built on Parquet**: the actual data is still stored in ordinary Parquet files, so it keeps Parquet’s fast reads and cheap storage.

🌟 **Analogy: a binder with a change diary.** Parquet files are the **pages in a binder**. The Delta transaction log is the **diary at the front** that writes down every time pages are added, removed or edited, with a **version number**. Because of the diary you can see, or even restore, the binder as it was last Tuesday.

```
  my_delta_table/
     |-- part-0001.parquet            <- the real data (Parquet files)
     |-- part-0002.parquet
     |-- _delta_log/                  <- the TRANSACTION LOG (the diary)
            |-- 00000000000000000000.json   v0: table created, data inserted
            |-- 00000000000000000001.json   v1: an UPDATE was applied
            |-- 00000000000000000002.json   v2: a DELETE was applied
```

*Caption: a Delta table is Parquet files plus a \_delta\_log folder of JSON files. Each JSON file records one version of the table.*

⚠️ **Nuance** *(extra)*: each Parquet file still carries its own small metadata. Delta’s contribution is a **table-level log** that records which files make up the table at every version.

### 12.2 The superpowers

**Superpower 1: Versioning and time travel**

| Version | What happened | Rows in table |
| --- | --- | --- |
| v0 | Table created, 100 rows inserted | 100 |
| v1 | An update was applied to some rows | 100 |
| v2 | A delete was run (by mistake!) | 60 |
| back to v1 | **Restore from the log** | 100 again |

```sql
-- Time travel in Delta (Databricks / Spark SQL, extra)
DESCRIBE HISTORY sales;                    -- see every version and what happened
SELECT * FROM sales VERSION AS OF 1;      -- look at the table as it was in version 1
RESTORE TABLE sales TO VERSION AS OF 1;   -- undo the mistaken delete
```

**Superpower 2: Schema evolution.** Your table has 5 columns, then the source suddenly adds a 6th. Delta can **evolve** the schema to accept the new column instead of failing. (The transcript mistakenly says “schema evaluation”.)

```python
# Allow new columns while appending (PySpark, extra)
df.write.format('delta').mode('append').option('mergeSchema', 'true').save('/mnt/lake/silver/orders')
```

**Superpower 3: ACID transactions.** Traditional databases (PostgreSQL, MySQL) guarantee ACID. Delta brings the same guarantees to a lake or lakehouse.

| Letter | Meaning | Bank-transfer analogy |
| --- | --- | --- |
| **A** | **Atomicity**: all or nothing | Money leaves Account A **and** reaches Account B, or neither happens |
| **C** | **Consistency**: rules are always respected | Total money in the bank stays correct; no negative balance if forbidden |
| **I** | **Isolation**: simultaneous jobs don’t disturb each other | While one person is mid-transfer, another sees either the before or after, never a half-done state |
| **D** | **Durability**: once saved, it stays saved | After the “success” message, a power cut does not undo the transfer |

**Superpower 4: low cost.** The data are still Parquet files in cheap lake storage. Only the small log is added. The presenter says you often cannot tell the difference from a traditional database, in both query performance and behaviour.

### 12.3 Parquet vs Delta

|  | Plain **Parquet** | **Delta** (Parquet + log) |
| --- | --- | --- |
| Storage | Columnar files | Columnar Parquet files **plus** `_delta_log` |
| ACID transactions | No | **Yes** |
| Time travel | No | **Yes** |
| Schema evolution and enforcement | Limited, manual | **Built in** |
| Safe UPDATE / DELETE / MERGE | Awkward (rewrite files yourself) | **Supported** |
| Reader sees half-written data? | Possible | **No**, only committed versions |

```
  Where Delta sits in a lakehouse (bottom to top)

   SQL / BI tools / Spark
   -------------------------------
   DELTA  (transaction log + table behaviour)
   -------------------------------
   PARQUET files (columnar data)
   -------------------------------
   Cloud storage (ADLS Gen2 / S3 / GCS)
```

*Caption: Delta is the metadata layer from Section 10 made concrete.*

✅ **Checkpoint:** Say the four Delta superpowers (versioning, schema evolution, ACID, low cost) and give one sentence for each.

### Interview Questions

**Q1. What is Delta format and how does it relate to Parquet?** **A:** Delta is an open table format built on Parquet. The data are stored as Parquet files, and a transaction log (JSON files in `_delta_log`) adds ACID transactions, time travel and schema evolution.

**Q2. What does the transaction log do?** **A:** It records every change as a numbered version, listing which files were added or removed. That allows consistent reads, concurrent writes, versioning and time travel.

**Q3. Scenario: an engineer ran DELETE without a WHERE clause on a production Delta table. How do you recover?** **A:** Check `DESCRIBE HISTORY` to find the version before the delete, then `RESTORE TABLE ... TO VERSION AS OF <n>` (or read that version). This works only while the old files are still retained: running VACUUM removes old files (default retention is 7 days), so act quickly.

**Q4. Scenario: the source system adds a new column and your pipeline into a Delta table fails. Options?** **A:** Enable schema evolution (for example `mergeSchema`) to accept the new column, or keep strict schema enforcement and update the pipeline deliberately. Choose evolution for trusted, additive changes; choose enforcement when unexpected columns should raise an alarm.

**Q5. Explain ACID with an example and say why a plain data lake lacks it.** **A:** In a bank transfer, atomicity means both the debit and credit happen or neither does; consistency keeps rules valid; isolation stops concurrent transfers from seeing half-done states; durability keeps committed data after a crash. A plain lake is just files, so a job that fails midway can leave partial files that readers might see. Delta’s log makes writes commit atomically.

**Q6. Scenario: two pipelines try to update the same Delta table at the same time. What happens?** **A:** Delta uses optimistic concurrency control through the log. Non-conflicting writes both succeed; if they touch the same data, one gets a conflict error and must retry. Readers keep seeing the last committed version.

---

## 13. Big Data, Big Data Frameworks and Apache Spark

### 13.1 What is big data?

**Big data** = a very large amount of data, too large or too fast for one ordinary computer to handle comfortably. There is no official line between “normal” and “big”. The presenter’s view: nowadays almost all company data is so large that the word “big” is no longer needed; “data” already means big data.

💡 **Simple English: the 3 Vs** *(extra, commonly asked)*: **Volume** (how much data), **Velocity** (how fast it arrives), **Variety** (how many different shapes it has).

When data is this large, one machine and one tool are not enough. So we use **big data frameworks**.

### 13.2 The big data frameworks mentioned

| Framework | What it is used for | Everyday analogy |
| --- | --- | --- |
| **Apache Kafka** | Handling **streaming (real-time) data** that is also huge | A never-ending **conveyor belt** of messages that many readers can pick from |
| **Apache Airflow** | **Orchestration**: deciding **what runs when**, and in what order, across many pipelines | A music **orchestra conductor**: tells each player when to start and stop |
| **Apache Hive** | A SQL-like layer to create tables and databases over data in big data storage (if you know SQL, Hive feels familiar) | A **catalogue** that makes a pile of files look like tables |
| **Apache Spark** | A **distributed engine to process and transform big data fast**. The hero of the show and the most in-demand skill | A **team of workers** splitting one huge job |
| **Databricks** | A platform that **manages Spark clusters for you** | A **fully staffed kitchen** you rent instead of hiring and managing every cook |

💡 **Simple English: orchestration** = coordinating many tasks so they run in the right order at the right time, with retries if something fails. If pipeline B needs the result of pipeline A, orchestration makes sure A finishes first.

### 13.3 Distributed computing

🌟 **Analogy 1: the school computer lab.** Imagine joining 20 computers from your lab so they act as **one super-computer**. Give it a job and 20 machines work together, so the job finishes far faster than on one.

🌟 **Analogy 2: the group assignment.** Your professor gives you a big assignment. Instead of doing it alone, you split it into pieces and give a piece to each of 10 or 20 friends. One friend (the team leader) hands out the pieces and collects them at the end. That is distributed computing.

💡 **Simple English**

- **Node** = one machine (computer).
- **Cluster** = a group of machines working together as one.
- **Distributed computing** = splitting work across many machines in a cluster, instead of asking one machine to do everything.

|  | One powerful machine | Distributed cluster |
| --- | --- | --- |
| Speed on huge data | Slow, may run out of memory | **Fast**, work done in parallel |
| Growing data | Must buy a bigger machine | **Add more machines** |
| If one machine fails | Everything stops | Others can take over *(extra)* |

### 13.4 Spark architecture

Spark uses two kinds of nodes:

- **Driver node**: exactly **one**, the **brain** of the cluster. It receives your job, decides how to split it and tells each worker what to do. In the presenter’s words it “doesn’t do the heavy work, it just orchestrates”.
- **Worker nodes**: all the **other machines**. They carry out the real work: executing your code and transforming the data.

```
                         +--------------------------+
   You submit a job ---> |       DRIVER NODE        |   the brain: plans the work,
                         |  (only ONE per cluster)  |   gives instructions
                         +------------+-------------+
                                      |
           +--------------------------+--------------------------+
           |                          |                          |
   +-------v--------+         +-------v--------+         +-------v--------+
   |  WORKER NODE 1 |         |  WORKER NODE 2 |         |  WORKER NODE 3 |
   |  works on      |         |  works on      |         |  works on      |
   |  slice A       |         |  slice B       |         |  slice C       |
   +----------------+         +----------------+         +----------------+

         <==== results are combined and returned to you ====
   [ the whole group of machines together = the CLUSTER ]
```

*Caption: Spark architecture. One driver coordinates many workers; together they form a cluster.*

**Worked example** *(extra numbers)*: you want total revenue per city from **1 billion** order rows.

1. The driver splits the data into slices (say 4 slices of 250 million rows).
2. Each worker totals revenue per city **for its own slice** at the same time.
3. The partial totals are combined into the final answer. Four machines finish in roughly a quarter of the time of one machine.

```python
# The same idea in PySpark; Spark does the splitting and combining for you
from pyspark.sql import functions as F

df = spark.read.parquet('/lake/silver/orders')                 # data is spread across workers
result = df.groupBy('city').agg(F.sum('amount').alias('revenue'))
result.write.format('delta').mode('overwrite').save('/lake/gold/revenue_by_city')
```

**Why Databricks?** Running Spark yourself means choosing machines, installing software, and managing the driver and workers. **Databricks manages the cluster for you.** You only say how much computing power you want (configure the cluster); it does the rest. That is why the presenter loves it, and why companies hire Databricks developers.

✅ **Checkpoint:** Draw the driver and three workers from memory and describe what each does.

### Interview Questions

**Q1. What is Apache Spark and why is it popular?** **A:** Spark is a distributed data processing engine. It splits big datasets across many machines and processes them in parallel (and largely in memory), so large transformations finish quickly. It is flexible, supports Python/SQL/Scala and is the centre of most big data stacks.

**Q2. Driver node vs worker node?** **A:** The driver is the single coordinator: it builds the execution plan and assigns tasks. Workers execute those tasks on slices of the data and return results.

**Q3. What do Kafka, Airflow, Hive, Spark and Databricks each do?** **A:** Kafka streams real-time data; Airflow orchestrates and schedules pipelines; Hive provides SQL-style tables over big data; Spark processes and transforms data in a distributed way; Databricks is a managed platform that runs and manages Spark clusters.

**Q4. Scenario: your Python script on a single server takes 10 hours and sometimes crashes with out-of-memory errors on a 500 GB dataset. What do you do?** **A:** Move the processing to a distributed engine such as Spark on a cluster (for example Databricks). The data is partitioned across workers, so memory pressure is spread out and work runs in parallel. Store the data in a columnar format like Parquet or Delta for faster scans.

**Q5. Scenario: a worker node dies in the middle of a Spark job. Does the job fail?** **A:** Usually not. Spark tracks how each partition was built and re-runs the lost tasks on other workers. The driver node, however, is a single point of coordination, so losing it fails the job.

**Q6. Scenario: you have 20 pipelines where pipeline C must run only after A and B succeed, with automatic retries and alerts. Which tool category do you reach for?** **A:** An orchestrator such as Apache Airflow (or Azure Data Factory in Azure) to define dependencies, schedule runs, retry failures and send alerts.

---

## 14. Cloud Computing and Cloud Data Engineering

### 14.1 Why the cloud?

The presenter says that around **90%** of data is now stored in the cloud, with only highly sensitive data kept on-premise (treat this as a rough guide, not a statistic). The main reasons: cloud storage is **cheaper**, it **scales** whenever you want, and you do **not** maintain the hardware.

**The three big players**

| Provider | Owned by | Full name |
| --- | --- | --- |
| **Azure** | Microsoft | Microsoft Azure |
| **AWS** | Amazon | Amazon Web Services |
| **GCP** | Google | Google Cloud Platform |

### 14.2 What is cloud computing? (the presenter’s example)

You run a company and need **100 computers**, each with a processor, **8 GB RAM** and **1 TB storage**. Problems if you buy them:

- It is **very expensive**.
- You rarely use all 100 at the same time. Often you use only 40 to 50, sometimes 80 to 90.
- During a **festival season** you suddenly need **150 to 200**. Rushing to a market to buy 50 more computers is slow and painful.

**The cloud solution:** Azure owns **thousands** (in reality many more) of computers. It says: *rent from me.* You pay only for what you use: 80 computers, pay for 80. Need 200 urgently? You get them **within minutes**. You do not own the machines, and you do not maintain them or guard them.

💡 **Simple English: cloud computing** = renting computing power, storage and tools over the **internet**, and paying only for what you use.

🌟 **Analogies**

- **Electricity from the grid vs owning a power plant.** You don’t build a generator; you plug in and pay for the units you consume.
- **Taking a cab vs buying a car** for occasional trips.
- **A hotel vs buying a house** for a short stay.

```
  ON-PREMISE                               CLOUD
  +------------------------+               +---------------------------------+
  | Your own data centre   |               | Provider’s huge data centres     |
  | 100 computers bought   |               | thousands of computers          |
  | idle most of the time  |               |  rent 80 today, 200 tomorrow    |
  | you repair and secure  |               |  pay per use, provider maintains|
  +------------------------+               +---------------------------------+
```

*Caption: owning machines vs renting capacity on demand.*

|  | On-premise | Cloud |
| --- | --- | --- |
| Upfront cost | High (buy hardware) | Low (pay as you go) |
| Scaling | Slow (buy and install) | **Minutes** |
| Unused capacity | You still pay for it | You don’t pay |
| Maintenance | Your team | Provider |
| Billing | Fixed | Based on usage |

💡 **Simple English: scalability** = being able to grow or shrink resources whenever needed.

⚠️ **Security nuance** *(extra)*: the presenter says the provider takes care of security of the data, and quotes about 99.95% (that figure is really an **availability** promise, not a security guarantee). In practice there is a **shared responsibility model**: the provider secures the physical data centres and platform; **you** must configure access, passwords and permissions correctly.

⚠️ **Cost nuance** *(extra)*: “pay for what you use” also means a cluster left running overnight is billed. Use auto-shutdown and budgets (see Cost Management in Section 16).

The lake from Section 10 is why cloud data storage is so cheap: most engineers store big data in a **data lake** on cloud storage.

### 14.3 Which cloud should you learn?

The presenter’s advice:

1. **Pick one cloud and master it.** All clouds offer the same kinds of services under different names, so moving later is easy.
2. **Recommended: Azure.** Reason one: demand is growing, and he sees a solid future after Microsoft Fabric. Reason two: you can create a **free Azure account with about $200 credit for 30 days** (verify the current offer on Microsoft’s site).

**The same service under different names**

| Job | **Azure** | **AWS** | **GCP** |
| --- | --- | --- | --- |
| Data lake storage | ADLS Gen2 | S3 | Cloud Storage |
| Cloud data warehouse | Synapse Analytics | Redshift | BigQuery |
| Streaming ingestion | Event Hubs | Kinesis *(extra)* | Pub/Sub *(extra)* |
| Relational database | Azure SQL DB | RDS *(extra)* | Cloud SQL *(extra)* |
| ETL / orchestration | Data Factory | Glue *(extra)* | Dataflow / Composer *(extra)* |
| Secrets vault | Key Vault | Secrets Manager *(extra)* | Secret Manager *(extra)* |

The presenter named the lake and warehouse equivalents (S3, Cloud Storage, Redshift, BigQuery, Snowflake). The other cells are my additions for your revision.

✅ **Checkpoint:** Explain why an e-commerce company with sales spikes in festival season prefers cloud over buying servers.

### Interview Questions

**Q1. What is cloud computing and what are its benefits?** **A:** Renting computing resources (compute, storage, networking, managed services) over the internet on a pay-as-you-go basis. Benefits: lower upfront cost, instant scalability, no hardware maintenance, wide service choice.

**Q2. Scenario: your company traffic triples every festival season and idle servers cost money the rest of the year. What do you propose?** **A:** Move to cloud and scale resources up for the festival period and back down afterwards, paying only for what is used.

**Q3. Scenario: your team knows Azure, but a new client uses AWS. How do you approach it?** **A:** The concepts (lake, warehouse, orchestration, Spark, medallion layers) are the same. I would map each Azure service to its AWS equivalent (ADLS Gen2 to S3, Synapse to Redshift, and so on) and learn the AWS-specific details.

**Q4. Scenario: your cloud bill doubled this month. Where do you look?** **A:** Check cost-management reports for the biggest resources. Typical culprits: clusters left running, oversized clusters, unneeded data copies, and pipelines running more often than required. Add auto-termination, budgets and alerts.

**Q5. Who is responsible for security in the cloud?** **A:** Both. The provider secures the underlying infrastructure; the customer secures identities, access permissions, secrets and data configuration (the shared responsibility model).

---

## 15. Medallion Architecture (Bronze, Silver, Gold)

### 15.1 The idea

The **medallion architecture** is a way to organise data in a lake or lakehouse into **three layers**, named after medals. As data moves from one layer to the next it gets **cleaner and more useful**. It is similar in spirit to the staging layer from Section 6, and it is the standard pattern in cloud data engineering.

```
  Batch data -------+
                    +--> BRONZE -------> SILVER -------> GOLD -------> BI, data analysts,
  Streaming data ---+    raw             cleaned          serve-ready     data scientists
                         no changes      schema applied   facts and dims  (downstream)
```

*Caption: batch and streaming data both enter bronze, get cleaned in silver, and are shaped for use in gold.*

🌟 **Analogy: from gold ore to jewellery.**

- **Bronze** = ore dug out of the ground, exactly as found, mud and stones included.
- **Silver** = ore crushed, washed and refined into pure metal. Clean, but not yet something you would wear.
- **Gold** = polished jewellery, shaped for customers and ready to sell.

💡 **Simple English**

- **Batch data**: data that arrives in chunks (for example every hour or every night).
- **Streaming data**: data that flows continuously in real time.
- **Downstream**: the people and apps that consume the final data (Section 3).

### 15.2 The three layers

|  | **Bronze** | **Silver** | **Gold** |
| --- | --- | --- | --- |
| Also called | Raw layer, **landing zone** | Cleansed / transformed layer | Curated / serving layer |
| What it holds | Data **exactly as it came** from the source | Data after **cleaning and transformation** | Data modeled for use: **facts and dimensions** or **aggregated tables** |
| Changes allowed? | **No changes at all** (rule number one) | Clean, validate, de-duplicate, standardise, apply and enforce schema, evolve schema if needed | Business modeling and aggregation based on requirements |
| Schema | None needed | **Defined and enforced** | Defined by the data model (for example a star schema) |
| Cleanliness | Zero | Cleaned, **not yet ready to serve** | **Ready to serve** |
| Typical users | Data engineers (reprocessing, audit) | Engineers, advanced analysts, data scientists | Analysts, BI tools, managers, ML |

The presenter notes that “aggregations” in silver simply means cleaning-type transformations, not business aggregations. Business aggregation belongs in gold.

**Why bronze must stay untouched** *(extra)*: it is your safety net. If you find a bug in your cleaning logic three weeks later, you can **re-run silver and gold from bronze** because the original data is still there.

**Mapping to the older warehouse vocabulary**

| Warehouse world (Section 6) | Lakehouse world |
| --- | --- |
| Source | Source |
| Staging layer | Roughly **Bronze** (raw landing) |
| Cleaning and transformation | **Silver** |
| Core layer (facts and dimensions) | **Gold** |

### 15.3 Worked example: pizza orders through the medals *(extra)*

| Layer | What the data looks like |
| --- | --- |
| **Bronze** `orders_raw` | `101, Aman, mumbai, qty 2` and the same order `101` again, `102, Riya, MUMBAI, qty NULL` (stored as received, duplicates and all) |
| **Silver** `orders_clean` | duplicate 101 removed, city uppercased to `MUMBAI`, dates typed properly, order 102 sent to a quarantine table |
| **Gold** `fact_orders`, `dim_customer`, `dim_product`, `gold_daily_sales` | star-schema tables plus a ready-made daily sales summary for the dashboard |

```python
from pyspark.sql import functions as F

# BRONZE: land the raw data exactly as received (no changes)
raw = spark.read.json('/lake/landing/orders/')
raw.write.format('delta').mode('append').save('/lake/bronze/orders')

# SILVER: clean and validate
bronze = spark.read.format('delta').load('/lake/bronze/orders')
silver = (bronze.dropDuplicates(['order_id'])                   # remove duplicates
                .withColumn('city', F.upper(F.trim('city')))     # standardise text
                .filter('qty IS NOT NULL'))                      # bad rows go elsewhere in real projects
silver.write.format('delta').mode('overwrite').save('/lake/silver/orders')

# GOLD: business-ready table
gold = silver.groupBy('city').agg(F.sum(F.col('qty') * F.col('price')).alias('revenue'))
gold.write.format('delta').mode('overwrite').save('/lake/gold/revenue_by_city')
```

In the cloud architecture of Section 16, the lake storage holds all three layers, **Azure Data Factory** moves data into bronze, **Databricks** transforms bronze to silver, and **Synapse** builds the facts and dimensions in gold.

✅ **Checkpoint:** Without looking, state the one rule of bronze and the one job of silver.

### Interview Questions

**Q1. Explain the medallion architecture.** **A:** A layered lakehouse design. Bronze holds raw data as ingested, silver holds cleaned and validated data with an enforced schema, and gold holds business-ready models (facts, dimensions, aggregates) for downstream users. Quality improves at each step.

**Q2. Why shouldn’t we transform data in the bronze layer?** **A:** Bronze is the untouched record of what the source sent. Keeping it as-is allows auditing and lets you reprocess everything if transformation logic has a bug or requirements change.

**Q3. Scenario: two weeks after go-live you discover the silver cleaning logic dropped valid rows. How do you recover?** **A:** Fix the logic and rebuild silver (and then gold) from the bronze layer, which still holds the raw data. Without a bronze layer you would have to ask the source to resend everything.

**Q4. Scenario: analysts report different revenue numbers because some query silver and some query gold. What do you do?** **A:** Make gold the single approved source for reporting, with agreed metric definitions. Restrict or document silver as an engineering layer, so every dashboard uses the same curated models.

**Q5. Where would a Type 2 slowly changing dimension live, and why?** **A:** In the gold layer, because dimensions and facts are the serving models. Silver supplies the cleaned input and the pipeline applies SCD logic when loading gold.

**Q6. How does medallion compare with staging and core layers?** **A:** Staging is roughly bronze (raw landing). Core (facts and dimensions) corresponds to gold, with silver as the explicit cleaning step in between. Medallion makes that intermediate stage a named, stored layer, and it runs on a lake rather than a traditional database.

---

## 16. End-to-End Cloud Data Engineering Architecture on Azure

### 16.1 The plan

The presenter shows a famous architecture diagram from Microsoft Learn, packed with icons and numbers. The first reaction is always “what is all this?” His method, which we copy here:

1. **Ignore the numbers** in the Microsoft diagram.
2. **Learn each tool** one at a time (this section).
3. **Walk through the flow once**, in his order (16.4).

By the end, every box should make sense. Notice how many of the tools are just the **concepts you already learned** wearing Azure names.

### 16.2 The tools, one by one

#### 1. Azure Event Hubs: the streaming source

- **What:** a service that **receives and stores a continuous stream of data** (a source that keeps going “tuck tuck tuck” non-stop) so you can run real-time analytics on it.
- **Interview answer:** “Which Azure service would you use to store or ingest streams?” → **Azure Event Hubs**.
- **IoT Hub** (shown at the start of the diagram): IoT = Internet of Things, meaning sensors and devices such as digital thermostats that record data every second. They send their streams through IoT Hub to Event Hubs.
- 🌟 **Analogy:** an airport **conveyor belt** that never stops. Bags (events) keep arriving and are held on the belt until someone picks them up.
- It plays the same role as **Apache Kafka** from Section 13 *(extra: Event Hubs can even speak the Kafka protocol)*.

#### 2. Azure SQL Database (Azure SQL DB): the cloud OLTP database

- **What:** your familiar SQL database (like MySQL, PostgreSQL or SQL Server), but running in Azure.
- **Role:** an **OLTP source** (Section 4). You can create OLTP databases in the cloud with it.
- **Same SQL as always:** SELECT, UPDATE, DELETE, DDL, TCL and DCL commands all work, just like on an on-premise database.

💡 **Simple English: the SQL command families** *(extra)*: **DDL** defines structure (CREATE, ALTER, DROP); **DML** changes data (INSERT, UPDATE, DELETE); **TCL** controls transactions (COMMIT, ROLLBACK); **DCL** controls permissions (GRANT, REVOKE).

#### 3. Azure Data Lake Storage Gen2 (ADLS Gen2): the data lake

- **What:** Azure’s data lake (Section 10). It stores **structured, semi-structured and unstructured** data.
- **Where it lives:** you first create a **storage account**. Inside it you get several services (the presenter forgot the last name; they are **blob / data lake storage, file shares, queues and tables**). The **data lake** is the main one for data engineers. **Tables** there hold NoSQL key-value data.
- **Hierarchical namespace (HNS):** data lake storage is organised as **containers**, and inside a container you can create **folders inside folders inside folders**, as deep as you like.
  - 💡 **Simple English: hierarchical namespace** = **real folders and sub-folders** (a tree) rather than one flat pile of files.
  - 🌟 **Analogy:** a **filing cabinet**: the cabinet is the storage account, a drawer is a container, then folders, then sub-folders.
  - This matters for big data, where you save data into many nested folders (for example `orders/2024/01/02/`). It is also the main difference between ADLS Gen2 and plain **blob storage** *(the presenter mentions this and says it will be covered later)*.

```
  Storage account: mylake
     |-- container: bronze                 <- raw data (Section 15)
     |      |-- orders/2024/01/02/orders.json
     |-- container: silver                 <- cleaned data
     |      |-- orders/
     |-- container: gold                   <- facts, dimensions, aggregates
            |-- fact_orders/
```

*Caption: an example lake layout with one container per medallion layer (my example, not from the video).*

- **AWS equivalent:** S3. **GCP equivalent:** Google Cloud Storage.

#### 4. Azure Data Factory (ADF): the ETL and orchestration tool

- **What:** Azure’s **ETL tool** (Section 5). It **extracts and moves data** from one place to another, and **orchestrates** (schedules and sequences) tasks.
- **Low-code, not no-code:** most work is done by dragging and configuring boxes, with only a little code.
- **Connectors:** it has a huge number of ready-made **connectors**, so you can connect an API, a SQL database, files and many other systems.
- **Example:** pull data from an API (a website’s data connector) and store it in the data lake or in a SQL database, all configured visually.
- 🌟 **Analogy:** a **logistics manager with a fleet of delivery trucks**. Trucks (connectors) carry goods between places, and the manager schedules who goes where and when.

#### 5. Azure Databricks: the transformation engine

- **What:** the managed platform for **Apache Spark** (Section 13).
- **Typical job:** ADF drops data into the lake’s **raw/bronze** zone. Databricks reads it, **transforms** it and creates the **silver** layer.
- **Why love it:** you do **not** manage driver or worker nodes. You simply **configure the cluster** (how much computing power) and Databricks does the rest.
- **In demand:** the presenter says almost every company is hunting for Databricks developers.

#### 6. Azure Synapse Analytics: the cloud data warehouse

- **What:** a **cloud data warehousing** solution (Section 4). You can build **facts and dimensions** in it (star schema, Section 8).
- **Equivalents:** Snowflake, Amazon Redshift, Google BigQuery.
- **Role in the flow:** builds the **gold layer** of facts and dimensions that reports use.

#### 7. Power BI: reporting and dashboards

- **What:** Microsoft’s **reporting tool**. Analysts use it to build dashboards on top of the gold layer.
- **Why Azure + Power BI is a strong pair:** same parent company (Microsoft), so connectors are excellent, and demand for Power BI is rising fast.
- **KPIs:** reports usually show **KPIs (key performance indicators)**, the key numbers that show how the business is doing (is it growing? are there losses?), as pie charts, line charts and so on.
- **Mobile and laptop:** managers can view the same dashboards on a phone or a laptop.

```
  The complete data journey in one line (the presenter’s final drawing):

  OLTP source --> ETL --> OLAP (gold: star schema) --> Power BI --> Report --> Manager / decision maker
```

#### 8. The supporting cast (you should know them, but others often manage them)

| Service | What it does | Simple analogy |
| --- | --- | --- |
| **Microsoft Purview** | **Data governance**: catalogues what data exists, where it came from and who may use it. Usually run by a **data governance team**, but you should know it | The **library catalogue plus rulebook** |
| **Azure DevOps** | **CI/CD** for deploying code between environments. In real projects you work in three environments: **Dev, QA and Prod** | An **assembly line with quality checks** before products reach the shop |
| **Azure Key Vault** | Stores **secrets**: passwords, keys, connection strings, anything you cannot leave in the open | A **locker or safe**; pipelines ask the vault for the password instead of having it written in code |
| **Microsoft Entra ID** | The **identity service**: a record of all users in your organisation and what they are allowed to do | The **school ID-card office** |
| **Azure Monitor** | **Monitors** the Azure environment: which pipelines ran, which failed, and alerts | The **CCTV and alarm system** |
| **Cost Management** | Tracks and controls your **monthly bills** | The **expense tracker** |

💡 **Simple English: CI/CD** = **C**ontinuous **I**ntegration / **C**ontinuous **D**elivery. Code changes are automatically tested and then **promoted step by step** to different environments.

- **Dev** = where you build (test kitchen).
- **QA** = where it is tested (tasting panel).
- **Prod** = the real thing that users and the business rely on (the live restaurant).

### 16.3 One-page summary of the tools

| Tool | Category | Its job in the flow | Concept from earlier sections |
| --- | --- | --- | --- |
| IoT Hub, Event Hubs | Streaming source | Capture continuous sensor and event data | Streaming data, Kafka (Section 13) |
| Azure SQL DB | OLTP database | Source of transactional data | OLTP (Section 4) |
| ADLS Gen2 | Data lake | Stores bronze, silver and gold | Data lake (Section 10), medallion (Section 15) |
| Azure Data Factory | ETL / orchestration | Moves data, schedules pipelines | ETL (Section 5), Airflow role |
| Azure Databricks | Spark platform | Transforms bronze to silver | Spark (Section 13) |
| Azure Synapse Analytics | Cloud data warehouse | Builds facts and dimensions | OLAP, star schema (Sections 4 and 8) |
| Power BI | Reporting | Dashboards for analysts and managers | Serving (Section 2) |
| Purview, DevOps, Key Vault, Entra ID, Monitor, Cost Management | Governance, security, operations | Protect, deploy, watch and budget the platform | Upstream/downstream care (Section 3) |

### 16.4 Walking through the architecture step by step

```
  IoT sensors                                                       
      |                                                             
      v                                                             
 [Azure IoT Hub] --> [Azure Event Hubs]  (real-time stream captured)
                              |
                              v
                     [Azure Data Factory]   moves data as it is
                              |
                              v
    +----------------- ADLS Gen2 (the data lake) -----------------+
    |                                                             |
    |   BRONZE  ------->  SILVER  ------->  GOLD                 |
    |   raw, no change     cleaned           facts + dimensions   |
    |        ^ [Azure Databricks / Spark] ^  ^ [Azure Synapse]    |
    +-------------------------------------------------------------+
                                          |
                          +---------------+---------------+
                          v                               v
                     [Power BI]                  Data science / ML tools
                (analysts, managers)               (data scientists)

  Around everything: Purview | Azure DevOps | Key Vault | Entra ID | Monitor | Cost Management
```

*Caption: the architecture rebuilt in the presenter’s order. Streaming data goes in on the left, passes through bronze, silver and gold, and reaches two downstream groups on the right.*

**Step by step**

1. **IoT Hub** receives data from sensors and sends the **stream** to **Event Hubs**, which stores the real-time data.
2. **Azure Data Factory** picks the data up from Event Hubs and pushes it into the **bronze layer** of the lake **as it is** (rule number one: no change).
3. **Azure Databricks** reads bronze, uses **Spark** to clean and transform it, and writes the **silver layer**.
4. **Azure Synapse Analytics** builds the **gold layer** as **facts and dimensions** (a star schema).
5. Gold serves **two downstream groups**: **analysts** through Power BI (data analysts) and **data scientists** through their own resources. The data scientists’ side is not your responsibility.
6. **Purview** (governance), **DevOps** (CI/CD across Dev, QA, Prod), **Key Vault** (secrets), **Entra ID** (users), **Monitor** (health and failures) and **Cost Management** (bills) surround the whole thing.

✅ **Checkpoint:** Redraw the diagram without looking. Then say which tool is the E and L, which is the T, and which is the serving layer.

### Interview Questions

**Q1. Design a pipeline in Azure from IoT sensors to a dashboard. Which services do you use?** **A:** IoT Hub and Event Hubs ingest the stream; Data Factory moves data into the bronze layer in ADLS Gen2; Databricks transforms bronze to silver; Synapse builds gold facts and dimensions; Power BI serves dashboards. Supporting services: Key Vault, Monitor, DevOps, Purview, Entra ID.

**Q2. What is the hierarchical namespace in ADLS Gen2 and why does it matter?** **A:** It gives real directories (folders within folders) instead of a flat namespace. It makes organising big data (for example by date or layer) natural, and makes directory-level operations and permissions efficient.

**Q3. Data Factory vs Databricks: what is the difference in role?** **A:** Data Factory is for moving data and orchestrating pipelines with a low-code interface. Databricks is for heavy transformation using Spark. Typically ADF copies data in and triggers Databricks notebooks to transform it.

**Q4. Scenario: your pipeline needs the password of a source database. Where do you keep it?** **A:** In Azure Key Vault. Pipelines reference the secret at run time. Never hard-code passwords in code or configuration files.

**Q5. Scenario: the pipeline worked in Dev but failed in Prod after deployment. How do you reduce such surprises?** **A:** Use CI/CD through Azure DevOps to deploy the same tested code through Dev, then QA, then Prod, with environment-specific settings (connections, secrets) kept separate. Test in QA with production-like data before releasing.

**Q6. Scenario: a pipeline failed at 3 AM and nobody noticed until the manager complained at 10 AM. What do you add?** **A:** Monitoring and alerting with Azure Monitor, so failures trigger notifications (email, chat, pager), plus retry rules and a run-history dashboard.

**Q7. Scenario: a new analyst should see gold tables but not raw bronze data containing personal details. How do you handle it?** **A:** Use Entra ID groups and role-based access (and folder or container permissions in the lake) so that analysts have read-only access to gold only. Use Purview to classify sensitive data.

**Q8. Event Hubs vs Data Factory?** **A:** Event Hubs ingests and buffers a continuous stream of events. Data Factory moves data between systems and orchestrates pipelines, for example picking data up from Event Hubs and landing it in the lake.

---

## 17. Mixed Scenario Practice for Data Engineers *(extra)*

These questions combine several topics, the way real interviews do. Try answering out loud before reading the answer. Each one lists the concepts it tests so you can go back to the right section.

**Scenario 1: Design a data platform from scratch** An online store has an orders database, website click events and a payment API. Managers want daily sales dashboards, and data scientists want the raw click data. *Concepts tested: Sections 2, 4, 5, 10, 15, 16.* **Answer:**

1. **Sources:** orders in an OLTP database (Azure SQL DB), click events as a stream (Event Hubs), payments through an API.
2. **Ingest:** Data Factory runs hourly **incremental** loads (watermark on `updated_at`) from the orders DB and API into the **bronze** layer. Event Hubs data is landed in bronze too.
3. **Store:** ADLS Gen2 with bronze, silver and gold containers, files in **Delta** format.
4. **Transform:** Databricks (Spark) cleans bronze into silver: de-duplicate, standardise, enforce schema, quarantine bad rows.
5. **Model:** gold **star schema**: `fact_orders`, `dim_customer` (SCD Type 2 if history matters), `dim_product` (Type 1), `dim_date`, plus a daily sales aggregate.
6. **Serve:** Power BI reads gold; data scientists use silver and bronze.
7. **Operate:** orchestration in Data Factory, secrets in Key Vault, alerts in Monitor, CI/CD in DevOps, governance in Purview, budgets in Cost Management.

**Scenario 2: The dashboard total does not match the finance report** *Concepts tested: Sections 1, 6, 8, 9.* **Answer:** Work backwards and compare at each layer.

1. Agree on the **metric definition** with finance (gross or net? which time zone? refunds included?).
2. Compare **row counts and totals** between source, staging/bronze, silver and gold to find the layer where numbers diverge.
3. Look for **duplicates** (a reload without de-duplication), **fan-out joins** (a join on a non-unique key multiplies rows), **missing late-arriving data**, and for SCD Type 2 dimensions, joins that forgot `is_current` or the date range and double counted versions.
4. Fix the root cause, add automated reconciliation checks, and tell the stakeholder what was wrong.

**Scenario 3: A nightly full load takes 9 hours and is getting slower every month** *Concepts tested: Sections 5, 6, 7.* **Answer:** Convert it to **incremental loading**. Keep one full (initial) load. Then each night extract only rows with a `last_modified` greater than the stored watermark into transient staging, upsert them into core, and advance the watermark only after success. Run a periodic full reconciliation (for example weekly) to catch missed deletes or late data.

**Scenario 4: Revenue by region should reflect the region the customer lived in at the time of purchase** *Concepts tested: Sections 8, 9.* **Answer:** Use **SCD Type 2** on `dim_customer` with surrogate keys, start date, expiry date and current flag. When loading the fact table, look up the customer version where the order date falls between start and expiry, and store that **surrogate key** in the fact row. Old sales then stay linked to the old region forever.

**Scenario 5: Warehouse reports got slow after the data doubled** *Concepts tested: Sections 4, 8, 11, 12.* **Answer:** Check the model first: is it a **star** or a heavily joined snowflake? Flatten if needed. Confirm data is stored in a **columnar** format (Parquet/Delta, or a columnar warehouse). Reduce scanned data with **partitioning** by date and by selecting only needed columns. Pre-compute common aggregates into **gold summary tables**. Make sure loads are incremental so tables are not being rewritten.

**Scenario 6: A backfill must re-process the last 30 days without creating duplicates** *Concepts tested: Sections 5, 7, 12.* **Answer:** Make the load **idempotent**. Either overwrite just those 30 date partitions, or use a **MERGE** (upsert) on the business key so re-running the same data changes nothing. Re-run silver and gold from **bronze**, which still holds the raw data. Validate row counts before and after.

**Scenario 7: The source deletes some orders, but the warehouse still shows them** *Concepts tested: Sections 7, 9.* **Answer:** A date-based incremental filter never sees deletions. Options: use **Change Data Capture** or a source delete log; ask upstream for **soft deletes** (an `is_deleted` flag); or periodically compare the full list of source keys against the warehouse and mark missing ones as deleted. Prefer flagging in the warehouse over physically removing rows, so history is auditable.

**Scenario 8: 2 TB of application logs arrive daily. Analysts query them once a month. Where and how do you store them?** *Concepts tested: Sections 10, 11, 12, 14.* **Answer:** Not in a costly warehouse. Land raw logs (JSON) in the **cloud data lake** (bronze), convert to **Parquet or Delta** partitioned by date (silver) for fast, cheap queries, and expose them through a lakehouse SQL engine. Keep only curated summaries in gold. Cheap storage plus columnar format keeps cost low for infrequent use.

**Scenario 9: Data scientists want raw detail; analysts want clean numbers. One dataset can’t serve both, can it?** *Concepts tested: Sections 2, 15.* **Answer:** The medallion layers solve this. Data scientists use **silver** (clean but detailed) or even bronze for exploration; analysts use **gold** (modeled, aggregated, consistent). Engineers own bronze for replay and audit. One platform, three serving levels.

**Scenario 10: A source column changes from integer to text and the pipeline fails** *Concepts tested: Sections 3, 12.* **Answer:** Short term: investigate the failure log, cast or quarantine the incompatible values, and restart. Long term: agree **data contracts** with the upstream team, use **schema enforcement** in silver (with controlled schema evolution for additive changes), and alert on schema drift before it breaks reports.

**Scenario 11: Should this feed be streaming or batch?** *Concepts tested: Sections 13, 16.* **Answer:** Ask how fresh the business needs the data. If decisions can wait an hour or a day (daily sales), **batch** is simpler and cheaper. If seconds matter (fraud alerts, sensor alarms), use **streaming** (Event Hubs or Kafka plus a streaming job). Many platforms use both: streaming for urgent alerts, batch for analytics.

**Scenario 12: A colleague suggests connecting Power BI directly to the OLTP database “to save time”. Your response?** *Concepts tested: Sections 4, 5, 8.* **Answer:** It would slow the live application, produce inconsistent logic across reports, and reports would struggle against a normalised, write-optimised schema. Instead, build a warehouse or gold layer with dimensional models, and point Power BI at that.

**Scenario 13: Cloud costs jumped after launching a Databricks cluster** *Concepts tested: Section 14.* **Answer:** Check Cost Management for the cluster’s runtime. Typical fixes: **auto-terminate idle clusters**, use job clusters that start for a run and stop afterwards, right-size workers, avoid running heavy jobs more often than needed, and set budget alerts.

**Scenario 14: The upstream team refuses to add a column you need** *Concepts tested: Section 3.* **Answer:** Understand their constraints, then present the **business impact** (what decision or revenue depends on it). Offer alternatives: derive it from existing data, join to a reference table, or let your pipeline compute it. If it is critical, escalate with a clear request and a deadline through your manager. Keep the relationship healthy because you need them again tomorrow.

---

## 18. Full Step-by-Step Recap Checklist

This video teaches concepts rather than a click-along project, so this checklist is the **order in which you would think through and build a data platform**, drawn from every topic in the class. Tick each box when you can do or explain it without notes.

### Phase A: Understand the job

| # | Action | Done when you can… |
| --- | --- | --- |
| 1 | ☐ Define data engineering with the chef analogy | Say it in two sentences |
| 2 | ☐ Name the 3 pillars: production, transformation, serving | Draw them with an example each |
| 3 | ☐ Identify your **upstream** and **downstream** | Say who gives you data and who consumes it |
| 4 | ☐ Agree requirements with downstream; agree source changes with upstream | Explain why both conversations matter |

### Phase B: Design the source and warehouse

| # | Action | Done when you can… |
| --- | --- | --- |
| 5 | ☐ Treat the OLTP database as a **source** (managed by a DBA, normalised) | Explain write-optimised vs read-optimised |
| 6 | ☐ Plan an **OLAP data warehouse** you own | Explain why reports shouldn’t hit OLTP |
| 7 | ☐ Choose a warehouse tool (Snowflake, Synapse, Redshift, BigQuery) | Name two |
| 8 | ☐ Decide the layers: **staging (transient)** then **core** | Explain why staging exists |
| 9 | ☐ Model the core layer as **facts and dimensions** | Split a flat table into fact and dims |
| 10 | ☐ Choose **star schema** (not snowflake) by default | Justify with joins and speed |
| 11 | ☐ Choose an **SCD type** for each dimension (0, 1, 2 or 3) | Pick one for a given scenario |

### Phase C: Build the pipelines

| # | Action | Done when you can… |
| --- | --- | --- |
| 12 | ☐ Build the **ETL pipeline**: extract to staging, transform, load to core | Draw E, T and L |
| 13 | ☐ Do a **full (initial) load** the first time | Explain why it happens once |
| 14 | ☐ Switch to **incremental loading** using a watermark | Describe the Jan 2023 to Jan 2, 2024 example |
| 15 | ☐ Truncate transient staging after each run | Explain what goes wrong if you forget |
| 16 | ☐ Make loads **idempotent** (safe to re-run) *(extra)* | Explain upsert and de-duplication |
| 17 | ☐ **Schedule and orchestrate** the pipelines | Say what Airflow or Data Factory does |

### Phase D: Move to a lake and lakehouse

| # | Action | Done when you can… |
| --- | --- | --- |
| 18 | ☐ Store raw, mixed-format data in a **data lake** | Explain schema-on-read |
| 19 | ☐ Pick **Parquet** (column-based) for analytics files | Explain row vs column storage |
| 20 | ☐ Use **Delta format** for ACID, time travel and schema evolution | Explain the transaction log |
| 21 | ☐ Build a **lakehouse**: lake storage + metadata layer + dimensional models | Explain lake + warehouse = lakehouse |
| 22 | ☐ Organise layers as **bronze, silver, gold** | State the rule of each layer |

### Phase E: Process big data and go cloud

| # | Action | Done when you can… |
| --- | --- | --- |
| 23 | ☐ Use **Spark** for big transformations | Draw driver and workers |
| 24 | ☐ Use **Databricks** so you don’t manage clusters yourself | Explain what it manages for you |
| 25 | ☐ Use **Kafka / Event Hubs** for streaming data | Say when to choose streaming |
| 26 | ☐ Pick one cloud (Azure recommended) and map services across clouds | Name the AWS and GCP equivalents |
| 27 | ☐ Create a **free Azure account** (about $200 credit for 30 days; verify the current offer) | Account is ready for practice |

### Phase F: Assemble and operate the Azure architecture

| # | Action | Done when you can… |
| --- | --- | --- |
| 28 | ☐ Ingest: IoT Hub, Event Hubs, Azure SQL DB, APIs | Explain each source |
| 29 | ☐ Move: **Data Factory** copies data into **ADLS Gen2** bronze | Explain linked connectors and no-change rule |
| 30 | ☐ Transform: **Databricks** takes bronze to silver | Explain the cleaning steps |
| 31 | ☐ Model: **Synapse** builds gold facts and dimensions | Explain star schema in gold |
| 32 | ☐ Serve: **Power BI** dashboards (KPIs) for managers; ML tools for data scientists | Describe the end-to-end flow |
| 33 | ☐ Protect and run: Purview, DevOps (Dev, QA, Prod), Key Vault, Entra ID, Monitor, Cost Management | Say what each does in one line |

### Study actions the presenter recommends

| # | Action |
| --- | --- |
| 34 | ☐ Make notes **with your own drawings and analogies**, and revise from the diagrams |
| 35 | ☐ **Rewatch** the hardest parts (OLTP vs OLAP, SCD types). Nobody absorbs everything in one pass |
| 36 | ☐ **Share what you learned on LinkedIn** (a screenshot plus the keywords you learned). Summarising forces you to revise, and it shows recruiters you are serious |
| 37 | ☐ Follow his separate **end-to-end Azure data engineering project** video to practise the tools hands-on |
