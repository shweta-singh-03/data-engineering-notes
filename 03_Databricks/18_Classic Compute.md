# Creating Classic Compute (Cluster) — Permissions & Configuration (Follow-Along Guide)

> Topic: Who is allowed to create compute in Databricks, and a full walkthrough of the "Create Compute" configuration screen — policies, Databricks Runtime/LTS, Photon, worker types, Single Node, autoscaling, and the auto-termination cost-saving feature.
> This is a **hands-on lecture** — numbered follow-along guide with a **Common Doubts** section.

🌟 **Personal connection**: This lecture explains the EXACT settings you already configured when you built your own cluster earlier — and even better, it explains the **exact same quota error message format** you hit with your SQL Warehouse ("Estimated available 10, requested 36"), just for general-purpose compute this time.

---

## Part 1 — Who Can Actually CREATE Compute?

### Simple English: Two groups can create compute
1. **Admins** — can do literally anything in a Databricks workspace, including creating compute.
2. **Non-admins with the "Unrestricted cluster/compute creation" permission** — a specific permission that must be explicitly granted to a user account.

⚠️ **Everyone else can only USE compute (attach to it), not create it.**

```
        WHO CAN CREATE COMPUTE?
                  │
        ┌──────────┴──────────┐
        ▼                        ▼
     ADMINS                UNRESTRICTED CLUSTER
  (can do anything)         CREATION permission
                            (granted individually
                             to specific non-admin
                             users)
                  │
                  ▼
         EVERYONE ELSE
    (can only USE existing
     compute, cannot create
     new compute)
```
*Caption: In real organizations, there are usually only 1-2 admins — most developers either get this specific permission, or simply use compute someone else already created.*

