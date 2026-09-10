# Creating Your First Catalog, Schema & Table (Follow-Along Guide)

> Topic: Using the Databricks UI to create a Catalog and Schema (letting them auto-inherit the Metastore's storage location), then creating a Managed Table by simply uploading a CSV file — and physically inspecting the resulting Parquet file + Delta Log to see Delta Lake internals with your own eyes.
> This is a **hands-on lecture** — numbered follow-along guide with a **Common Doubts** section.

💰 **Cost note**: Uploading one small CSV file and creating one tiny Delta table adds a negligible amount of storage (a few KB) to your already-existing Storage Account. **No meaningful cost impact.** ⚠️ This catalog is explicitly built as a throwaway/practice object — the instructor plans to delete it in the next lecture, so don't worry about "cleaning it up perfectly" right now.

---

## Why This Lecture Matters

Up to now, everything (Metastore, Access Connector, External Locations) has been **plumbing** — necessary setup, but not yet the actual day-to-day work. This lecture is the payoff: you finally **create real objects** (a Catalog, a Schema, and a Table) and get to **see, with your own eyes, inside the actual folder structure** that Delta Lake creates — connecting directly back to your earlier "Delta Lake Internals" notes (Parquet + Delta Log).

⚠️ **Important framing from the instructor**: Creating objects via the **UI** (clicking buttons) like this lecture does is great for quick learning/exploration — but in **real production work**, you'll almost always create these objects via **notebooks and scripts** instead, specifically so the exact same setup can be **replicated reliably** across multiple environments (e.g., Dev → QA → Prod). Treat this UI method as a "sandbox," not the production pattern.

---

## Part 1 — Follow-Along: Creating a Catalog via UI

**Step 1** — Go to **Catalog** in the left sidebar.

**Step 2** — Click the **"+"** icon → **Add data** → **Create catalog**.

⚠️ **Doubt: "What if I don't see this option?"** If "Create catalog" isn't available/greyed out, it means your current account doesn't have the right permissions on the Metastore (recall the Account Admin vs. Metastore Admin distinction from two lectures ago!). Since this course already fixed that via the Group-based Metastore Admin assignment, the option should now be enabled.

**Step 3** — Fill in the form:
- **Catalog name**: any name you like (this is a throwaway/practice catalog).
- **Type**: **Standard**.
- **Storage location**: ⚠️ **Leave this blank / don't provide one.**

### Doubt: "Why leave the storage location blank here?"
**Answer**: Because you *want* this catalog to automatically fall back to your **Metastore's root storage location** (the `metastore` container) — exactly the behavior explained in your earlier "Unity Metastore Setup Concepts" notes. If you don't explicitly specify a catalog-level location, Databricks automatically uses whatever is configured at the Metastore level. This is intentional here, for simplicity.

**Step 4** — Click **Create**.

**Step 5** — You'll be prompted to configure permissions — scroll down and grant **"All account users"** access (a simple, permissive choice appropriate for a learning/practice catalog).

**Step 6** — Click **Next** → **Save**.

✅ **Checkpoint**: Your new catalog now appears, already containing two **automatically pre-created schemas**: `default` and `information_schema` (standard for any new catalog).

---

## Part 2 — Follow-Along: Creating a Schema

**Step 7** — Inside your new catalog, click **Create schema**.

**Step 8** — Give it a name (e.g., `raw`).

⚠️ Again — **don't provide a storage location** here either, for the exact same reason: it will automatically inherit from the Catalog (which itself inherits from the Metastore).

**Step 9** — Click **Create**.

✅ **Checkpoint**: You now have both a Catalog and a Schema — the full hierarchy (Metastore → Catalog → Schema) is ready to hold actual tables.

---

## Part 3 — Follow-Along: Creating a Managed Table by Uploading a File

**Step 10** — Click into your new schema (`raw`) → click **Create** → select **Table** (you'll also see other options here like Volume, Model, Metric View — ignore those for now).

**Step 11** — You'll be prompted to **upload a file directly from your computer** — literally any file (CSV, in this example).

**Step 12** — Confirm the target: Catalog = your new catalog, Schema = `raw`, Table name = auto-filled based on your file name (e.g., `bookings`).

**Step 13** — Click **Create table**.

✅ **Checkpoint**: Within moments, Databricks automatically:
1. Reads your uploaded CSV.
2. Infers a schema (column names/types) from it.
3. **Converts it into Delta format** automatically.
4. Registers it as a fully working table you can immediately query.

🌟 **This is the simplest possible way to create a table in Databricks** — no code, no manual schema definition, just drag, drop, and go.

---

## Part 4 — Proving It's a Managed Table, Stored in the Metastore Container

This is the most valuable part of the lecture — actually **verifying**, hands-on, everything you learned conceptually in earlier lectures.

### Doubt: "You said managed tables automatically get stored in the metastore's location — can you actually prove that?"

**Step 14** — Click on your new table → scroll down to find its **"Location"** field.

✅ **Checkpoint**: The location shown will literally contain the word `metastore` in its path — direct, visible proof that this managed table's data landed inside your Metastore's root container, exactly as explained in the "Unity Metastore Setup Concepts" notes.

⚠️ **Reminder**: You should never manually touch/browse this container as a regular practice in real projects — but for learning purposes, it's genuinely useful to look inside it once, which is exactly what happens next.

---

## Part 5 — Follow-Along: Physically Inspecting the Delta Table's Files

**Step 15** — Go to your **Storage Account** in the Azure Portal → open the **`metastore`** container.

**Step 16** — Navigate through the auto-generated folder structure: a top-level folder → a `tables` folder → a folder named after your table.

**Step 17** — Open that table's folder. You'll see exactly what your earlier "Delta Lake Internals" notes predicted:

```
📁 [your table's folder]/
   ├── [weirdly-named-file].parquet     ← your actual data (columnar format)
   └── 📁 _delta_log/
        ├── [entry].json                 ← the transaction metadata
        └── [entry].crc                   ← checksum/integrity file
```

⚠️ **Doubt: "Why does the Parquet file have such a weird/random-looking name?"**
**Answer**: This is standard Delta Lake behavior — Delta auto-generates unique, non-human-readable file names for its underlying Parquet files (rather than naming them after your table). You never need to reference these files by name directly; Delta Lake's transaction log is what tracks and manages them for you.

**Step 18** — Open the `_delta_log` folder → open the `.json` file (click **Edit** or **View** to see its raw content).

✅ **Checkpoint**: You'll see JSON content describing a transaction — specifically, an `"add"` entry, referencing the exact Parquet file name that was just created. This is the transaction log literally recording: *"a new file was added, and here's its name."*

### Connecting this back to your earlier Delta Lake notes
This directly confirms everything from your "Delta Lake Internals" notes:
- **CSV → converted into Parquet** (the columnar, actual data format).
- **A Delta Log folder was created alongside it**, with a JSON entry recording the transaction.
- **A CRC file** also exists — just a checksum/integrity helper, not core metadata.

```
   YOUR UPLOADED CSV
          │
          ▼
   Databricks automatically converts it
          │
          ▼
   ┌─────────────────────────┐
   │  metastore/.../tables/    │
   │  bookings/                │
   │   ├── xxxxx.parquet         │  ← your actual data, columnar
   │   └── _delta_log/            │
   │        ├── 000...json         │  ← "add" transaction entry
   │        └── 000...crc           │  ← checksum file
   └─────────────────────────┘
```
*Caption: What you physically see inside the metastore container after creating a managed table — exactly matching the Parquet + Delta Log structure from the Delta Lake Internals notes, now seen live.*

### Why did the instructor bother showing you this?
⚠️ **Direct quote's intent**: In real day-to-day work, you will **almost never** manually browse into these folders — you interact with tables through SQL/Python, not by digging through raw storage. This was purely a **one-time, "see it to believe it" learning exercise**, meant to cement your understanding of what's actually happening behind the scenes — not something to make a habit of, especially not in production environments.

---

## 🤔 Common Doubts — Quick Recap

### Doubt 1: "Why does the instructor say to use notebooks/scripts instead of the UI for real work?"
**Answer**: UI-based creation isn't easily repeatable — if you need the exact same catalog/schema/table structure in a Dev, QA, and Production environment, manually clicking through the UI three times is error-prone and hard to track/version. Notebooks and scripts (often managed with version control, like Git) let you define this structure as code, so it can be reliably re-run and reproduced across environments.

### Doubt 2: "If I don't specify a storage location for either the Catalog or the Schema, where exactly does the data end up?"
**Answer**: It falls back all the way up the hierarchy to the Metastore's own root storage location (the `metastore` container) — following the exact resolution order covered in earlier notes: Schema → Catalog → Metastore.

### Doubt 3: "Is uploading a file through the UI considered a 'Managed' or 'External' table?"
**Answer**: **Managed.** You handed your raw file over to Databricks and let it decide everything about storage — this is the textbook definition of a Managed Table. The next lecture covers the full Managed vs. External comparison in detail.

### Doubt 4: "Why did my CSV file get converted into Parquet automatically — I never asked for that?"
**Answer**: Because Delta Lake (Databricks' default and recommended table format) **requires** the underlying data to be stored in Parquet — this was covered in your "Delta Lake Internals" notes. Whenever you create a table without specifying otherwise, Databricks defaults to Delta format, and therefore automatically performs this CSV → Parquet conversion behind the scenes for you.

### Doubt 5: "Should I make a habit of browsing these raw storage folders to check on my tables?"
**Answer**: No — this was purely an educational, one-time exercise. In real practice, you should interact with your data through SQL queries and the Catalog Explorer UI, not by manually digging through the underlying storage account. The instructor explicitly notes this is something you'd only look at when actively optimizing table performance — not as routine practice.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What are the two ways given in this lecture to create Databricks objects?** → Via UI (clicking buttons — used here for learning) or via notebooks/scripts (the real production approach, for repeatability across environments).
- **Q: What are the two default schemas auto-created inside any new catalog?** → `default` and `information_schema`.
- **Q: What happens if you upload a CSV and click "Create table" without further configuration?** → Databricks automatically infers the schema, converts the data into Delta (Parquet + Delta Log) format, and registers it as a fully working Managed Table.
- **Q: How can you PROVE a table is managed and stored in the metastore container?** → Check the table's "Location" field — it will show a path containing "metastore."
- **Q: What did opening the actual Parquet + Delta Log folder reveal?** → Exactly what the Delta Lake Internals notes predicted: a Parquet file (the data) + a `_delta_log` folder containing a JSON transaction entry (an "add" record) and a CRC checksum file.
- **Q: Should you regularly browse inside the metastore container in real projects?** → No — this was a one-time learning exercise; in practice, you interact with tables via SQL/Catalog Explorer, only inspecting raw files when actively optimizing performance.

### One-line mental model
```
No storage location specified at Schema or Catalog level
   → falls back to Metastore's root ("metastore" container)
Upload a CSV + Create Table (no extra config) → Managed Table → auto-converted to Delta
   (Parquet file + _delta_log folder with JSON "add" entries + CRC checksum files)
```

---

## Full Step-by-Step Recap Checklist

- [ ] 1. Catalog → "+" → Add data → Create catalog.
- [ ] 2. Name it, set Type = Standard, leave storage location blank.
- [ ] 3. Grant "All account users" access → Next → Save.
- [ ] 4. Inside the new catalog, click Create schema → name it → leave storage location blank → Create.
- [ ] 5. Inside the schema, click Create → Table.
- [ ] 6. Upload any file from your computer (e.g., a CSV).
- [ ] 7. Confirm Catalog/Schema/Table name → Create table.
- [ ] 8. Wait for automatic Delta conversion to complete.
- [ ] 9. Click the table → check its "Location" field → confirm it contains "metastore."
- [ ] 10. (Optional, for learning) Go to the Storage Account → `metastore` container → navigate to `.../tables/[table-name]/` → observe the `.parquet` file and `_delta_log` folder.
- [ ] 11. (Optional) Open the `_delta_log`'s `.json` file → observe the "add" transaction entry referencing your Parquet file.

---

*End of notes. Next lecture: a detailed comparison of Managed vs. External tables — after which this practice catalog will be deleted.*
