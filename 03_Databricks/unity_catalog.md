# Databricks Unity Catalog — Complete Study Notes

---

## 1. Introduction — Why Unity Catalog Matters

### 1.1 The Big Picture
- Databricks is in very high demand across **data engineering, data analytics, data science, and machine learning** roles. Job portals frequently list "Databricks experience" as a requirement.
- Most learners jump straight to writing PySpark code and skip the **governance layer** that sits underneath every modern Databricks deployment — **Unity Catalog (UC)**.
- **Core idea to remember:** *"If you understand Unity Catalog, you can work with Databricks."* Unity Catalog is called the **backbone of the modern Databricks architecture** — you cannot build a production-grade Databricks solution today without it.
- A few years ago, Databricks used a different system called the **Hive Metastore**. It still exists for backward compatibility, but **99% of new setups use Unity Catalog**. Hive Metastore is now considered *legacy*.

### 1.2 What is Databricks (Quick Refresher)
In simple English: **Databricks is an end-to-end managed platform for data work** — it covers:
- Data engineering
- Data analytics
- Data warehousing
- Machine learning
- Orchestration (scheduling/running pipelines)
- Managed storage/processing

**Key fact:** Databricks itself does **NOT store your data**. It is a **processing engine**, not a storage system. Your actual data lives in a cloud storage account (Azure Data Lake Storage Gen2, AWS S3, or GCP Cloud Storage). Databricks just *processes* it.

Historically, Databricks was simply a managed layer on top of **Apache Spark** — it took away the pain of manually managing Spark clusters, virtual machines (VMs), and cluster managers. Over time it evolved into a full AI/data platform.

### Interview Questions — Section 1
1. **Q: Why is Unity Catalog considered the backbone of Databricks?**
   A: Because it provides the governance layer (access control, lineage, auditing, discovery) that modern Databricks architecture depends on; without it you cannot properly manage or secure data objects across workspaces.
2. **Q: Does Databricks store data itself?**
   A: No. Databricks is a processing engine. Data resides in cloud object storage (ADLS Gen2, S3, GCS); Unity Catalog governs access to it.
3. **Q: What existed before Unity Catalog?**
   A: The Hive Metastore, which is now legacy and used in only a small percentage of modern setups.

---

## 2. What Problem Does Unity Catalog Solve?

### 2.1 The "SQL Database" Analogy
In traditional SQL:
- You create a **database** → create a **schema** → create a **table**.
- Everything (data + metadata) lives inside the same RDBMS system, so governing/querying is simple because the engine owns the data.

In Databricks:
- Data lives **outside** Databricks (in the cloud data lake).
- Databricks needs a special governing layer to know **what catalog, what schema, what table** a piece of data belongs to, and **who can access it**.
- That governing layer = **Unity Catalog**.

### 2.2 Definition
> **Unity Catalog is a centralized data catalog that provides access control, auditing, lineage, quality monitoring, and data discovery capabilities across Databricks workspaces.**

### 2.2.1 🌟 Real-World Analogy: Library vs Warehouse

Think of it like this:

- **Traditional SQL database** = A **small local library**. The librarian (the database engine) owns the building, owns the books, and knows exactly where every book is. If you want a book, the librarian just walks over and gets it. Simple, because everything is in one place, owned by one system.

- **Databricks + Cloud Storage (without Unity Catalog)** = A **giant public warehouse** full of boxes (your data files) spread across multiple buildings (storage accounts/workspaces) owned by different landlords. Databricks (the "processing worker") can go and process items from any box, but there's **no shared master catalog** telling everyone "box 45 in building B contains customer records, and only HR is allowed to open it."

- **Unity Catalog** = A **central inventory management system** that sits above all these warehouses. It keeps one master list of: what's in every box, which building it's stored in, and who is allowed to open which box — no matter which warehouse worker (workspace) is asking.

```
        WITHOUT Unity Catalog                     WITH Unity Catalog
   (each workspace = isolated warehouse)      (one shared inventory system)

  Workspace A --- Warehouse A (own list)          +-------------------+
  Workspace B --- Warehouse B (own list)   ---->   |  Unity Catalog     |
  Workspace C --- Warehouse C (own list)           |  (master inventory)|
                                                    +-------------------+
   No sharing, 3 separate lists                     /        |        \
   to maintain manually                     Workspace A  Workspace B  Workspace C
                                             (all read the SAME inventory)
```

**Example:** Imagine your company has 3 Databricks workspaces — one for the US team, one for the EU team, one for the Data Science team. Without Unity Catalog, each team's tables are stuck in their own workspace. With Unity Catalog, all three workspaces can be attached to the **same metastore**, so the Data Science team can directly query a `sales.customers` table created by the US team — no copying, no duplicate pipelines.

### 2.3 The Five Pillars / Top Features of Unity Catalog

| # | Feature | Meaning (Simple English) | Example |
|---|---------|---------------------------|---------|
| 1 | **Access Control** | Decide who can see which data/tables | Out of 100 tables, only 10 sensitive ones are restricted to Senior Data Engineers/Analysts; the other 90 are open to everyone (juniors, new joiners, seniors). |
| 2 | **Auditing** | Track who ran what query, how long it took, how much compute it used | If someone repeatedly queries sensitive data, you can see exactly what query they ran and when — full transparency. |
| 3 | **Lineage** | Track the "family tree" of data — which table feeds which other table | If a Gold-layer table shows wrong numbers, lineage lets you trace back: Gold table ← Silver table X ← Bronze table Y ← Source table A, so you can pinpoint the root cause quickly instead of spending days investigating. |
| 4 | **Quality Monitoring** | Create dashboards/metrics (like KPIs) tracking query performance and behavior over time | See whether queries are getting slower or faster, track data quality metrics automatically. |
| 5 | **Data Discovery** | See metadata about a table/object without needing to remember everything manually — is it managed/external, what columns exist, where it's stored, etc. | New employee joins a company with 500+ tables — instead of memorizing details, they browse the Data Discovery tab in Unity Catalog. |

### 2.3.1 🌟 Mini Example Combining All 5 Pillars

Imagine you work at a bank, and there's a table called `bank.transactions.customer_ledger`:

```
+-------------------------------------------------------------+
|                     customer_ledger table                    |
+-------------------------------------------------------------+
| Access Control  --> Only "Finance" & "Compliance" groups     |
|                      can view account_balance column         |
| Auditing        --> Log shows "user_priya ran SELECT * at    |
|                      10:03 AM, query took 4.2 sec"            |
| Lineage         --> ledger table <- raw_transactions (Bronze)|
|                      <- bank_feed_files (Source)              |
| Quality Monitor --> Dashboard shows "0 null values, avg query |
|                      time = 2s over last 7 days"              |
| Data Discovery  --> New analyst sees: "This table is EXTERNAL,|
|                      stored in raw container, has 12 columns" |
+-------------------------------------------------------------+
```
This single example shows how all 5 pillars work together on just ONE table.