⚠️ **Why this restriction exists**: *"Computes are expensive... you should be responsible enough before creating the compute."* Since compute is the primary cost driver in Databricks (as you've directly experienced!), organizations deliberately limit who can spin up new, potentially costly infrastructure — preventing accidental overspending by giving unrestricted creation rights to everyone by default.

---

## Part 2 — Follow-Along: Creating Your First Compute

**Step 1** — Go to **Compute** in the left sidebar. ⚠️ Make sure you're specifically in the **Classic compute** area (not All-Purpose/Job/SQL Warehouse tabs — those are related but distinct sections, as covered in your Compute Types reference notes).

**Step 2** — Click **Create compute**.

### Doubt: "Wait — we already used Databricks without creating any compute. How?"
**Answer**: That was **Serverless compute** — automatically available by default, with zero manual creation needed. This lecture is specifically about **Classic compute**, which you DO need to manually create and configure — a genuinely separate path.

---

## Part 3 — Configuration Walkthrough, Field by Field

### Name
Just a label — pick anything meaningful (e.g., `my-compute`).

### Policy
**Simple English**: A **policy** is a pre-built template that controls what settings you're allowed to configure.

| Policy | What it means |
|---|---|
| **Unrestricted** | Full control — you configure everything from scratch yourself |
| **Personal Compute** | A Databricks-provided template, pre-filled and restricted specifically for individual learning/light use — great for keeping costs low while learning |

⚠️ You *can* create your own custom policies/templates too (not covered in depth here) — but for this lecture, **Unrestricted** is chosen, to configure everything manually and understand each piece.

### Performance section — Machine Learning checkbox
**Doubt: "Should I check the 'Machine Learning' box?"**
**Answer**: Only if you're doing actual ML/data science work. Checking it enables **Databricks Runtime for Machine Learning**, which comes with libraries like **PyTorch** pre-installed, plus other ML-specific optimizations. Since this course is data-engineering focused, **leave it unchecked** — you'd otherwise need to manually install any ML libraries yourself later.

### Databricks Runtime
⚠️ **Simple English callout**: The "Runtime" is a **bundled package** — it includes a specific Spark version, Scala version, Python version, and more — essentially "the software stack" your cluster runs on to actually process your data.

**This lecture uses: 17.3 LTS** — which includes **Spark 4.0** (described as "a big shift" in Apache Spark's evolution; 4.1 and 4.2 exist too, but 4.0 is used here).

⚠️ **What does "LTS" mean, and why pick it?** **LTS = Long-Term Support.** It's **recommended to always pick an LTS runtime version**, because it guarantees stability — your workflows keep running reliably without unexpected breaking changes, unlike newer, potentially less-tested versions.

### Photon Acceleration
⚠️ **This is important and enabled by default.**

**Simple English**: Photon is a **next-generation, C++-based query engine** built by Databricks. Historically, Spark's execution engine ran entirely on the **JVM (Java Virtual Machine)** — Photon adds a much faster, natively-built C++ alternative underneath, specifically to **boost performance and reduce total cost.**

🌟 **Everyday example**: Think of upgrading from a general-purpose translator who has to convert everything through an intermediate language, to a native speaker who understands the material directly — Photon removes a layer of overhead (JVM), running much closer to the hardware for raw speed.

⚠️ **Do you need to configure anything here?** No — it's automatically enabled by default; you just need to know it exists and why it matters.

### Worker Type
**Simple English**: This is where you pick **what kind of machine** each worker node in your cluster should be — i.e., how much RAM and how many CPU cores.

⚠️ **Recommended practice**: **Pick the smallest/lowest possible machine** unless you have a specific reason not to. This lecture uses **`DS3_v2`** — 14 GB RAM, 4 cores.

### Min / Max Workers (Autoscaling)
**Simple English**: This controls **how many machines (worker nodes)** your cluster can scale between:
- **Min** = the baseline number of machines always running when the cluster is on.
- **Max** = the ceiling it can automatically scale UP to, if your workload increases.

🌟 **Everyday example**: Like a restaurant that always keeps 2 staff on shift minimum, but can call in up to 8 more during a sudden rush — scaling capacity to match real-time demand, instead of either being understaffed or wastefully overstaffed at all times.

---

## Part 4 — 🚨 The Quota Error (Exactly What You Already Experienced!)

While configuring Min/Max workers, you may see:

```
This account may not have enough CPU cores to satisfy this request.
Estimated available: 10, requested: 36.
```

### Doubt: "I've seen this exact pattern before — what is this?"
**Answer**: **Yes — this is the exact same Azure vCPU quota mechanism** you already troubleshot for your SQL Warehouse! Recall from your Compute Types notes: **Classic compute (which this cluster IS) draws from your Azure subscription's vCPU quota** — and by default, new Pay-As-You-Go subscriptions get a conservative starting limit (commonly 10 cores per region).

⚠️ **Why does Serverless avoid this entirely?** Because Serverless compute is managed directly by Databricks' own infrastructure — it never touches your Azure subscription's quota at all. This is precisely why the lecture says: *"because nowadays we have serverless compute, so we ignore this step... when we use classic compute, our cloud provider will have those hosted virtual machines... they should have enough capacity."*

### The practical fix used in this lecture: **Single Node**
Instead of requesting multiple worker machines (which multiplies your core requirement — e.g., 8 machines × 4 cores each could easily exceed a small quota), the lecture switches to **Single Node**.

⚠️ **Simple English callout — Single Node**: This means your cluster is just **ONE machine total** — acting as both the coordinating "driver" and the only "worker," with no separate additional worker nodes at all. Perfect for learning, since it requires the smallest possible quota footprint (just this one small machine's cores — e.g., 4 cores, well within a typical starting quota).

```
NORMAL CLUSTER (Min 2, Max 8):                SINGLE NODE:
  Driver + up to 8 worker machines               Just ONE machine total
  = potentially 36+ cores needed                 = ~4 cores needed
  ❌ Can hit quota limits fast                    ✅ Fits comfortably within
                                                     default quotas
```

⚠️ **Real-world guidance**: *"In the real world, you can pick 8 machines, 10 machines, 80 machines, 100 machines, as many as you want — your company will pay the bill."* Single Node is specifically a **learning-phase** choice, not a production limitation — real production clusters scale to whatever the workload genuinely requires.

---

## Part 5 — The Cost-Saving Feature: Terminate Policy

⚠️ **This is one of the most important settings for you personally, given your Pay-As-You-Go account.**

**Doubt: "If I'm not actively using my compute, am I still being charged?"**
**Answer**: **Not if you configure this correctly.** You can set **"Terminate after [X] minutes of inactivity"** (e.g., 10 minutes) — if nothing runs on the compute for that long, it **automatically shuts itself down**, and billing stops.

💰 **This directly matches the cost-management habits from your very first Azure setup notes** — always set the shortest reasonable auto-termination timer.

---

## Part 6 — Tags/Keys (Brief Mention)

You can add **key-value tags** (e.g., `domain: sales`) to categorize your compute — genuinely useful in real organizations running many different computes simultaneously, to track ownership, cost allocation, or purpose. Not critical for learning, but good practice to know.

---

## 🤔 Common Doubts — Quick Recap

### Doubt: "Why did we not need to configure ANY of this for the Serverless compute we used earlier?"
**Answer**: Because Serverless compute is fully pre-provisioned and managed by Databricks itself — there's no VM sizing, no worker count, no quota consideration, and no manual creation step. Classic compute requires you to configure all of this because YOU are the one responsible for provisioning real infrastructure inside your own Azure account.

### Doubt: "Should I always pick Unrestricted policy?"
**Answer**: Not necessarily — for genuine learning/cost-conscious use, the **Personal Compute** policy template (pre-built by Databricks) is specifically designed to keep things simple and cost-controlled. This lecture picked Unrestricted purely for teaching purposes (to show every setting manually).

### Doubt: "Is Photon something I need to manually turn on?"
**Answer**: No — it's enabled by default in modern Databricks Runtimes. You don't need to configure anything; just understand what it's doing behind the scenes (a faster, C++-based execution engine replacing parts of the traditional JVM-based Spark execution).

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: Who can create compute in Databricks?** → Admins, and non-admins who've been explicitly granted the "Unrestricted cluster/compute creation" permission. Everyone else can only use existing compute.
- **Q: What is a "Policy" when creating compute?** → A pre-built template controlling what settings are configurable — e.g., "Unrestricted" (full control) vs. "Personal Compute" (Databricks' simplified, cost-conscious template).
- **Q: What does "Databricks Runtime" bundle together?** → Spark version, Scala version, Python version — the full software stack the cluster runs on.
- **Q: What does "LTS" mean and why is it recommended?** → Long-Term Support — guarantees stability, so your workflows don't unexpectedly break from underlying changes.
- **Q: What is Photon?** → A next-generation, C++-based vectorized query engine that speeds up Spark workflows and lowers cost, replacing parts of the traditional JVM-based execution; enabled by default.
- **Q: What determines the quota error "Estimated available 10, requested 36"?** → The number of workers × cores-per-worker you're requesting exceeds your Azure subscription's available vCPU quota for that region — the exact same mechanism behind your SQL Warehouse quota errors.
- **Q: What is "Single Node," and why use it while learning?** → A cluster consisting of just ONE machine total (acting as both driver and worker) — minimizes core requirements, comfortably fits within default quotas, ideal for learning/light use.
- **Q: How do you avoid being charged when compute sits idle?** → Set a "Terminate after X minutes of inactivity" policy — the compute automatically shuts down and stops billing once idle for that long.

### One-line mental model
```
Compute creation = restricted to Admins / Unrestricted-permission users (cost control)
Classic compute = runs on YOUR Azure quota → Single Node + short auto-termination
                   is the learning-phase sweet spot
Photon = free performance boost, on by default
LTS Runtime = the stable, recommended choice
```

---

## Full Step-by-Step Recap Checklist

- [ ] 1. Confirm you're either an Admin, or have "Unrestricted cluster creation" permission.
- [ ] 2. Go to Compute → Create compute (ensure you're in the Classic compute area).
- [ ] 3. Name your compute.
- [ ] 4. Choose a Policy (Unrestricted for full control, or Personal Compute for a simpler, cost-conscious template).
- [ ] 5. Leave "Machine Learning" unchecked (unless doing actual ML work).
- [ ] 6. Select an LTS Databricks Runtime (e.g., 17.3 LTS).
- [ ] 7. Confirm Photon Acceleration is enabled (default).
- [ ] 8. Pick the smallest/lowest Worker Type available.
- [ ] 9. If you hit a quota error on Min/Max workers, switch to **Single Node**.
- [ ] 10. Set a short "Terminate after X minutes of inactivity" value (e.g., 10-20 min).
- [ ] 11. (Optional) Add tags/keys for categorization.
- [ ] 12. Create the compute.

---

*End of notes. Next lecture: advanced compute settings — going beyond this basic configuration.*
