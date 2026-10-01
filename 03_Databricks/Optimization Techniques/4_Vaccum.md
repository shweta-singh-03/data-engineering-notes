# Delta Lake – VACUUM

## 1. Why do we need VACUUM?

We learned that Delta keeps old Parquet files even after:

* UPDATE
* DELETE
* RESTORE

Those old files may no longer be needed for the **current table**, but they can still exist physically in storage.

So over time:

```text
Delta Table
├── Current files
├── Old files
├── Expired files
└── More old files...
```

This can increase storage and operational overhead.

---

# 2. What does VACUUM do?

> **VACUUM physically deletes old Parquet files that are no longer needed.**

Think:

```text
Old / expired files
        ↓
      VACUUM
        ↓
Physically deleted
```

So:

**Delta Log** = tells which files are currently needed
**VACUUM** = physically cleans up files that are no longer needed

---

# 3. Which files does VACUUM delete?

VACUUM does **not** simply delete every old file.

According to the lecture, a file must satisfy both conditions:

```text
1. File is NOT needed by the latest table version
                 +
2. File is older than the retention period
                 ↓
             DELETE
```

The default retention period discussed in the lecture is:

> **7 days = 168 hours**

---

# 4. Why is VACUUM risky?

Because **Time Travel depends on old files**.

Before VACUUM:

```text
Version 5
   ↓
Old files still exist
   ↓
Time Travel can access older versions
```

After VACUUM:

```text
Old files physically deleted
        ↓
Those old versions may no longer be available
        ↓
Time Travel to them won't work
```

So:

> **VACUUM = storage cleanup, but you lose access to historical data whose physical files were deleted.**

---

# 5. Retention period

The lecture uses **7 days as the default guardrail**.

Example:

```sql
VACUUM sales;
```

Conceptually:

> Delete files that are no longer needed and are outside the retention period.

Some organizations may choose a longer retention period, such as **30 days**, when they need a longer Time Travel window.

```text
7 days  → shorter history
30 days → longer history
```

---

# 6. DRY RUN

Before actually deleting anything, you can use:

```sql
VACUUM sales DRY RUN;
```

### What is DRY RUN?

> **It shows which files would be deleted without actually deleting them.**

Think:

```text
DRY RUN
   ↓
"Show me what you would delete"
   ↓
No files deleted
```

This is useful for safely checking what VACUUM will do.

---

# 7. Retention Guardrail

Suppose you try:

```sql
VACUUM sales RETAIN 0 HOURS;
```

You are basically saying:

> "Delete old files immediately."

Databricks has a **retention safety check/guardrail** to prevent dangerously low retention periods.

The lecture shows the check rejecting a very low retention period because it could risk the Delta table and remove the files needed for historical access.

The lecture also shows the setting:

```text
delta.retentionDurationCheck.enabled
```

being used to control that safety check.

### Important

Don't disable this casually.

The instructor specifically recommends experimenting with this kind of operation in a **test environment**, not production.

---

# 8. Real Data Engineering Example

Suppose you have:

```text
sales Delta table
```

You update a record:

```text
Old file → expired
New file → current
```

The old file may still physically exist.

Later:

```text
VACUUM
   ↓
Old unused file removed
```

This reduces unnecessary storage.

---

# 9. VACUUM vs Time Travel

This distinction is very important:

| Concept         | Purpose                            |
| --------------- | ---------------------------------- |
| **Time Travel** | Read an older version              |
| **RESTORE**     | Make an older version current      |
| **VACUUM**      | Physically remove old unused files |

Think:

```text
TIME TRAVEL
→ "Show me the past"

RESTORE
→ "Bring the past back"

VACUUM
→ "Clean up old physical files"
```

---

# ⭐ Super-simple memory trick

```text
Delta Log
→ Keeps track of files

Time Travel
→ Lets me see old versions

Restore
→ Brings an old version back

VACUUM
→ Physically deletes old unused files
```

### Interview one-liner

> **VACUUM is a Delta Lake maintenance command used to physically remove old data files that are no longer required after the configured retention period.**

### ⚠️ Most important warning

> **After VACUUM physically removes files, you may lose the ability to Time Travel to versions that depend on those files.**
