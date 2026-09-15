# Creating a SQL Warehouse — Cluster Size & Scaling Explained Simply (Study Notes)

> Topic: Setting up a SQL Warehouse in the Databricks portal, understanding "Cluster Size" (T-shirt sizes like 2X-Small, X-Small, Small), and the genuinely tricky but important distinction between **Vertical Scaling** and **Horizontal Scaling** as it applies specifically to SQL Warehouses.
> Written in simple, plain language, with Interview Questions and DP-750 style exam questions at the end.

---

## Quick Recap Before We Start

You may already have a **"Starter Warehouse"** automatically sitting in your account — you didn't create it; Databricks auto-creates one by default for every new workspace. It's fine to leave it alone (it's just sitting there, turned off, not costing anything).

---

## Part 1 — Creating a New SQL Warehouse (Simple Steps)

**Step 1** — Go to **Compute → SQL Warehouses → Create SQL Warehouse**.

**Step 2** — Give it a name (anything you like).

**Step 3** — Pick a **Cluster Size**.

---

## Part 2 — What Does "Cluster Size" Actually Mean? (In Simple Words)

Think of a **cluster** as just "a team of machines working together" (you already know this from earlier notes). **Cluster Size** simply answers: **"How many machines (worker nodes) do I want in this team, and how powerful should each one be?"**

Databricks gives you **T-shirt sizes** to pick from, instead of manually choosing exact machine specs:

```
2X-Small  →  X-Small  →  Small  →  Medium  →  ...  →  4X-Large
(smallest,                                              (biggest,
 fewest                                                  most
 machines)                                               machines)
```

⚠️ **Simple English callout — Worker Node**: A worker node is just **one machine** that actually processes part of your query. More worker nodes = more machines working together on your query at the same time.

### Do I need to memorize exactly how many workers each size gives me?
**No — and the instructor says this directly.** These exact numbers (like "2X-Small = 1 worker" or "Small = 2 workers") are **subject to change over time**, and you can always look them up in Databricks' official documentation whenever you actually need to know. **Don't waste effort memorizing this — just know that bigger T-shirt sizes = more/bigger machines.**

---

## Part 3 — The Confusing (But Important) Part: Vertical vs. Horizontal Scaling

This is the trickiest concept in this lecture, so let's go slow and keep it simple.

### First, the normal way people usually think about these terms
- **Vertical scaling** = making ONE machine bigger/more powerful (more RAM, more CPU).
- **Horizontal scaling** = adding MORE machines to work together.

### But in THIS lecture, for SQL Warehouses specifically, the instructor uses these terms slightly differently — and it's important you understand HIS framing for this topic:

#### "Vertical Scaling" here means: making your ONE cluster bigger by picking a bigger T-shirt size
```
2X-Small  →  X-Small
(1 worker)    (2 workers, more powerful driver)

This is called "VERTICAL scaling of the CLUSTER"
— you're making your ONE cluster more powerful overall,
  even though technically it now has more worker machines inside it.
```
⚠️ **Why call this "vertical" if it adds more workers?** Because the instructor is looking at it from **"the whole cluster" point of view** — you still only have **ONE cluster**, just a bigger/stronger version of it. You're not adding a second, separate cluster — you're just leveling up your single cluster's overall power. Think of it as upgrading your one team from a small team to a bigger, stronger team — still just one team.

#### "Horizontal Scaling" here means: adding a SECOND, SEPARATE cluster
```
CLUSTER 1  +  CLUSTER 2
(both handling queries together, side by side)

This is called "HORIZONTAL scaling"
— you now have MULTIPLE separate clusters,
  sharing the workload between them.
```
⚠️ This is genuinely a **different, additional cluster** — not just a bigger version of your existing one. (This setting is called "Min/Max Clusters" — the instructor says this will be explained in full detail in the **next lecture**.)

🌟 **Everyday analogy to make this click**:
- **Vertical scaling (cluster-level)** = upgrading your one delivery truck to a bigger, stronger truck that can carry more packages at once.
- **Horizontal scaling** = instead of one bigger truck, you get a SECOND separate truck, and now two trucks are delivering packages at the same time.

---

## Part 4 — The Golden Rule of Thumb: When to Use Which

This is the single most practical, most important takeaway from this whole lecture.

> **Rule of thumb: One cluster can efficiently handle about 10 concurrent queries at a time.**

### What does "concurrent queries" mean, simply?
The number of people/tools **actively running a query at the exact same moment** — not the total number of users overall, just how many queries are happening simultaneously, right now.

### The key insight: bigger size (vertical) does NOT help with more concurrent users
```
SCENARIO: Your data isn't very big or complex,
          BUT you have 20-30 people trying to query it AT THE SAME TIME.

❌ WRONG FIX: Pick a huge cluster size like "4X-Large"
   → Even with the biggest, most powerful single cluster,
     you STILL only get "1 cluster per 10 concurrent queries" worth
     of comfortable handling — a bigger engine doesn't fix a
     "too many people trying to use ONE truck at once" problem.

✅ RIGHT FIX: Add a SECOND cluster (horizontal scaling)
   → Now you have 2 clusters sharing the load, each handling
     roughly 10 concurrent queries comfortably.
```

🌟 **Everyday analogy**: If a single toll booth is jammed because 30 cars want to pass through at once, making that ONE booth lane wider and fancier doesn't fix the traffic jam nearly as well as simply **opening a second toll booth lane**. More simultaneous "customers" (queries) needs more parallel "lanes" (clusters) — not necessarily a bigger single lane.

### Simple decision guide
| Your situation | What to increase |
|---|---|
| Queries are slow because the DATA itself is large/complex | Increase **Cluster Size** (vertical — bigger T-shirt size) |
| Queries are slow because TOO MANY PEOPLE are querying at once | Increase **number of clusters** (horizontal — Min/Max Clusters, next lecture) |

---

## Part 5 — Auto Stop (Quick Reminder)

Same concept as your cluster notes: you can set the SQL Warehouse to **automatically stop after a period of inactivity** (e.g., 10 minutes) — so you're not paying for it while nobody's using it.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What is "Cluster Size" for a SQL Warehouse?** → A T-shirt size (2X-Small to 4X-Large) that determines how many/how powerful the worker machines in your ONE cluster are.
- **Q: Do I need to memorize exact worker counts per size?** → No — check official documentation if curious; these numbers can change over time.
- **Q: In this lecture's terms, what is "Vertical Scaling"?** → Making your ONE cluster bigger/more powerful by picking a bigger T-shirt size.
- **Q: In this lecture's terms, what is "Horizontal Scaling"?** → Adding a SECOND, separate cluster to share the workload (covered fully via Min/Max Clusters in the next lecture).
- **Q: What is the rule of thumb for concurrent queries?** → Roughly one cluster per 10 concurrent queries.
- **Q: If I have many simultaneous users but not much data, should I pick a bigger cluster size?** → No — a bigger single cluster still only comfortably handles ~10 concurrent queries; you need MORE clusters (horizontal scaling) instead.
- **Q: What does Auto Stop do?** → Automatically shuts down the SQL Warehouse after a set period of inactivity, so you stop being charged.

### One-line mental model
```
Data is big/complex           → go VERTICAL (bigger cluster size)
Too many people at once        → go HORIZONTAL (more clusters)
Rule of thumb: ~10 concurrent queries per cluster
```

---

## Interview Questions & Answers

### 1. "Explain the difference between vertical and horizontal scaling for a SQL Warehouse."

**Answer:** Vertical scaling means increasing the cluster's overall size/power by picking a bigger T-shirt size (e.g., moving from 2X-Small to X-Small) — you still have just one cluster, just a stronger version of it. Horizontal scaling means adding an entirely separate, additional cluster to share the workload, rather than making the existing one bigger — configured via the warehouse's Min/Max Clusters setting.

### 2. "A team reports that their SQL Warehouse queries are slow whenever many analysts run reports at the same time, even though each individual query is simple. What would you recommend, and why?"

**Answer:** I'd recommend increasing the number of clusters (horizontal scaling) rather than the cluster size (vertical scaling). Since the rule of thumb is roughly one cluster per 10 concurrent queries, a large number of simultaneous simple queries is a concurrency problem, not a compute-power problem — a bigger single cluster wouldn't meaningfully help, since it's still just one cluster handling that same concurrency ceiling.

### 3. "Why doesn't picking the largest available cluster size (e.g., 4X-Large) solve a concurrency bottleneck?"

**Answer:** Because cluster size (vertical scaling) increases how much a SINGLE cluster can handle per query in terms of raw power, but it doesn't change the fundamental "roughly 10 concurrent queries per cluster" ceiling. If the real problem is too many simultaneous queries rather than heavy individual queries, only adding more clusters (horizontal scaling) actually relieves that bottleneck.

### 4. "What should a data engineer do to determine the right SQL Warehouse cluster size for their team, given that exact worker-count numbers can change over time?"

**Answer:** Rather than trying to memorize specific worker-count numbers (which the documentation itself states are subject to change), a data engineer should check Databricks' current official documentation for the latest specs when needed, and more importantly, base their sizing decision on actual observed workload behavior — experimenting with cluster size and monitoring query wait times/performance to find the right balance for their specific data size and query complexity.

---

## DP-750 Style Exam Questions & Answers

### Q1.
A SQL Warehouse is experiencing slow query performance because the underlying dataset being queried is very large and complex, but the number of concurrent users is low (typically 2-3 at a time). Which action is MOST appropriate?

A. Increase the number of clusters (horizontal scaling).
B. Increase the Cluster Size / T-shirt size (vertical scaling).
C. Enable Auto Stop with a shorter timeout.
D. Switch the warehouse type from Pro to Classic.

**✅ Correct Answer: B**

**Explanation:** Since the bottleneck here is data size/complexity per query (not concurrency), increasing the Cluster Size (vertical scaling) provides more processing power per query, which directly addresses this specific problem. Horizontal scaling (more clusters) is the appropriate fix for concurrency issues, not raw per-query compute power needs.

---

### Q2.
According to the rule of thumb discussed for SQL Warehouse scaling, approximately how many concurrent queries can a single cluster efficiently handle?

A. 1
B. 10
C. 100
D. Unlimited, regardless of cluster size

**✅ Correct Answer: B**

**Explanation:** The stated rule of thumb is approximately one cluster per 10 concurrent queries — this guideline directly informs whether a scaling problem should be solved with a bigger cluster (vertical) or more clusters (horizontal).

---

### Q3.
An organization has 30 analysts who frequently run SQL queries against Databricks at the same time, though each individual query is relatively lightweight. The current SQL Warehouse uses the largest available cluster size but is still experiencing performance issues. What does this scenario best illustrate?

A. The organization should switch to an even larger cluster size, since no size increase has yet resolved the issue.
B. The organization's problem is concurrency-related, and horizontal scaling (adding more clusters via Min/Max Clusters) is the appropriate solution, since vertical scaling alone does not increase the number of concurrent queries a warehouse can efficiently handle.
C. The organization should disable Auto Stop to resolve the performance issue.
D. This scenario indicates a Unity Catalog permissions misconfiguration.
E. This indicates the warehouse must be switched to Classic type.

**✅ Correct Answer: B**

**Explanation:** This is a textbook example of a concurrency bottleneck rather than a per-query performance bottleneck. Since vertical scaling (bigger cluster size) does not change the roughly "10 concurrent queries per cluster" ceiling, the correct fix is horizontal scaling — adding additional clusters so more concurrent queries can be handled in parallel across multiple clusters rather than queuing up on a single one.

---

### Q4.
What is the primary purpose of "Cluster Size" (T-shirt sizing) when configuring a SQL Warehouse?

A. It determines how many separate clusters will run in parallel to handle concurrent queries.
B. It determines the number and power of worker nodes within a SINGLE cluster.
C. It controls Unity Catalog access permissions for the warehouse.
D. It sets the maximum number of users who can log into the workspace.

**✅ Correct Answer: B**

**Explanation:** Cluster Size configures the compute resources (number/power of worker nodes) within one single cluster — this is the "vertical scaling" lever. The number of separate parallel clusters handling concurrency (option A) is a different, separate setting (Min/Max Clusters, horizontal scaling), not what Cluster Size itself controls.

---

*End of notes. Next lecture: a full deep-dive into Min/Max Clusters — the setting that actually controls horizontal scaling (multiple clusters) for a SQL Warehouse.*