### 2.4 "Define Once, Secure Everywhere"
This is a favorite principle of Unity Catalog.

**Before Unity Catalog (Old Way — using Hive Metastore):**
```
Workspace 1 ---- ADLS Gen2 Storage A ---- Hive Metastore A (Manage Tables)
Workspace 2 ---- ADLS Gen2 Storage B ---- Hive Metastore B (Manage Tables)
```
Problems:
1. **More workspaces = more metastores to manage** (order of N — the more workspaces, the more admin overhead).
2. **Each metastore has its own separate storage account** → managed data gets scattered across many storage accounts.
3. **No sharing** — Workspace 1 cannot directly access tables created in Workspace 2.

**After Unity Catalog (New Way):**
```
                     +-----------------------+
                     |   ONE Unity Metastore  |
                     | (Global, one per region)|
                     +-----------+-----------+
                            |
        -------------------------------------------
        |                  |                       |
   Workspace 1         Workspace 2             Workspace 3
   (Catalogs)          (Catalogs)              (Catalogs)
```
Benefits:
1. **Only one metastore** manages all managed tables → all stored in a single (or well-organized) storage account.
2. **Catalogs/tables can be shared across workspaces** because they all connect to the same metastore.
3. Plus you automatically get: auditing, lineage, access control, data discovery.

### Interview Questions — Section 2
1. **Q: What are the 5 pillars of Unity Catalog?**
   A: Access Control, Auditing, Lineage, Quality Monitoring, Data Discovery.
2. **Q: What was the main limitation of the pre-Unity-Catalog (Hive Metastore) architecture?**
   A: Each workspace needed its own metastore and storage account (leading to scattered data and no cross-workspace sharing), and no centralized governance existed.
3. **Q: Explain "define once, secure everywhere."**
   A: You define governance rules and catalogs once at the Unity Catalog / metastore level, and all attached workspaces can reuse them without re-defining anything — as long as they share the same Unity Metastore.
4. **Q: Can two workspaces share catalogs before and after Unity Catalog?**
   A: Before: No, each workspace had an isolated Hive Metastore. After: Yes, if they are attached to the same Unity Metastore.

---

## 3. Unity Catalog Object Hierarchy (4 Levels)

Databricks documentation shows a **3 to 4 level naming hierarchy**:

```
Level 0:  METASTORE        (Unity Metastore) — one per region
              |
Level 1:  CATALOG           (≈ "database" in SQL terms)
              |
Level 2:  SCHEMA             (≈ "schema"/"database" within SQL Server/Postgres)
              |
Level 3:  TABLE / VIEW / VOLUME / FUNCTION   (the actual objects)
```

### 3.1 Level 0 — Metastore (a.k.a. "Unity Metastore")
- **Definition:** The metastore is the **top-level container for metadata** in Unity Catalog. It registers metadata about **data and AI assets** (tables, models, permissions, functions, etc.) and the permissions governing access to them.
- **Simple English:** A metastore is just a **central storage location where all the metadata (information ABOUT your data) is kept** — like table names, schema names, column names, catalog names — NOT the actual data itself.
- **Rule:** To use Unity Catalog, a workspace **must have a Unity Catalog Metastore attached**.
- **Rule:** You can only create **ONE metastore per region** (e.g., one for East US).

### 3.2 Level 1 — Catalog
- The catalog is the **first level of the 3-level naming convention**: `catalog.schema.table`.
- **Think of catalog as "database"** in the traditional SQL sense (even though Databricks calls it "catalog" instead of "database" to avoid confusion, since underlying storage terms differ).
- Modern approach uses a **3-level namespace** (catalog → schema → table); older systems just used 2 levels (schema → table).

### 3.3 Level 2 — Schema
- Also known as a "database" in some contexts (confusingly, since catalog is *also* sometimes called database — see note below).
- **Simple analogy:** Just like in SQL Server/Postgres, you create a database, then create a schema inside it (default schema is `dbo` in SQL Server if none specified), then tables inside the schema.
- Example: within a catalog, you might create schemas named **bronze**, **silver**, **gold** (following Medallion Architecture — see Section 8).

> ⚠️ **Naming Confusion Clarified:** Every tool has its own naming convention.
> - Feel free to mentally treat **Catalog = Database**, and then **Schema** sits inside the catalog, and **Table** sits inside the schema.
> - Don't get confused if the official docs say "schemas also known as databases" — just remember the analogy above and move on.

### 3.3.1 🌟 Real-World Analogy: Computer Folder Structure

Think of the Unity Catalog hierarchy exactly like folders on your computer:

```
This PC (Metastore)
   └── D: Drive (Catalog)                  e.g., "sales_catalog"
         └── 2024_Reports folder (Schema)  e.g., "quarterly_schema"
               ├── report1.xlsx  (Table)     e.g., "q1_sales"
               ├── report2.xlsx  (Table)     e.g., "q2_sales"
               ├── images/       (Volume)    e.g., "invoice_scans"
               └── macro.vba     (Function)  e.g., "mask_salary"
```

**Worked Example:**
- Metastore = "US-East Metastore" (one for the whole US-East region)
- Catalog = `retail_catalog` (like a "database" for the retail business unit)
- Schema = `bronze`, `silver`, `gold` (like sub-folders for raw/cleaned/curated data)
- Table = `retail_catalog.bronze.raw_orders`

So when you write:
```sql
SELECT * FROM retail_catalog.bronze.raw_orders;
```
You're literally saying: *"Go to the `retail_catalog` catalog → open the `bronze` schema (folder) → read the `raw_orders` table (file)."*

### 3.4 Level 3 — Objects Inside a Schema
There are **4 types of objects** you can create inside a schema:
1. **Tables** — structured tabular data.
2. **Views** — saved queries on top of tables (behave like tables).
3. **Volumes** — a NEW concept for governing **files** (structured, semi-structured, unstructured) — explained fully in Section 7.
4. **Functions** — reusable SQL functions, used heavily for data masking / security (Section 9).

### Interview Questions — Section 3
1. **Q: What are the 4 layers of Unity Catalog's hierarchy?**
   A: Metastore → Catalog → Schema → (Table/View/Volume/Function).
2. **Q: How many metastores can exist per region?**
   A: Only one Unity Metastore per region.
3. **Q: What is the 3-level naming convention for a table in Unity Catalog?**
   A: `catalog_name.schema_name.table_name`
4. **Q: What are the 4 object types you can create within a schema?**
   A: Tables, Views, Volumes, Functions.

---

## 4. Connecting Unity Catalog to Cloud Storage (Access Connector & Credentials)

