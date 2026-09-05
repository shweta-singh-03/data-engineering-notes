# Setting Up Azure Databricks — Resource Groups & Workspace Creation (Follow-Along Guide)

> Topic: Creating your first Azure Databricks workspace — Resources, Resource Groups, Microsoft Entra ID, pricing tiers, and workspace types (Serverless vs. Hybrid).
> This is a **hands-on lecture**, so these notes are a numbered follow-along guide.
>
> ⚠️ **Personalized note for you**: Since you're on a **Pay-As-You-Go Azure account** (your free credits expired), every hands-on/lab section from now on will include a **💰 Cost & Resource Management** section — telling you exactly what costs money, how to minimize it, and how/when to shut things down. This lecture's version is below.

---

## Prerequisites

| Requirement | Why you need it |
|---|---|
| An Azure account (free trial OR Pay-As-You-Go) | You need somewhere to actually create the Databricks resource |
| Azure Portal access (portal.azure.com) | This is where all the clicking happens in this lecture |

⚠️ The instructor used a **paid (Pay-As-You-Go)** account in the video, same as your current setup — so these notes already match your situation well.

---

## Part 1 — Core Concepts You Need First

### What is a "Resource" in Azure?
**Simple English**: A resource is simply **any individual service** you create/use in Azure. If it's Databricks, Azure Data Factory, a Data Lake, a Virtual Machine — literally anything you spin up in Azure — it's called a "resource."

### What is a "Resource Group"?
**Simple English**: Whenever you create a resource in Azure, it has to live inside a **folder-like container** called a **Resource Group**. This keeps related resources organized together.

🌟 **Everyday example**: Think of your Azure account as a filing cabinet, and each Resource Group as a labeled folder inside it. If you're working on "Project A," you'd keep all of Project A's paperwork (resources) in one folder, rather than scattering them loosely across the whole cabinet.

**Why does this matter for this course specifically?** Throughout this course, you'll be creating many resources — Databricks, a Storage Account, various connectors, and more. Grouping them all under **one Resource Group** makes them much easier to manage together — and (important for you) makes it much easier to **delete everything at once** when you're done, to stop being charged.

```
   AZURE ACCOUNT
        │
        ├── 📁 Resource Group: "azure-databricks"
        │      ├── Azure Databricks workspace
        │      ├── Storage Account
        │      ├── Connectors
        │      └── (everything else for this course)
        │
        └── 📁 Resource Group: "some-other-project"
               └── (unrelated resources)
```
*Caption: A Resource Group is a labeled container — grouping all of this course's resources into ONE resource group makes cleanup easy later.*

