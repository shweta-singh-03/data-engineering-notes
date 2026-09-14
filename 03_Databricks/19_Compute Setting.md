# Advanced Compute Settings — Access Mode, Spark Config & More (Follow-Along Guide)

> Topic: The "Advanced" section of the Create Compute screen — Access Mode (Standard vs. Dedicated, and the legacy modes now phased out by Unity Catalog), custom Spark configuration, environment variables, logging destinations, and init scripts.
> This is a **hands-on lecture** — numbered follow-along guide with a **Common Doubts** section.

💰 **Cost note**: Nothing here changes cost directly — these are all *behavioral/configuration* settings, not pricing-related. Your earlier Single Node + short auto-termination choices remain your main cost levers, independent of anything covered in this lecture.

⚠️ **Reassurance up front, straight from the lecture**: *"You can literally click on this create button and everything is good... you don't NEED to touch Advanced settings."* This entire section is optional, power-user territory — most of the time, the default (basic) configuration from the previous lecture is all you need.

---

## Part 1 — Access Mode

### The Five Access Modes (but really, just 2 that matter today)

```
                    ACCESS MODE
                        │
        ┌────────────────┼────────────────┐
        ▼                                       ▼
   STANDARD                              DEDICATED
 (~90% of real-world use)              (assigned user/group only)
        │
        └── (also exist, but LEGACY/outdated now: No Isolation,
             Credential Passthrough — replaced by Unity Catalog)
```

### Standard vs. Dedicated

| Access Mode | Simple English | Who can use it? |
|---|---|---|
| **Standard** | The default, most common choice | **Anyone** on the team can attach their notebook to this compute and run their work |
| **Dedicated** | Restricted, locked-down compute | **Only** a specifically assigned user or group can attach to and use this compute |

⚠️ **Important default behavior**: If you select **"Auto"**, it automatically resolves to **Standard** — because Standard covers roughly 90% of real-world scenarios.

🌟 **Everyday example**: Standard compute is like a shared office printer — anyone on the team can walk up and use it. Dedicated compute is like a locked private printer in one specific manager's office — only that person (or their assigned team) has the key.

### Doubt: "When would I actually need Dedicated compute?"
**Answer — worked example from the lecture**: Imagine you've built a very **high-workload, resource-intensive compute** specifically for **machine learning model training or feature building**. This compute would be expensive to run, and you wouldn't want just *anyone* on the team casually attaching to it and running unrelated workloads on your expensive infrastructure. In that scenario, Dedicated compute makes sense.

⚠️ **But here's the honest nuance the instructor adds**: *"You actually do not need dedicated compute to fulfill that requirement — you can even use permissions [to control] who can actually use compute or not."* In other words, Unity Catalog's own **permission system** can already achieve the same access restriction Dedicated compute provides — meaning Dedicated compute is more of a **"nice to know it exists"** option than something you'll reach for often in practice.

### Doubt: "What are 'No Isolation' and 'Credential Passthrough,' and should I use them?"
**Answer**: **No — these are legacy/outdated access modes**, now effectively replaced by modern Unity Catalog capabilities.

⚠️ **Historical context**: Before Unity Catalog existed, Credential Passthrough was how compute accessed data — using a service principal or a user's own account credentials directly, passed through to the compute layer. Now that Unity Catalog exists — combined with the **Access Connector** (which you already set up in earlier lectures!) — this older mechanism simply isn't needed anymore. Unity Catalog + Access Connector handles secure data access far more cleanly.

```
   BEFORE Unity Catalog:                   NOW (with Unity Catalog):
   Credential Passthrough                  Standard / Dedicated access mode
   (service principal or user               + Unity Catalog governance
    credentials passed directly              + Access Connector
    to compute)                              (the exact setup you built
                                               several lectures ago!)
   ⚠️ Legacy, outdated                       ✅ Modern, recommended
```

---

## Part 2 — Spark Configuration

### Simple English
Apache Spark has **many internal configuration settings** you can customize — the lecture's example: `spark.sql.files.maxPartitionBytes`, which controls the **default partition size** Spark uses when processing files (e.g., changing it from a default like 128 MB to something larger, like 512 MB or 1 GB, depending on your workload's needs).

### Doubt: "Why set Spark configs at the CLUSTER level instead of just in my notebook code?"
**Answer**: You absolutely **can** set Spark configs directly in a notebook — but if you set them **once, at the cluster level**, you avoid having to **repeat that same configuration in every single notebook** that uses this compute. It's a "set it once, applies everywhere this compute is used" convenience.

```
   NOTEBOOK-LEVEL config:                    CLUSTER-LEVEL config:
   Must repeat in EVERY notebook               Set ONCE, applies automatically
   that needs this setting                     to EVERY notebook attached
   ❌ Repetitive                               ✅ Set-and-forget
```

---

## Part 3 — Environment Variables

**Simple English**: Standard environment variables — key-value pairs your code can reference. Particularly useful when **deploying to production**, where you often need to handle configuration (like connection strings, feature flags, or environment-specific settings) without hardcoding them directly into your notebook code.

⚠️ Same idea as Spark config: you *can* handle environment variables inside a notebook too, but setting them at the cluster level is generally preferred for cleaner, more maintainable production deployments.

---

## Part 4 — Logging

**Simple English**: Controls **where cluster logs get written** — i.e., where you can go look if you need to debug what happened on this compute.