### 4.1 The Core Problem
A Unity Metastore needs to **use a cloud storage account** (e.g., ADLS Gen2) to physically store managed data. But the storage account has security — it won't just let *anyone* read/write to it.

### 4.2 The "Security Guard" Analogy
> Imagine your storage account has a **security guard** at the gate. The Metastore walks up and says "I want to store my data here." The guard says, "Who are you? Show me your ID card." Without an ID card, access is denied.

The **ID card = Access Connector**.

### 4.3 Access Connector (Azure-specific term)
- A special Azure resource called **"Access Connector for Azure Databricks."**
- It is granted a role (e.g., **Storage Blob Data Contributor**) on the storage account via **Azure Access Control (IAM) → Add Role Assignment**.
- Once this role is assigned, the connector has permission to read/write data in that storage account.

**Steps to create (Azure):**
1. Go to your Resource Group → Create → search "Access Connector for Azure Databricks."
2. Give it a name (e.g., `databricks-unity-connector`).
3. Create it (takes seconds).
4. Go to your Storage Account → Access Control (IAM) → Add Role Assignment.
5. Search role: **Storage Blob Data Contributor**.
6. Assign it to: **Managed Identity → Access Connector** (select the one you created).
7. Review + Assign.

Now the Access Connector has permission to interact with the storage account.

### 4.4 Credential (Databricks-side "wrapped ID card")
- The Access Connector ID **cannot be shown directly to the metastore for every operation** — you must **register it inside Databricks** as a **Credential**.
- **Simple English analogy:** Earlier you showed the raw ID card directly. Now, you need to "wrap" that ID card into a badge and register it — that registered badge is called a **Credential** in Databricks.

**Steps to create a Credential (in Databricks UI):**
1. Go to **Catalog → External Data → Credentials**.
2. Click **Create Credential**.
3. Give it a name (e.g., `access-connector`).
4. Paste the **Access Connector ID** (same ID you used for the metastore).
5. Add comments (optional) → Create.

### 4.5 External Location
Once a credential exists, you can create **External Locations** — these map a **cloud storage container/path** to Unity Catalog, using the credential for authentication.

- By default, **one external location per container** (max access scope = the container level).
- Example: If you have containers named `raw` and `enriched` in your storage account, you'd create **two separate external locations** — one for each container.

**Steps to create an External Location:**
1. Go to **Catalog → External Data → External Locations → Create**.
2. Provide:
   - **Name:** e.g., `raw`
   - **URL:** `abfss://raw@<storage-account-name>.dfs.core.windows.net/`
   - **Storage Credential:** select the credential created earlier.
3. Click **Test Connection** to confirm it works.
4. Click **Create**.

### 4.5.1 🌟 Real-World Analogy: Airport Security

```
   [Unity Metastore]  = A passenger who wants to board a plane (access storage)
   [Storage Account]  = The airport gate (destination you want to reach)
   [Security Guard]   = Airport security checkpoint
   [Access Connector]  = Your passport (raw identity document)
   [Credential]        = Your boarding pass (passport info REGISTERED with the airline/system)
   [External Location]  = The specific gate number you're allowed to enter (Gate 5 = "raw" container,
                          Gate 6 = "enriched" container)
```

**Example walkthrough:**
1. You (Metastore) have a passport (Access Connector) — proves who you are.
2. But security won't let you through with just a passport — you need a **boarding pass** tied to that passport. That's your **Credential**.
3. Even with a boarding pass, you can only enter the **gate printed on it** — that's your **External Location** (e.g., only the `raw` container, not the `enriched` one, unless you have a separate boarding pass/external location for it).

So if you have data in TWO containers (`raw` and `enriched`), you need **two separate "boarding passes" (external locations)** — one per gate (container) — even though you use the same passport (credential/connector) for both.

### 4.6 Full Connection Flow Diagram
```
 [Unity Metastore] --wants to store data--> [Storage Account]
        |                                         ^
        |  shows "ID card"                        |
        v                                         |
 [Access Connector] --(has IAM role: Storage Blob Data Contributor)--
        |
        | registered inside Databricks as
        v
   [Credential]
        |
        | used by
        v
 [External Location] --maps to--> [Container in Storage Account]
```

### Interview Questions — Section 4
1. **Q: What is an Access Connector used for in Azure Databricks?**
   A: It's an Azure resource that acts like an "identity/ID card," granted IAM roles (like Storage Blob Data Contributor) so Databricks Unity Catalog can securely read/write to a storage account.
2. **Q: What's the difference between an Access Connector and a Credential?**
   A: The Access Connector is the Azure-side identity resource; the Credential is the Databricks-side registration of that connector's ID so Unity Catalog objects can reference it.
3. **Q: What is an External Location?**
   A: A Unity Catalog object that maps a specific cloud storage path/container to a credential, allowing controlled access to that location for creating external tables/volumes.
4. **Q: How many external locations do you typically create per container?**
   A: One per container (this is the maximum scope of access Unity Catalog will use for that location).

---

## 5. Setting Up a Unity Metastore (Full Practical Walkthrough)

### 5.1 Prerequisites Created
1. **Resource Group** (e.g., `databricks-unity`) in Azure, region: US East.
2. **Storage Account** with:
   - Preferred type: **Azure Blob Storage (Gen 2)**
   - Primary workload: **Big Data Analytics** (mandatory — enables hierarchical namespace)
   - Redundancy: **LRS** (cheapest option)
   - **Hierarchical namespace** must be checked (auto-checked if you pick Big Data Analytics workload).
3. **Azure Databricks Workspace**:
   - Pricing tier: **Trial** (Premium features for 14 days, free)
   - **Managed Resource Group**: an auto-created internal resource group where Databricks stores its own infra (VMs, disks, virtual networks). You typically never touch this manually. Good practice: name it something like `managed-<workspace-name>` for easy identification.

### 5.2 Databricks Architecture — Control Plane vs Compute Plane
This is a **very common interview topic**.

```
             CONTROL PLANE                       COMPUTE PLANE
         (Databricks side)                    (Cloud account side)
    +---------------------------+          +---------------------------+
    | Web Application            |          | Virtual Machines (VMs)    |
    | Unity Catalog               |          | Data Lake / Storage       |
    | Query definitions            |          | External Location         |
    | Compute Orchestration         |         |                            |
    +---------------------------+          +---------------------------+
```
- **Control Plane:** everything on the Databricks side — the web UI, Unity Catalog, queries, orchestration logic.
- **Compute Plane (traditional):** the actual VMs/clusters that run your code, plus your cloud storage — these sit on your cloud account side.
- **Serverless Compute (modern):** Databricks has introduced **serverless compute**, which automatically scales using **intelligent workload management (IWM)** and AI-based predictions. In this model, BOTH control plane and compute now sit on the **Databricks side**, and only the **cloud storage** remains on the cloud account side.
- **Benefit of Serverless Compute:** You don't manage cluster size, VM types, node counts, driver size — nothing. Just attach your notebook to serverless compute and run code.

