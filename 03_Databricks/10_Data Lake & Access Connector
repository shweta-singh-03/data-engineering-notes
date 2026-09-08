# Setting Up the Data Lake & Access Connector (Follow-Along Guide)

> Topic: Creating the two resources needed for Unity Metastore (from the previous lecture's concepts) — an **ADLS Gen2 Data Lake** (Storage Account) and an **Access Connector for Azure Databricks**, then granting the Access Connector proper permissions via **IAM role assignments**, plus registering the **Event Grid** resource provider.
> This is a **hands-on lecture**, so these notes are a numbered follow-along guide — with a dedicated **"Common Doubts"** section answering exactly the kind of questions a beginner would naturally have at each step, explained clearly and simply.

---

## Prerequisites
- Your `azure-databricks` Resource Group already exists (from the workspace-setup lecture).
- Your Azure Databricks workspace is already deployed.

---

## 💰 Cost & Resource Management for THIS Lecture

| Resource Created | Does it cost money? | How to minimize cost | How to clean up |
|---|---|---|---|
| **Storage Account (Data Lake Gen2)** | ✅ Yes, but **extremely small** — you're charged for (a) the amount of data actually stored (pennies for a learning project), and (b) transactions (reads/writes) — both negligible while learning | Choose **LRS redundancy** (Locally Redundant Storage) — the cheapest replication option, exactly as done in this lecture. Avoid GRS/ZRS unless you have a real production reason. | Delete it along with your resource group when you're done with the course/section |
| **Access Connector for Azure Databricks** | ❌ No — this resource is **free**. It's purely an identity/permission construct, not a billed compute or storage resource. | N/A | Delete along with the resource group; no urgency |
| **Role Assignments (IAM)** | ❌ No — permissions themselves are never billed | N/A | Automatically removed when the underlying resources are deleted |
| **Event Grid registration** | ❌ No — registering a resource *provider* costs nothing by itself. You'd only pay if you later actually create and heavily use Event Grid topics/subscriptions (usage-based, and the free tier covers most learning-scale usage) | N/A for now | Nothing to clean up at the provider-registration level |

⚠️ **Bottom line**: This entire lecture's resources cost you **effectively nothing** — the storage account might add a few cents/rupees per month at most for this scale of learning data. The real cost risk in this course remains **compute/clusters**, not these governance/storage resources.

---

## Part 1 — Follow-Along: Creating the Data Lake (Storage Account)

**Step 1** — Go to your `azure-databricks` Resource Group (search for it, or navigate from Home).

**Step 2** — Click **Create** → search **"storage account"** → select the official **Microsoft** result → **Create**.

**Step 3** — Fill in the form:
- **Resource Group**: same one as before (`azure-databricks`) — must match, so everything stays organized together.
- **Storage account name**: must be **globally unique across all of Azure** (e.g., `azuredatabricksyourname`) — no spaces, no special characters.
- **Region**: keep it consistent with your other resources.
- **Preferred storage type**: **Data Lake Storage Gen 2** (a variant of Blob Storage).
- **Redundancy**: **LRS** (Locally Redundant Storage) — chosen specifically to **keep cost low**; Data Lake storage is already cheap, and LRS is the most budget-friendly redundancy tier.
- **Performance tier**: **Standard** is fine.

**Step 4** — Click **Next** to reach the **Advanced** tab.

**Step 5** — ⚠️ **Enable "Hierarchical Namespace."** This is the single most important checkbox in this entire form.

**Step 6** — Click **Review + Create** → **Create**. Deployment takes only a few seconds.

---

## Part 2 — Follow-Along: Creating the Access Connector

**Step 7** — While the storage account deploys, go back to **Home** → search **"Access Connector for Azure Databricks"**.

**Step 8** — Click on the correct result → **Create**.

**Step 9** — Fill in:
- **Name**: e.g., `azure-databricks-access`
- **Region**: same region as your other resources — no reason to pick a different one.
- Nothing else needs configuring.

**Step 10** — Click **Review + Create** → **Create**.

✅ **Checkpoint**: Go back to your `azure-databricks` resource group — you should now see **three resources**: your Databricks workspace, your Storage Account, and your Access Connector.

---

## Part 3 — Follow-Along: Creating a Dedicated "Metastore" Container

**Step 11** — Click into your **Storage Account** resource.

**Step 12** — Navigate to **Data storage → Containers**.

**Step 13** — Click **+ Container**, name it exactly `metastore`.

⚠️ **Why a dedicated container just for this?** This container is meant to be used **exclusively** by your Unity Metastore — nothing else should ever be stored here. You'll create separate containers later for other purposes (like your actual Bronze/Silver/Gold Medallion data). Keeping the metastore's root storage completely separate and untouched is a clean best practice.

---

## Part 4 — Follow-Along: Granting the Access Connector Permission (IAM Roles)

⚠️ **Critical navigation tip before you start**: Make sure you are on the **Storage Account's main page** (showing the list of Containers) — **NOT** inside a specific container. If you assign the role while a container is selected/open, you'll only grant access to that one container instead of the whole account, and things will mysteriously "not work" later with no obvious error.

**Step 14** — From the Storage Account's main page, go to **Access Control (IAM)**.

**Step 15** — Click **Add → Add role assignment**.

You need to add **FOUR separate roles**, one at a time, following the same pattern each time:

| # | Role Name | What it's for |
|---|---|---|
| 1 | **Storage Blob Data Contributor** | The core permission — lets the Access Connector actually read and write the data files themselves |
| 2 | **Storage Account Contributor** | Broader management-level access on the storage account (needed for certain configuration-level operations, not just data read/write) |
| 3 | **Storage Queue Data Contributor** | Needed because a Storage Account internally also has queue services — relevant for certain event-driven features |
| 4 | **Event Grid Subscription Contributor** | Needed specifically to support **file-driven triggers** — i.e., automatically kicking off a job the moment a new file lands in your data lake (this requires Event Grid to be enabled — covered in Part 5) |

**For EACH of the 4 roles, repeat this exact pattern:**
1. Search for the role name (⚠️ tip: if the full name doesn't appear in the list, type only part of it, e.g., "storage account," and scroll down — this is a known minor UI quirk in Azure).
2. Click **Next**.
3. Under "Assign access to," choose **Managed Identity** (⚠️ NOT "User, group, or service principal" — see the Doubts section below for why).
4. Click **Select members** → choose **Access Connector for Azure Databricks** as the managed identity type → find and select your specific connector (e.g., `azure-databricks-access`).
5. Click **Select** → **Review + assign**.

✅ **Checkpoint**: After all four, go to **Role assignments** tab under IAM — you should see your Access Connector listed four times, once per role.

---

## Part 5 — Follow-Along: Registering the Event Grid Resource Provider

⚠️ **This is a completely separate concept from role assignment** — registering a resource *provider* just tells Azure "yes, I intend to use this type of service in my subscription." Some services (like Event Grid) are **not registered by default**.

**Step 16** — Go to **Home** → search **"Subscriptions"** → click your subscription.

**Step 17** — Go to **Settings → Resource providers**.

**Step 18** — Search for **"Event Grid"** in the list.

**Step 19** — If its status shows **"NotRegistered"**, select it and click **Register**. (If it already shows "Registered," you're already good — nothing to do.)

**Step 20** — Wait for registration to complete (you'll get a notification). ⚠️ If things still seem off afterward, try logging out and back into the Azure Portal — a full refresh sometimes resolves lingering UI state issues after a provider registration.

✅ **Checkpoint**: Once Event Grid shows "Registered," and all four IAM roles are assigned, your Access Connector setup is fully complete — ready to actually be used inside Databricks in the next lecture.

---

## 🤔 Common Doubts — Clear, Simple Answers

### Doubt 1: "Why does the Access Connector need FOUR different roles? Isn't one 'give access' permission enough?"
**Answer**: Because a Storage Account isn't just one simple thing — it's actually a bundle of different sub-services (blob data storage, account-level configuration, queues, and event notifications). Each role unlocks access to one specific sub-service:
- **Storage Blob Data Contributor** → touching the actual files.
- **Storage Account Contributor** → managing account-level settings.
- **Storage Queue Data Contributor** → the internal messaging/queue system.
- **Event Grid Subscription Contributor** → reacting automatically to file events (like "a new file just arrived").

Giving just the first role is enough for basic reading/writing — the other three exist to "future-proof" the connector for more advanced features (like automatic triggers) you may want later.

### Doubt 2: "Why pick 'Managed Identity' instead of 'User, group, or service principal' when assigning the role?"
**Answer**: Because you're granting access to a **resource** (the Access Connector), not to a **person** or a manually-created application identity. A Managed Identity is Azure's built-in, automatically-managed identity system specifically designed for *resources talking to other resources* — no passwords or secrets to manage yourself. "User, group, or service principal" is for granting access to actual people or manually-registered applications — not what's happening here.

### Doubt 3: "I assigned the role but my container still isn't accessible — what did I do wrong?"
**Answer**: The most common mistake: you were **inside a specific container** (like `metastore`) when you clicked "Add role assignment," instead of being on the **Storage Account's main overview/containers list page**. Assigning the role while inside one container only grants access to *that* container, not the whole account. Always double check you're on the account-level page (where you can see the list of all containers) before assigning IAM roles meant to cover the entire storage account.

### Doubt 4: "What's the actual difference between plain Blob Storage and a 'Data Lake' — why does enabling 'Hierarchical Namespace' matter so much?"
**Answer**: Without Hierarchical Namespace, your storage is just a flat container of files with no real folder structure (technically it *looks* like folders in the UI, but under the hood, it's just files with long path-like names). With Hierarchical Namespace enabled, Azure gives you **true, efficient nested folder structures** — meaning you can create folders inside folders (e.g., `bronze/sales/2026/august/`), and operations like renaming or moving a folder are fast and atomic, rather than having to individually touch every single file inside it. This is literally *what turns Blob Storage into "Data Lake Storage Gen2."*

### Doubt 5: "Why do I need a SEPARATE container just for the metastore instead of just using the storage account directly?"
**Answer**: Good data hygiene — keeping this container reserved *exclusively* for Unity Catalog's internal metastore data means you'll never accidentally mix your own project data (Bronze/Silver/Gold tables) with the metastore's internal bookkeeping. It also makes permissions and troubleshooting cleaner: if something ever goes wrong with the metastore, you know exactly which container to investigate, without wading through unrelated business data.

### Doubt 6: "If I forget to register Event Grid, will EVERYTHING about my Data Lake / Access Connector setup break?"
**Answer**: No — only the **event-driven, file-trigger-based features** will fail to work (e.g., automatically kicking off a pipeline the instant a new file lands). Your core ability to read/write data, create tables, and use Unity Catalog normally will work completely fine without Event Grid. It's a "nice to have for later," not a hard blocker for the main setup.

### Doubt 7: "Why choose LRS redundancy instead of something more resilient like GRS?"
**Answer**: LRS (Locally Redundant Storage) keeps 3 copies of your data within a single datacenter — the cheapest redundancy option Azure offers. GRS (Geo-Redundant Storage) additionally copies your data to a second, distant region for disaster-recovery purposes, but costs meaningfully more. For a learning project (and even for many real production workloads without strict disaster-recovery requirements), LRS is a perfectly reasonable, cost-conscious default — which is exactly why the instructor picked it here.

### Doubt 8: "Is 'registering a resource provider' the same thing as 'assigning an IAM role'? They both feel like permission things."
**Answer**: No, they're two unrelated concepts that just happen to both live under "permissions/settings" conceptually:
- **IAM role assignment** = "This specific identity (your Access Connector) is allowed to do X on this specific resource (your storage account)."
- **Resource provider registration** = "This entire Azure subscription is allowed to create/use this category of service (Event Grid) at all." It's a subscription-wide on/off switch, unrelated to any specific identity or resource.

You need **both** for Event-Grid-based features to work: the subscription must be registered for Event Grid AND your specific Access Connector must have the Event Grid role.

---

## Full Recap Diagram

```
   AZURE RESOURCE GROUP: azure-databricks
   ├── Azure Databricks Workspace
   ├── Storage Account (ADLS Gen2 — Hierarchical Namespace ON)
   │      └── Container: "metastore"   ← reserved exclusively for Unity Metastore
   └── Access Connector for Azure Databricks
              │
              │  granted 4 IAM roles on the Storage Account:
              │   1. Storage Blob Data Contributor
              │   2. Storage Account Contributor
              │   3. Storage Queue Data Contributor
              │   4. Event Grid Subscription Contributor
              ▼
   [Access Connector is now fully authorized to read/write
    the Data Lake, and supports future event-driven triggers]

   SEPARATELY (subscription-level, not resource-level):
   Subscription → Resource Providers → Event Grid → Registered ✅
```

---

## Final Revision Cheat Sheet

### Q&A
- **Q: What setting turns plain Blob Storage into a true Data Lake?** → Enabling "Hierarchical Namespace" during storage account creation.
- **Q: What redundancy tier was chosen, and why?** → LRS — the cheapest option, appropriate for cost-conscious/learning setups.
- **Q: What is a "container" in a storage account?** → An isolated location/section within the storage account where you put your data — like a top-level folder.
- **Q: Why create a dedicated "metastore" container?** → To keep Unity Catalog's internal metastore data completely separate from your actual project data.
- **Q: How many IAM roles does the Access Connector need, and what are they?** → Four: Storage Blob Data Contributor, Storage Account Contributor, Storage Queue Data Contributor, and Event Grid Subscription Contributor.
- **Q: Why "Managed Identity" instead of "User, group, or service principal"?** → Because you're granting access to a resource (the Access Connector), and Managed Identity is Azure's purpose-built mechanism for resource-to-resource authentication.
- **Q: What's the #1 mistake that breaks this whole setup?** → Assigning the IAM role while inside a specific container instead of at the storage account's top level.
- **Q: What is "resource provider registration," and is it the same as an IAM role?** → No — it's a subscription-wide switch enabling a whole category of Azure service (like Event Grid); IAM roles are separate, resource-specific permissions.
- **Q: What breaks if Event Grid isn't registered?** → Only event-driven/file-trigger features; core Data Lake and Unity Catalog functionality is unaffected.

---

## Full Step-by-Step Recap Checklist

- [ ] 1. Create a Storage Account in your `azure-databricks` resource group, with Data Lake Storage Gen2, LRS redundancy, Standard tier.
- [ ] 2. Enable **Hierarchical Namespace** on the Advanced tab.
- [ ] 3. Create an **Access Connector for Azure Databricks** in the same resource group and region.
- [ ] 4. Inside the Storage Account, create a container named `metastore`.
- [ ] 5. From the Storage Account's main page (NOT inside a container), go to Access Control (IAM).
- [ ] 6. Add 4 role assignments to the Access Connector (as a Managed Identity): Storage Blob Data Contributor, Storage Account Contributor, Storage Queue Data Contributor, Event Grid Subscription Contributor.
- [ ] 7. Go to Subscriptions → Settings → Resource providers → search "Event Grid" → Register if not already registered.
- [ ] 8. Confirm all 4 role assignments appear under Role assignments.
- [ ] 9. (If needed) log out/in to Azure Portal to refresh state after Event Grid registration.

---

*End of notes. Next lecture: logging into Databricks itself to actually connect these pieces together and complete the Unity Metastore setup.*