| Option | What it means |
|---|---|
| **None** | No log destination configured |
| **DBFS** | Databricks File System — Databricks' own internal storage |
| **Volume** | ⚠️ New term — a **governed layer over your Data Lake** (essentially, a Unity-Catalog-managed way of writing arbitrary files, like logs, directly into your governed Data Lake storage) |

⚠️ **Doubt: "What exactly is a 'Volume'?"** This lecture only briefly introduces it as "a governed layer over your data lake" — meaning you can write logs (or really, any files) through Unity Catalog's governance, landing in your actual Data Lake storage. A full, dedicated explanation of Volumes is coming in a future lecture — for now, just recognize it as one of your logging destination options.

---

## Part 5 — Init Scripts

**Simple English**: A script that runs automatically **when the cluster starts up** — used for custom initialization logic specific to whatever application/workload you're building with Apache Spark.

⚠️ This is application-specific — the exact use case depends entirely on what you're building; the lecture doesn't go deep into specific examples here, just introduces that this capability exists.

---

## Part 6 — Why It's Called "Advanced"

⚠️ **Direct takeaway from the lecture**: *"Not every time you will access this thing."* All of Part 1-5 above are genuinely optional, power-user settings — most learners and even many production use cases will simply click **Create** on the basic configuration (from the previous lecture) without ever touching Advanced settings.

---

## Part 7 — Follow-Along: Finalizing Cluster Creation

**Step 1** — After reviewing (or skipping) Advanced settings, click **Create**.

✅ **Checkpoint**: Deployment begins — this takes a **few minutes** (this is the real Classic-compute VM provisioning process, same mechanism behind the slow starts you experienced earlier with your SQL Warehouse).

**Step 2** — Go to **Compute** → refresh the page → your new cluster should now appear.

### Doubt: "Can I actually SEE the underlying Azure infrastructure this creates?"
**Answer**: **Yes.** Since Classic compute deploys real virtual machines inside your own Azure subscription, you can go check the Azure Portal directly and see the actual VMs, disks, and related resources that got created for this cluster — a nice way to connect what you configure in Databricks to the real, physical Azure resources it produces (this directly echoes the "Databricks Architecture" notes from much earlier in the course, where Classic/all-purpose compute lives inside your own cloud account).

---

## 🤔 Common Doubts — Quick Recap

### Doubt: "Do I need to configure Advanced settings for this course?"
**Answer**: No — the lecture explicitly frames these as optional, "know it exists" concepts. Stick with the basic configuration (Policy, Runtime, Worker Type, Single Node, Auto-termination) covered in the previous lecture for all your hands-on work here.

### Doubt: "Is Dedicated access mode the same as restricting who can CREATE compute (from the earlier lecture)?"
**Answer**: No — those are two different permission layers. "Who can CREATE compute" (Admin / Unrestricted permission) controls who can spin up NEW compute at all. "Access Mode: Dedicated" controls who can USE an ALREADY-CREATED compute resource — a completely separate, narrower permission concern.

### Doubt: "Why don't we use Credential Passthrough anymore?"
**Answer**: Because Unity Catalog + the Access Connector (which you set up earlier in this course) now provides a modern, more secure, more manageable way to govern data access — making the older Credential Passthrough mechanism unnecessary for new setups.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What are the two main, currently-relevant Access Modes?** → Standard (anyone can use it — ~90% of cases) and Dedicated (only an assigned user/group can use it).
- **Q: What does "Auto" access mode resolve to?** → Standard.
- **Q: What replaced Credential Passthrough and No Isolation modes?** → Unity Catalog, combined with the Access Connector.
- **Q: Why set Spark configuration at the cluster level instead of per-notebook?** → So you configure it once, and it automatically applies to every notebook attached to that compute — avoiding repetition.
- **Q: What is a "Volume," in the context of logging destinations?** → A governed layer over your Data Lake — a Unity-Catalog-managed way to write files (like logs) directly into governed Data Lake storage (full explanation coming in a later lecture).
- **Q: What is an Init Script?** → A script that runs automatically when the cluster starts, for custom application-specific initialization logic.
- **Q: Do most users need to touch Advanced settings?** → No — they're optional, power-user configurations; the basic setup is sufficient for most needs.
- **Q: Can you see the actual Azure VMs/disks created by a Classic compute cluster?** → Yes — since Classic compute runs inside your own Azure subscription, you can view these resources directly in the Azure Portal.

### One-line mental model
```
Access Mode: Standard (shared, default) vs Dedicated (locked to specific user/group)
Legacy modes (No Isolation, Credential Passthrough) → replaced by Unity Catalog + Access Connector
Spark Config / Env Vars / Logging / Init Scripts → all OPTIONAL, set-once-apply-everywhere conveniences
```

---

## Full Step-by-Step Recap Checklist

- [ ] 1. (Optional) Click "Advanced" on the Create Compute screen to review these settings.
- [ ] 2. Leave Access Mode as "Auto" (resolves to Standard) unless you have a specific need for Dedicated.
- [ ] 3. (Optional) Add any custom Spark configuration key-value pairs.
- [ ] 4. (Optional) Add any environment variables needed.
- [ ] 5. (Optional) Choose a logging destination (None / DBFS / Volume).
- [ ] 6. (Optional) Specify an init script path if your application needs one.
- [ ] 7. Click Create.
- [ ] 8. Wait a few minutes for deployment.
- [ ] 9. Go to Compute → refresh → confirm your cluster now appears.
- [ ] 10. (Optional) Check the Azure Portal to see the actual VM/disk resources created for this cluster.

---

*End of notes. You now have a fully configured, working Classic compute cluster — ready to be used for the rest of your hands-on notebook work in this course.*