### 5.3 Admin Console vs Normal Workspace Login
- A very common confusion: **"I created the workspace, so I should be the admin, right?"** — **NO.**
- The actual **admin of the workspace is your cloud identity account** (e.g., Azure Entra ID / Azure AD account), NOT your everyday Gmail-style login.
- To find this admin identity: Go to **Entra ID (Azure AD) → Users** — the listed user is the true admin.
- To access the **Account Console** (where you create metastores), you must log in via **`accounts.azuredatabricks.net`** using that Entra ID account (not your normal login).
- First-time login there may prompt password setup/MFA — this is normal.
- Once inside Account Console → **User Management** → select your normal account → **Roles → Account Admin** → Apply. Refresh the workspace, and "Manage Account" option should now appear (may take up to a day to propagate).

### 5.4 Creating the Metastore (Step-by-Step)
1. In Account Console → **Catalog → Metastores → Create Metastore**.
2. Provide:
   - **Name:** e.g., `metastore-us`
   - **Region:** must match your workspace region (e.g., East US)
   - **ADLS Path (optional but recommended):** point to a container/folder dedicated to metastore storage.
     - Format: `abfss://<container>@<storage-account>.dfs.core.windows.net/`
   - **Access Connector ID:** paste your Access Connector's Resource ID here.
3. Click **Create**.
4. **Assign it to your Databricks Workspace** and check **"Enable Unity Catalog."**
5. **Important — Ownership fix:** Go to the metastore → Edit → set the **Admin** to a **Group** (e.g., "admins") instead of your raw Entra ID account, because you'll typically be logging in with your normal account, not the Entra ID account. Add both accounts to the "admins" group via **User Management → Groups**.

> ⚠️ **Why provide ADLS path at metastore creation?** If you don't specify a storage location at the metastore level, then **every catalog you create later MUST specify its own storage location** (otherwise catalog creation fails). Providing it upfront gives you a fallback default.

### 5.5 Default Catalogs After Setup
Once the metastore is attached, by default you'll see:
- `main` — general workspace catalog
- `system` — internal Databricks system tables
- `examples` — sample data catalog
- `hive_metastore` (legacy) — the old system, kept for backward compatibility

### Interview Questions — Section 5
1. **Q: Why is "Big Data Analytics" workload type mandatory when creating the storage account for Databricks?**
   A: Because it auto-enables the hierarchical namespace feature required for ADLS Gen2, which Unity Catalog/Databricks needs.
2. **Q: What is a Managed Resource Group in Azure Databricks?**
   A: An auto-created resource group where Databricks stores its underlying infrastructure (VMs, disks, networking) — not meant to be manually edited.
3. **Q: Who is the actual "admin" of a freshly created Databricks workspace?**
   A: The cloud identity (e.g., Entra ID/Azure AD account) tied to the subscription — not the regular login email used day-to-day.
4. **Q: Explain Control Plane vs Compute Plane.**
   A: Control Plane = Databricks-side management layer (UI, Unity Catalog, orchestration). Compute Plane = where actual processing/VMs and storage happen; with serverless compute, both control and compute now live on the Databricks side, leaving only storage on the cloud side.
5. **Q: What happens if you don't set a storage location at metastore creation?**
   A: You will be forced to provide a storage location every time you create a new catalog.

---

## 6. Storage Location Hierarchy: Metastore vs Catalog vs Schema vs Table (Object) Level

This is one of the **most important and testable concepts** in Unity Catalog.

### 6.1 The Golden Rule
> **The storage location closest to the object (table) always wins (gets priority).** Upper-level storage settings are only used as a *fallback* if no lower-level location is specified.

Priority order (highest to lowest):
```
Table/Object-level location  >  Schema-level location  >  Catalog-level location  >  Metastore-level location
```

### 6.1.1 🌟 Real-World Analogy: Company Dress Code Policy

Think of storage-location precedence like a company's **dress code policy**, which can be set at multiple levels:

```
   Company-wide policy (Metastore)   -->  "Business casual, no restrictions otherwise"
        |
   Department policy (Catalog)       -->  "Engineering: t-shirts OK"
        |
   Team policy (Schema)              -->  "QA team: must wear company polo"
        |
   Individual role rule (Table)      -->  "On-call engineer: must wear formal for client visits"
```

**Rule:** Whatever rule is defined **closest to the individual** (most specific level) is the one that actually applies. If the individual (table) has no specific rule, it falls back to the team rule (schema); if the team has no rule, it falls back to the department rule (catalog); and so on up to the company-wide default (metastore).

This is EXACTLY how Unity Catalog decides where to physically store your table's data — the most specific (closest) location setting always wins, and it "falls back" upward only when a level is left unspecified.

**Concrete Example:**
- Metastore storage → `container/metastore_root/`
- Catalog `sales_catalog` storage → `container/sales_catalog_root/`
- Schema `sales_catalog.gold` storage → `container/gold_root/`
- Table `sales_catalog.gold.revenue` → **no location specified**

➡️ Since the table doesn't specify its own location, Unity Catalog looks at the **next closest level: schema** → finds `gold_root` is defined → **data goes into `container/gold_root/revenue/...`** (schema wins over catalog and metastore, because it's closer to the table).

### 6.2 Scenario 1 — Metastore-Level Storage Only
- No storage location defined at catalog, schema, or table level.
- **Result:** Data for ANY table created under this hierarchy is saved in the **Metastore's own managed data lake location**.

```sql
-- Create a catalog with NO managed location (falls back to metastore storage)
CREATE CATALOG IF NOT EXISTS managed_catalog;

-- Create schema with no location (falls back further up)
CREATE SCHEMA IF NOT EXISTS managed_catalog.managed_schema;

-- Create a plain managed table
CREATE TABLE IF NOT EXISTS managed_catalog.managed_schema.managed_table (
  id INT,
  name STRING
);

INSERT INTO managed_catalog.managed_schema.managed_table VALUES (1, 'Anla'), (2, 'John');

SELECT * FROM managed_catalog.managed_schema.managed_table;
```
Result: data physically lands inside `metastore_root/tables/<table-guid>/...`

### 6.3 Scenario 2 — Catalog-Level Storage Defined
```sql
CREATE CATALOG IF NOT EXISTS external_catalog
MANAGED LOCATION 'abfss://metastore-container@storageacct.dfs.core.windows.net/catalog';

CREATE SCHEMA IF NOT EXISTS external_catalog.managed_schema;

CREATE TABLE IF NOT EXISTS external_catalog.managed_schema.managed_table (id INT, name STRING);
```
- **Result:** Data is now stored inside the **catalog's folder**, NOT the metastore's default location — because the catalog-level location is **closer to the object** and takes priority.