### What is Microsoft Entra?
**Simple English**: Entra (formerly known as Azure Active Directory) is the **central hub** where Azure manages all your **users, permissions, and service principals** (a "service principal" is essentially an identity used by an application/automation, rather than a human user — you'll learn more about this later in the course). It's also becoming the shared hub for other Microsoft tools like Purview and Fabric.

⚠️ You don't need to dive deep into Entra right now — just know it exists as the central place for identity/access management across Azure.

⚠️ **Reassurance from the instructor**: Azure has *hundreds* of services total, but this course only needs you to work with a small handful of them, all covered as you go. You don't need to learn "all of Azure."

---

## Part 2 — Follow-Along: Creating the Resource Group

**Step 1 — Search for "Resource Group" in the Azure Portal search bar.**
Click on it — you'll see a list of any existing resource groups (if this is a new account, this list will likely be empty).

**Step 2 — Click "Create."**

**Step 3 — Fill in the details:**
- **Resource group name**: `azure-databricks` (or any name you prefer — the instructor used this exact name)
- **Region**: Pick your closest region for convenience while learning (e.g., the instructor used Canada Central). Region choice mostly matters for production latency — for learning purposes, any region is fine.

⚠️ **Cost tip for you**: Creating a Resource Group itself is **completely free** — a Resource Group is just an organizational container, not a billable resource by itself. No cost concern at this step.

**Step 4 — Click "Review + create," then "Create" again.**

✅ **Checkpoint:** Your new Resource Group now appears when you search for it (e.g., search "azure-databricks" in the top search bar). It should currently be **empty** (no resources inside yet).

---

## Part 3 — Follow-Along: Creating the Azure Databricks Workspace

**Step 5 — Inside your new Resource Group, click "Create" (or the "+ Resource" button).**
This opens the **Azure Marketplace** — a catalog of all Microsoft and third-party resources you can create.

**Step 6 — Search for "Databricks."**
⚠️ **Gotcha to watch for**: You'll see a long list of similarly-named services — make absolutely sure you select the **official Microsoft "Azure Databricks"** option, not a third-party look-alike.

**Step 7 — Click "Create" on Azure Databricks (you may need to click "Create" twice — once to open the form, once more inside it).**

**Step 8 — Fill in the configuration form carefully — this step matters a lot:**

| Field | What to enter | Why |
|---|---|---|
| **Resource Group** | Select the resource group you just made (`azure-databricks`) | Keeps this workspace grouped with the rest of your course resources |
| **Workspace name** | Any name, e.g., `azure-databricks-udemy` | Just a label to identify this specific workspace |
| **Region** | Ideally the same region as your Resource Group | Consistency; not strictly mandatory, but best practice |
| **Pricing Tier** | See detailed breakdown below | This affects both features AND cost |
| **Workspace type** | **Hybrid** (not Serverless) | Explained below |
| **Managed Resource Group** | Custom name, e.g., `azure-databricks-managed` | Explained below |

### Understanding the "Pricing Tier" choice

⚠️ **Important — this may look different for you than in the video**, since the instructor was demonstrating on a fresh/eligible account. Depending on your account status, you may see: **Trial**, **Standard**, or **Premium**.

- **Trial**: A **14-day free trial** of the full (Premium-equivalent) feature set. ⚠️ **You will NOT be charged anything during these 14 days.** After 14 days, the workspace access is suspended ("expired") until you manually upgrade it (a simple one-click action — no reconfiguration needed).
- **Premium / Pay-As-You-Go**: You pay only for what you actually use, primarily driven by **compute usage** (i.e., when clusters are actually running) — not by simply having the workspace exist.

**Recommendation (matches the instructor's advice)**: **Always start with the Trial tier if it's available to you**, even on a paid account — it gives you 14 days of full functionality with zero charges, and you can upgrade anytime later with one click if you need more time.

💰 **Cost tip for you specifically**: Since your free Azure credits already expired and you're now Pay-As-You-Go, check whether the **Trial pricing tier option is still available to you** when creating the workspace — some accounts lose access to the Trial tier once they've moved to Pay-As-You-Go. If Trial isn't offered to you, you'll be on Premium by default — this is fine, because **the workspace itself does not cost money just for existing**; charges are driven by compute (covered in the Cost Management section below).

### Understanding "Workspace Type": Serverless vs. Hybrid

This connects directly to the Databricks Architecture notes from earlier in this course:

| Option | What it means | When to pick it |
|---|---|---|
| **Serverless** | "No setup required" — uses Databricks-managed default storage and compute (recall: this is the Serverless Compute Plane, managed by Databricks, not inside your Azure account) | Quick, zero-config start |
| **Hybrid** | Requires access to compute and storage inside YOUR Azure account; supports custom compute (recall: this is the classic "all-purpose compute" architecture, where clusters live inside your Azure account) | ✅ **Chosen in this course** — needed because we WILL be working with Azure-hosted compute directly throughout this course |

**We pick Hybrid** because this course specifically needs you to work with Azure-based compute resources directly (not just the Databricks-managed serverless default).

### Understanding "Managed Resource Group"

**Simple English**: Remember — earlier in this course, you learned that the classic ("all-purpose") compute architecture creates its VM cluster **directly inside your Azure account**. But Azure requires every resource to sit inside *some* Resource Group. So Azure Databricks needs its own dedicated Resource Group specifically to hold all of the compute/infrastructure resources it will automatically create on your behalf (like cluster VMs).

⚠️ **This field is technically optional** — if you leave it blank, Azure will auto-generate a random name for you. But it's **best practice** (and strongly recommended by the instructor) to name it something clearly identifiable, e.g.:
- Main resource group: `azure-databricks`
- Managed resource group: `azure-databricks-managed`

**Why does naming it clearly matter?** In real production environments, you'll have many resource groups — having an obviously-labeled "managed" group makes it instantly clear which one is "your main project stuff" versus "the stuff Databricks manages automatically for itself."

⚠️ **CRITICAL RULE**: **Never manually touch/modify anything inside the Managed Resource Group.** This is exclusively managed by Azure Databricks itself — manual changes here can break your workspace.

**Step 9 — Leave Networking settings as default (unless you have a specific need), then click "Review + create."**

**Step 10 — Azure will validate your configuration. Once validated, click "Create."**

✅ **Checkpoint:** Deployment begins — this takes a few minutes. Once complete, you'll see a notification that your Azure Databricks resource has been deployed.

---

## Part 4 — Follow-Along: Navigating to & Launching Your Workspace

**Step 11 — Go to "Home" in the Azure Portal, then search for your Resource Group again (e.g., `azure-databricks`).**
✅ **Checkpoint:** You should now see **two** resource groups appear — your main one (`azure-databricks`) and the auto-created managed one (`azure-databricks-managed`). This confirms the managed resource group was successfully created.

**Step 12 — Click into your MAIN resource group (not the managed one) and click on your Databricks resource.**
This opens the workspace's configuration/overview page, where you can see: workspace type (Hybrid), managed resource group link, pricing tier, location, and more.

**Step 13 — Click "Launch Workspace."**

✅ **Checkpoint:** This opens the Databricks web UI (the **Control Plane**, from your earlier architecture notes!) in a new browser tab — this is your home page, with all the navigation options on the left-hand side.

⚠️ If you originally picked the **Trial** tier and 14 days have already passed, this step will instead show an **"expired"** message — simply click **"Upgrade"**, which is a one-click action requiring no reconfiguration.


## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What is a "resource" in Azure?** → Any individual service you create — Databricks, Data Factory, a Data Lake, a VM, etc.
- **Q: What is a "resource group"?** → A folder-like container that groups related resources together for easier management.
- **Q: Why put all this course's resources in one resource group?** → Easier management, and easy one-click cleanup/deletion when you're done.
- **Q: What is Microsoft Entra?** → The central hub for managing users, permissions, and service principals across Azure.
- **Q: What's the difference between Trial and Premium/Pay-As-You-Go pricing tiers?** → Trial gives 14 days of full features at zero cost, then requires a one-click upgrade; Premium/Pay-As-You-Go charges you based on actual usage (mainly compute), with no time limit.
- **Q: Serverless vs. Hybrid workspace type — which did we pick, and why?** → Hybrid — because this course needs direct access to Azure-hosted compute (the classic "all-purpose compute" architecture), not just Databricks-managed serverless defaults.
- **Q: What is the "Managed Resource Group"?** → A separate resource group, auto-created and fully managed by Azure Databricks itself, used to hold infrastructure like cluster VMs that Databricks creates on your behalf. Never touch it manually.
- **Q: Does creating a Databricks workspace cost money by itself?** → No — costs are driven by compute (cluster) usage, not by the workspace's mere existence.

### One-line mental model
```
Azure Account → Resource Group (your labeled folder) → Resources inside it (Databricks, Storage, etc.)
Databricks Workspace = FREE to have; real costs come from COMPUTE (clusters) you run inside it
```

---

## Full Step-by-Step Recap Checklist

- [ ] 1. Log into the Azure Portal.
- [ ] 2. Search "Resource Group" → Create → name it (e.g., `azure-databricks`) → pick a region → Review + Create → Create.
- [ ] 3. Confirm the new, empty resource group exists.
- [ ] 4. Inside the resource group, click Create/+Resource → search "Databricks" → select the official Microsoft "Azure Databricks."
- [ ] 5. Fill in: Resource Group (select the one you made), Workspace name, Region (match resource group), Pricing Tier (Trial if available), Workspace type = **Hybrid**, Managed Resource Group = custom clear name (e.g., `azure-databricks-managed`).
- [ ] 6. Leave Networking as default (unless you have specific needs) → Review + Create → Create.
- [ ] 7. Wait for deployment to finish.
- [ ] 8. Navigate to your resource group → confirm TWO resource groups now exist (main + managed).
- [ ] 9. Open your Databricks resource → click "Launch Workspace."
- [ ] 10. Confirm the Databricks web UI (Control Plane) opens successfully.
- [ ] 11. **(Your addition)** Set up an Azure Budget Alert for peace of mind.
- [ ] 12. **(Your addition)** Bookmark the "Cost Management + Billing" page to check in on periodically.

---

*End of notes. Next lecture: exploring the Databricks home page and its navigation options in detail.*