> **Common error you might hit:** `User does not have CREATE MANAGED STORAGE on external location [metastore root location]. PERMISSION DENIED.`
> **Fix:** Go to Account Console → Catalog → Metastore → grant yourself (or an "admins" group) the **Metastore Admin** role, and/or grant `ALL PRIVILEGES` on the relevant External Location.

### 6.4 Scenario 3 — Schema-Level Storage Defined
```sql
CREATE SCHEMA external_catalog.external_schema
MANAGED LOCATION 'abfss://metastore-container@storageacct.dfs.core.windows.net/schema';

CREATE TABLE external_catalog.external_schema.managed_table (id INT, name STRING);
```
- **Result:** Data is now saved inside the **schema's folder** — because schema is even closer to the object than the catalog.

> ⚠️ **Syntax note:** For **CATALOG** and **SCHEMA**, the keyword is `MANAGED LOCATION`. For **TABLE**, the keyword is just `LOCATION`. Mixing these up causes syntax errors.

### 6.5 Visual Summary
```
METASTORE  ---(fallback level 4: lowest priority)
   |
CATALOG    ---(fallback level 3)
   |
SCHEMA     ---(fallback level 2)
   |
TABLE      ---(level 1: HIGHEST priority — wins if specified)
```
Whichever level is **defined closest to the actual table** determines where the real data files get stored. Any unspecified levels above it are simply ignored for that table.

### Interview Questions — Section 6
1. **Q: If both a catalog and a schema have storage locations defined, which one wins for a table with no location specified?**
   A: The schema-level location wins because it's closer to the object than the catalog.
2. **Q: What SQL keyword differs between creating a catalog/schema vs a table for specifying storage?**
   A: `MANAGED LOCATION` for catalog/schema; `LOCATION` for table.
3. **Q: What's the general rule for storage precedence in Unity Catalog?**
   A: The storage location defined closest to the object (table) always takes precedence over higher-level defaults.

---

## 7. Managed Tables vs External Tables

### 7.0 🌟 Real-World Analogy: Rented Apartment vs Your Own House

```
   MANAGED TABLE  =  Living in a RENTED, fully-managed apartment
   -----------------------------------------------------------
   - Landlord (Databricks) decides where the building is, handles
     maintenance, cleaning, repairs (= automatic optimization).
   - If you "move out" (DROP TABLE), the landlord clears out the
     room completely — but there's a 7-day grace period where you
     can call and get your stuff back (UNDROP).
   - You never worry about plumbing/electric (partitioning/tuning).

   EXTERNAL TABLE =  Living in YOUR OWN HOUSE
   -----------------------------------------------------------
   - You (the user) chose the exact plot of land (LOCATION).
   - You own the house — if you "cancel your Databricks membership"
     (DROP TABLE), only the REGISTRATION/PAPERWORK (metadata) is
     cancelled — your actual house (data files) is still standing,
     completely untouched.
   - But YOU are responsible for maintenance (performance tuning).
```

**Example:**
- A retail company stores raw POS (point-of-sale) transaction files that MULTIPLE tools besides Databricks need to read directly (e.g., a legacy reporting tool, an external audit tool). → Use an **External Table**, because those other tools need direct file access even outside Databricks, and you don't want Databricks to ever accidentally delete those files.
- A data science team creates temporary aggregated tables purely for their own dashboards, with no other tool depending on the raw files. → Use a **Managed Table**, because Databricks will handle optimization automatically and there's a safety net (UNDROP) if they make a mistake.

### 7.1 Managed Tables
```
[Metastore] ---- [Managed Data Lake]
      |
  CREATE MANAGED TABLE
      |
  Metadata (catalog.schema.table_name) --> stored in METASTORE
  Actual data (files)                  --> stored in MANAGED DATA LAKE
```
- You do **NOT** provide a location — Databricks decides where to physically store data (inside its managed storage hierarchy).
- **DROP TABLE** on a managed table removes **BOTH** the metadata AND the underlying data files.
  ```sql
  DROP TABLE managed_catalog.managed_schema.managed_table;
  ```
- **Safety net — UNDROP:** Databricks keeps dropped managed table data for **7 days**, after which it's permanently deleted. You can restore it with:
  ```sql
  UNDROP TABLE managed_catalog.managed_schema.managed_table;
  ```
- **Biggest advantage of managed tables:** You don't need to worry about optimization, partitioning, liquid clustering, or performance tuning — **Databricks automatically manages and optimizes** managed table storage for best performance. This is why managed tables are becoming increasingly popular — the old fear of "accidentally losing data" is mitigated by the 7-day undrop window.

### 7.2 External Tables
```
[Metastore] ---- [Managed Data Lake]     (metadata only, no data)
      |
  CREATE EXTERNAL TABLE ... LOCATION '...'
      |
  Metadata (catalog.schema.table_name) --> stored in METASTORE
  Actual data (files)                  --> stored in YOUR OWN EXTERNAL DATA LAKE (you control it)
```
```sql
CREATE TABLE external_catalog.external_schema.external_table (id INT, name STRING)
LOCATION 'abfss://raw@storageacct.dfs.core.windows.net/external_table';

INSERT INTO external_catalog.external_schema.external_table VALUES (1,'x'),(2,'y');
SELECT * FROM external_catalog.external_schema.external_table;
```
- **Key advantage:** **You own the data.** Databricks cannot delete the underlying files even if you drop the table definition.
- **DROP TABLE** on an external table removes **ONLY the metadata** (catalog/schema/table registration) — the actual files **remain untouched** in your storage location, because Databricks doesn't own that storage — you do.
- **Important rule:** An external table's `LOCATION` **overrides everything** — even if metastore, catalog, and schema all have their own storage locations defined, the **table-level `LOCATION` always wins** for external tables, because it is the object-level (most specific) setting. This can be thought of as an extra layer:
  ```
  Object-level (table LOCATION) > Schema > Catalog > Metastore
  ```

### 7.3 Managed vs External — Comparison Table

| Aspect | Managed Table | External Table |
|---|---|---|
| Who controls storage location | Databricks decides | You decide (you provide LOCATION) |
| DROP TABLE effect | Deletes metadata **AND** data | Deletes **only** metadata; data files remain |
| Recovery after drop | UNDROP within 7 days | Not needed — data was never deleted |
| Performance optimization | Automatic (Databricks manages it) | You must manage (partitioning, clustering, etc.) |
| Best use case | You don't need external tool access to raw files, want zero-maintenance performance | You need direct file-level access/control (e.g., other tools reading raw files, strict data ownership/compliance requirements) |

### Interview Questions — Section 7
1. **Q: What happens to underlying data files when you DROP a managed table vs an external table?**
   A: Managed table: both metadata and data files are deleted (recoverable for 7 days via UNDROP). External table: only metadata is deleted; data files remain intact in storage.
2. **Q: Why are managed tables becoming more popular despite the "data deletion" risk?**
   A: Because of the UNDROP command (7-day recovery window) and because Databricks automatically optimizes managed table performance without manual tuning.
3. **Q: If a schema, catalog, and metastore all have storage locations defined, but you create an EXTERNAL table with its own LOCATION — where does the data go?**
   A: Into the external table's own specified LOCATION — table-level location always overrides everything above it.
4. **Q: How do you recover an accidentally dropped managed table?**
   A: `UNDROP TABLE catalog.schema.table_name;` within 7 days of the drop.

---

## 8. Medallion Architecture (Referenced for Lineage Example)

A common modern data engineering pattern with **3 layers**:

```
BRONZE (raw layer)  -->  SILVER (cleansed/enriched layer)  -->  GOLD (curated/business-ready layer)
```
- **Bronze:** Raw ingested data, as-is.
- **Silver:** Cleaned, validated, "enriched" data.
- **Gold:** Final, curated, business-consumable tables (e.g., used directly by BI dashboards/analysts).

**Example use of Lineage:** If a Gold-layer table suddenly shows incorrect numbers, Unity Catalog's **lineage** feature lets you trace: *Gold Table → depends on → Silver Table X → depends on → Bronze Table Y → depends on → Source Table A* — helping you quickly locate the root cause instead of manually investigating for days.

### Interview Questions — Section 8
1. **Q: What are the three layers of Medallion Architecture?**
   A: Bronze (raw), Silver (cleansed), Gold (curated/business-ready).
2. **Q: How does Unity Catalog lineage help debug a Medallion Architecture pipeline?**
   A: It shows the upstream/downstream dependency chain between tables, letting you trace an issue in a Gold table back through Silver and Bronze layers to its root cause.

---

## 9. Unity Catalog Volumes (Governing Files, Not Just Tables)

### 9.1 What is a Volume?
> **Definition (from docs):** *Volumes are Unity Catalog objects, similar to tables/views, representing a logical volume of storage in a cloud object storage location. Volumes provide capabilities for accessing, storing, governing, and organizing files.*

- **Simple English:** A Volume is like a **"governed folder"** inside your catalog/schema hierarchy — used for **files** (CSV, PDF, images, JSON, unstructured/semi-structured data) instead of structured **tables**.
- **Key distinction:**
  - **Tables** → govern **tabular data** (rows/columns).
  - **Volumes** → govern **non-tabular data / files** of ANY format (structured, semi-structured, unstructured).

### 9.1.1 🌟 Real-World Analogy: Library Bookshelves vs Storage Locker

```
   TABLE  = A perfectly organized BOOKSHELF with labeled, numbered
            slots (rows & columns) — great for structured info like
            "Book Title | Author | Year".

   VOLUME = A STORAGE LOCKER where you can dump ANYTHING — loose
            papers (CSV), photographs (images), posters (PDFs),
            even a random USB drive (binary files) — no fixed
            structure required, but it's still tagged with a label
            (catalog.schema.volume_name) so the librarian (Unity
            Catalog) knows it exists and who can open the locker.
```

**Example:** Your company receives scanned invoice PDFs, contract images, and raw sensor log files (`.txt`) that don't fit into rows and columns. Instead of forcing this into a table, you create a **Volume** (e.g., `finance_catalog.invoices.scanned_docs`), dump all these files inside it, and now Unity Catalog can govern (control access to, audit, and discover) these files — exactly like it governs your structured tables.

### 9.2 Why Do We Need Volumes?
Without volumes, if you have a CSV file sitting in cloud storage, you could technically read it directly using its cloud path (e.g., `abfss://...`) with PySpark. But you **cannot govern it through Unity Catalog** this way (no access control, no discovery, no lineage).

Volumes let you **register that file location as a UC object**, so it becomes part of your catalog/schema and inherits all governance benefits.

### 9.3 External Volume (points to an existing folder in cloud storage)
```sql
CREATE EXTERNAL VOLUME external_catalog.external_schema.external_volume
LOCATION 'abfss://raw@storageacct.dfs.core.windows.net/data';
```
- This registers the existing `data` folder (which may already contain files like `dim_airline.csv`) as a Unity Catalog Volume.
- Once created, you can query files directly using UC volume paths:
  ```sql
  SELECT * FROM csv.`/Volumes/external_catalog/external_schema/external_volume/dim_airline.csv`;
  ```
  Volume path format: `/Volumes/<catalog>/<schema>/<volume_name>/<optional_file_name>`

### 9.4 Managed Volume (Databricks manages storage automatically)
```sql
CREATE VOLUME external_catalog.external_schema.managed_volume;
```
- No location needed — Databricks stores whatever you upload inside its managed storage.
- You can upload files via UI: **Catalog → your schema → Volumes → managed_volume → Upload to Volume → Browse**.
- Uploaded files follow the same storage-hierarchy rule discussed in Section 6 (if schema is external, uploaded volume data lands in the external location; if managed, it lands in the managed metastore/catalog storage).

### 9.5 Volume vs Table — Quick Comparison

| Aspect | Table | Volume |
|---|---|---|
| Data type | Structured/tabular (rows & columns) | Any file type — structured, semi-structured, unstructured |
| Example | Employee table with ID/Name/Salary | CSV files, PDFs, images, JSON logs |
| Query method | Standard SQL `SELECT` | Query via file-format functions (e.g., `csv.\`/Volumes/...\``) or read via code |
| Governance | Full UC governance (ACL, lineage, discovery) | Full UC governance (ACL, lineage, discovery) — but for files |

### Interview Questions — Section 9
1. **Q: What is the purpose of a Unity Catalog Volume?**
   A: To bring file-based (non-tabular) data — like CSVs, PDFs, images — under Unity Catalog governance, enabling access control, discovery, and organization just like tables.
2. **Q: What's the difference between an External Volume and a Managed Volume?**
   A: An External Volume points to an existing folder/location you specify; a Managed Volume lets Databricks automatically manage the storage location for uploaded files.
3. **Q: How do you query a CSV file registered as a Volume?**
   A: `SELECT * FROM csv.\`/Volumes/<catalog>/<schema>/<volume>/<file>.csv\`;`

---

## 10. Data Security — Data Masking with Unity Catalog Functions

### 10.1 The Problem
You have a table like this:

| id | name | salary |
|---|---|---|
| 1 | A | 10,000 |
| 2 | B | 20,000 |
| 3 | C | 30,000 |

A team of developers needs to query this table for general use, but the **salary column is confidential**. You:
- **Cannot drop the column** (other logic may depend on it existing).
- **Cannot simply replace values for everyone** (some authorized people — e.g., HR, Directors — DO need to see real values).

**Solution: Data Masking using a Unity Catalog Function.**

### 10.1.1 🌟 Real-World Analogy: ATM PIN Masking

Think of how an **ATM screen** shows your PIN entry: `* * * *` instead of the real digits, unless you're the verified account owner entering them yourself. Data masking works the same way:

```
                     +----------------------------+
   User A (HR)  ---->|  masking(salary) function   |----> Real Salary: $50,000
                     |  checks: is user in "HR"?    |
   User B (Dev) ---->|  Yes -> show real value       |----> Masked: "***"
                     |  No  -> show '***'             |
                     +----------------------------+
```

**Example:** In an e-commerce company, a `customers` table has a `credit_card_number` column.
- **Customer support agents** should see only the last 4 digits: `**** **** **** 1234`.
- **Finance/fraud team** should see the full number.
- A masking function checks `IS_ACCOUNT_GROUP_MEMBER('fraud_team')` — if true, show full number; if false, show masked version. Same table, same column, different results depending on WHO is looking — just like an ATM only shows your real balance to YOU, not to the person standing behind you in line.

### 10.2 What is a Unity Catalog Function (in this context)?
A **Function** is one of the 4 object types under a schema (along with tables, views, volumes). Here, it's used to define **conditional logic** that returns either the real value or a masked value depending on **who is running the query**.

### 10.3 Step-by-Step: Building a Masking Function

**Step 1 — Create the base table:**
```sql
CREATE TABLE external_catalog.external_schema.employee (
  id INT,
  name STRING,
  salary INT
);

INSERT INTO external_catalog.external_schema.employee VALUES
  (1, 'A', 10000),
  (2, 'B', 20000),
  (3, 'C', 30000);
```

**Step 2 — Create a Group (for authorized users):**
- Go to **Settings → Identity and Access → Groups → Manage** (or Account Console → User Management → Groups).
- Create a group (e.g., `admins` or a custom group like `HR_Group`) and add authorized users to it.

**Step 3 — Create the Masking Function:**
```sql
CREATE FUNCTION external_catalog.external_schema.masking(salary_input INT)
RETURN
  CASE
    WHEN IS_ACCOUNT_GROUP_MEMBER('admins') THEN salary_input
    ELSE '***'
  END;
```
- **`IS_ACCOUNT_GROUP_MEMBER('group_name')`** is a **built-in Unity Catalog function** that checks whether the **currently logged-in user** is a member of the specified group.
  - If **YES** → return the real value.
  - If **NO** → return a masked placeholder (e.g., `***`).

**Step 4 — Apply the Function to the Column:**
```sql
ALTER TABLE external_catalog.external_schema.employee
ALTER COLUMN salary SET MASK external_catalog.external_schema.masking;
```

**Step 5 — Test:**
```sql
SELECT * FROM external_catalog.external_schema.employee;
```
- If you (the querying user) are **NOT** a member of the `admins` group → you see `***` instead of real salary values.
- If you recreate the function (`CREATE OR REPLACE FUNCTION ...`) referencing a group you ARE a member of → you now see real salary values.

### 10.4 Diagram
```
                     Query: SELECT * FROM employee
                                  |
                                  v
                 +----------------------------------+
                 |  masking(salary) function runs     |
                 +----------------------------------+
                       |                     |
             IS_ACCOUNT_GROUP_MEMBER      NOT a member
             ('admins') = TRUE               |
                  |                          v
                  v                    returns '***'
           returns real salary
```

### Interview Questions — Section 10
1. **Q: How do you implement column-level data masking in Unity Catalog?**
   A: Create a SQL Function using `CASE WHEN IS_ACCOUNT_GROUP_MEMBER(...)` logic that conditionally returns the real value or a masked placeholder, then apply it to a column using `ALTER TABLE ... ALTER COLUMN ... SET MASK <function>`.
2. **Q: What does `IS_ACCOUNT_GROUP_MEMBER()` do?**
   A: It's a built-in Unity Catalog function that checks if the current logged-in user belongs to a specified group; returns true/false.
3. **Q: Why not just delete the sensitive column instead of masking it?**
   A: Because other processes, reports, or users may need the column to exist (schema/structure), and masking allows selective visibility instead of complete removal.

---

## 11. Catalog Explorer — Exploring Objects in the UI

Navigate: **Catalog icon (left sidebar) → Catalog Explorer**

For any object (Catalog / Schema / Table), you can view tabs such as:
- **Overview** — description (can auto-generate via AI), schema/column list.
- **Sample Data** — preview rows (requires serverless SQL warehouse to be ON).
- **Details** — technical metadata: created date, created by, storage location, storage root, managed vs external status, reader/writer version, etc.
- **Permissions** — who has access.
- **Policies** — row filters, access policies, tag-based access rules.
- **History** — change history / audit trail.
- **Lineage** — upstream/downstream dependency graph; can show a **lineage graph** visualizing the chain of table dependencies.
- **Insights** — usage stats (e.g., table usage in the last 30 days).
- **Quality (Data Quality Monitoring)** — enable to capture data quality metrics/dashboards.

> Note: "Managed Catalog" in the **Details** tab does NOT mean the same thing as "Managed Table." A catalog can have a custom storage location provided AND still be called a "Managed Catalog" — this just means Databricks manages the underlying storage structure, regardless of whether you specified the storage account. Don't confuse this with the Managed vs External **Table** concept from Section 7.

### Interview Questions — Section 11
1. **Q: Where would you check who has access to a specific catalog/table?**
   A: Catalog Explorer → select the object → Permissions tab.
2. **Q: How do you view the dependency chain of a table?**
   A: Catalog Explorer → select the table → Lineage tab → view the lineage graph.
3. **Q: What must be turned on to preview sample data of a table in the UI?**
   A: The serverless SQL warehouse/pool must be turned on.

---

## 12. Practical Setup Checklist (End-to-End Recap)

Use this as your hands-on lab checklist:

1. ✅ Create Azure account (free trial or pay-as-you-go).
2. ✅ Create a **Resource Group**.
3. ✅ Create a **Storage Account** (ADLS Gen2, Big Data Analytics workload, LRS, hierarchical namespace enabled).
4. ✅ Create an **Azure Databricks Workspace** (Trial/Premium tier, managed resource group auto-named).
5. ✅ Create an **Access Connector for Azure Databricks**.
6. ✅ Assign **Storage Blob Data Contributor** role to the Access Connector on the Storage Account.
7. ✅ Create a dedicated **container** in the storage account for metastore usage.
8. ✅ Log into the **Account Console** (`accounts.azuredatabricks.net`) using your Entra ID/cloud admin identity.
9. ✅ Promote your normal login to **Account Admin** (User Management → Roles).
10. ✅ Create the **Unity Metastore**, pointing to the container + Access Connector ID; assign it to your workspace; enable Unity Catalog.
11. ✅ Fix metastore ownership to a **Group** instead of a single raw identity.
12. ✅ Create a **Credential** (registering the Access Connector inside Databricks).
13. ✅ Create **External Locations** for each container you'll use (e.g., `raw`, `enriched`).
14. ✅ Create **Catalogs**, **Schemas**, **Tables** (managed and/or external) as per your project's needs.
15. ✅ Create **Volumes** for file governance (CSV/PDF/etc.).
16. ✅ Apply **Data Masking Functions** for sensitive columns.
17. ✅ Explore everything via **Catalog Explorer** (lineage, permissions, insights, quality).

---

## 13. Final Revision Cheat Sheet

### Quick Definitions
| Term | Meaning |
|---|---|
| **Databricks** | End-to-end managed platform for data engineering, analytics, warehousing, ML; does NOT store data itself — only processes it. |
| **Unity Catalog (UC)** | Centralized governance layer providing access control, auditing, lineage, quality monitoring, and data discovery across workspaces. |
| **Metastore** | Top-level container for ALL metadata (about data + AI assets); one per region; must be attached to a workspace to enable UC. |
| **Catalog** | Level 1 of naming hierarchy; conceptually equals a "database." |
| **Schema** | Level 2; sits inside a catalog; conceptually equals a "schema"/"database" in traditional SQL. |
| **Table / View / Volume / Function** | Level 3 objects living inside a schema. |
| **Managed Table** | Databricks controls storage location & lifecycle; DROP deletes both metadata + data (recoverable 7 days via UNDROP); auto-optimized performance. |
| **External Table** | You control storage location (via LOCATION); DROP deletes only metadata, data files remain; you must manage optimization. |
| **Volume** | UC object governing FILES (any format) instead of tabular data — External Volume (existing location) or Managed Volume (Databricks manages storage). |
| **Function** | Reusable SQL logic object; commonly used for data masking via `IS_ACCOUNT_GROUP_MEMBER()`. |
| **Access Connector** | Azure identity resource ("ID card") granting Databricks permission to access a storage account. |
| **Credential** | Databricks-side registration of an Access Connector, used by external locations/catalogs. |
| **External Location** | Maps a specific cloud storage container/path to Unity Catalog using a credential. |
| **Control Plane** | Databricks-side management components (UI, UC, orchestration, queries). |
| **Compute Plane** | Traditional: cloud-side VMs/clusters + storage. Serverless: compute moves to Databricks side; only storage remains on cloud side. |
| **Medallion Architecture** | Bronze (raw) → Silver (cleansed) → Gold (curated) data layering pattern. |
| **Lineage** | Tracks upstream/downstream dependencies between tables — critical for debugging data issues. |
| **Data Masking** | Conditionally hiding column values from unauthorized users using UC Functions + group membership checks. |

### Storage Precedence (memorize this order!)
```
TABLE-level LOCATION  >  SCHEMA-level MANAGED LOCATION  >  CATALOG-level MANAGED LOCATION  >  METASTORE default storage
```
(Closest level to the object always wins.)

### Managed vs External Table — One-Line Memory Trick
> **Managed = Databricks owns it (deletes data on DROP, but auto-optimized + UNDROP safety net).**
> **External = You own it (DROP only removes metadata, data stays safe in your storage).**

### Key SQL Syntax Quick Reference
```sql
-- Catalog (uses MANAGED LOCATION)
CREATE CATALOG IF NOT EXISTS my_catalog
MANAGED LOCATION 'abfss://container@account.dfs.core.windows.net/path';

-- Schema (uses MANAGED LOCATION)
CREATE SCHEMA IF NOT EXISTS my_catalog.my_schema
MANAGED LOCATION 'abfss://container@account.dfs.core.windows.net/path';

-- Managed Table (no location)
CREATE TABLE IF NOT EXISTS my_catalog.my_schema.my_table (id INT, name STRING);

-- External Table (uses LOCATION)
CREATE TABLE my_catalog.my_schema.ext_table (id INT, name STRING)
LOCATION 'abfss://container@account.dfs.core.windows.net/path';

-- Undrop a managed table
UNDROP TABLE my_catalog.my_schema.my_table;

-- External Volume
CREATE EXTERNAL VOLUME my_catalog.my_schema.ext_volume
LOCATION 'abfss://container@account.dfs.core.windows.net/data';

-- Managed Volume
CREATE VOLUME my_catalog.my_schema.managed_volume;

-- Query a file via Volume
SELECT * FROM csv.`/Volumes/my_catalog/my_schema/ext_volume/file.csv`;

-- Masking Function
CREATE FUNCTION my_catalog.my_schema.mask_fn(input INT)
RETURN CASE WHEN IS_ACCOUNT_GROUP_MEMBER('admins') THEN input ELSE '***' END;

-- Apply mask to column
ALTER TABLE my_catalog.my_schema.my_table
ALTER COLUMN salary SET MASK my_catalog.my_schema.mask_fn;
```

### Rapid-Fire Interview Q&A (Master List)
1. **Unity Catalog is the backbone of what?** → Modern Databricks architecture/governance.
2. **Does Databricks store data?** → No, it only processes; data lives in cloud storage.
3. **What replaced Hive Metastore?** → Unity Catalog (Hive Metastore is now legacy).
4. **How many metastores per region?** → One.
5. **3-level naming convention?** → catalog.schema.table.
6. **4 object types under schema?** → Tables, Views, Volumes, Functions.
7. **What does dropping a managed table do?** → Deletes metadata + data (recoverable 7 days).
8. **What does dropping an external table do?** → Deletes only metadata; data stays.
9. **Storage precedence order?** → Table > Schema > Catalog > Metastore.
10. **What is an Access Connector?** → Azure identity resource granting Databricks storage access.
11. **What is a Credential?** → Databricks-side registration of the Access Connector.
12. **What is an External Location?** → Maps a cloud storage path to UC using a credential.
13. **What is a Volume used for?** → Governing files (non-tabular data) within Unity Catalog.
14. **How do you mask a column?** → Create a Function using `IS_ACCOUNT_GROUP_MEMBER()` logic, then `ALTER TABLE ... SET MASK`.
15. **Control Plane vs Compute Plane?** → Control = Databricks-side management; Compute = processing (cloud-side traditionally, Databricks-side with serverless).
16. **Medallion layers?** → Bronze → Silver → Gold.
17. **What does Lineage help with?** → Tracing root cause of data issues across dependent tables.
18. **Who is admin of a fresh Databricks workspace?** → The cloud identity (Entra ID/Azure AD account) tied to the subscription, not your everyday login.

---

*End of Notes — covers Unity Catalog fundamentals, metastore/catalog/schema/table hierarchy, access connectors & credentials, external locations, storage precedence rules, managed vs external tables, volumes, data masking with functions, and the full practical Azure setup walkthrough.*
