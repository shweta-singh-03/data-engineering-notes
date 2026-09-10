# External Locations & Storage Credentials (Follow-Along Guide)

> Topic: Packaging together a "path + permission" so Databricks (and anyone using your workspace) can directly read/write a Data Lake container — via **Storage Credentials** and **External Locations**. Includes a real troubleshooting story: hitting a permissions error and discovering the difference between an **Account Admin** and a **Metastore Admin**.
> This is a **hands-on lecture** — numbered follow-along guide with a **Common Doubts** section.

💰 **Cost note**: Everything in this lecture is pure configuration (credentials, permissions, group membership) — no new billable Azure resources are created. **No cost impact.**

---

## Why This Topic Matters (The Problem Being Solved)

You already know that **Metastore ↔ Data Lake** communication happens via the Access Connector (covered two lectures ago). But that connection is specifically for the Metastore's own root storage.

**New problem**: What if **you** (or anyone using Databricks day-to-day) want to directly read/write data in the Data Lake — not just let the Metastore quietly manage its own root folder, but actually work with your own containers (like a `raw` container for your Bronze/Silver/Gold data)?

⚠️ You *could* technically provide the connection details manually every single time you need access — but since you'll be reading/writing data constantly (maybe multiple times a day), that's impractical. You need to **package** this "how to connect" information **once**, into a reusable object.

🌟 **Everyday example**: Think of this like saving a Wi-Fi password on your phone. You *could* type the password every single time you want to connect — but instead, you save it once, and your phone automatically reconnects whenever needed. An External Location + Credential is exactly this: a saved, reusable connection package.

```
   METASTORE ↔ DATA LAKE                    DATABRICKS USERS/COMPUTE ↔ DATA LAKE
   (already set up, previous lecture)        (NEW — what this lecture sets up)
        via Access Connector                       via External Location + Credential
```
*Caption: Metastore-to-storage and User/Compute-to-storage are two SEPARATE connections — this lecture builds the second one.*

---

## Part 1 — The Two Objects You'll Create

### 🔑 Storage Credential
**Simple English**: A Storage Credential is just Unity Catalog's way of **wrapping your existing Access Connector** into an object it can reference and reuse. It's not a brand-new permission system — it's literally just "here's my Access Connector, registered as a reusable credential object."

### 📍 External Location
**Simple English**: An External Location **combines** a Storage Credential with a **specific path** (a specific container in your storage account) — the full "package" that lets Databricks actually read/write that exact location.

```
   STORAGE CREDENTIAL (wraps your Access Connector)
                    +
   A SPECIFIC PATH (abfss://container@storageaccount.dfs.core.windows.net/)
                    =
   EXTERNAL LOCATION  (the complete, reusable "connect here" package)
```
*Caption: A Credential alone isn't enough — it needs to be paired with a specific path to become a usable External Location.*

⚠️ **Order matters**: Always create the **Credential first**, then the **External Location** that references it.

---

## Part 2 — Follow-Along: Creating the Storage Credential

**Step 1** — In your Databricks workspace, go to **Catalog → Connect → External Data → External Locations** (or similar path depending on UI version) — this page lets you create both Credentials and External Locations.

**Step 2** — Go to the **Credentials** tab first.

⚠️ You'll likely already see one credential auto-listed — this is the managed identity automatically created for your **Managed Resource Group**. Don't touch that one; you're creating your own, separate credential.

**Step 3** — Click **Create credential**:
- **Storage credential type**: **Azure Managed Identity**
- **Credential name**: e.g., `my-credential`
- **Access Connector ID**: paste your Access Connector's **Resource ID** here.
- ⚠️ Do **NOT** provide the "Managed Identity ID" field by mistake — that's a different field for a different scenario.

**Step 4** — Click **Create**.

✅ **Checkpoint**: Your credential now appears in the Credentials list.

---

## Part 3 — Follow-Along: Creating External Locations

**Step 5** — Go to **Connect → External Location**.

### Discovery: The Metastore container already has one!

**Step 6** — Try creating an external location named e.g. `metastore_ext`, pointing at your `metastore` container:
```
abfss://metastore@azuredatabricksname.dfs.core.windows.net/
```
⚠️ **Error you'll likely hit**: *"Invalid path — overlaps with an existing external location."*

**What this means**: When you created your Metastore in the previous lecture (and gave it a root ADLS Gen2 path), Databricks **automatically created an External Location for that container already**, behind the scenes. You don't need to (and can't) create a duplicate one for the same path.

✅ **Verify this**: Go to **Catalog → External Data → External Locations** in the **Account Console** — you'll find one already listed, tied to your metastore's storage path.

### Creating a NEW External Location — for your OWN data (e.g., a "raw" container)

**Step 7** — First, go create a new container in your Storage Account (outside the scope of this lecture's transcript, but implied) — e.g., name it `raw`. ⚠️ This is separate from the `metastore` container — remember, that one is reserved exclusively for Unity Catalog's internal use, never your own project data.

**Step 8** — Back in Databricks, go to **Connect → External Location → Create location**:
- **Name**: e.g., `raw`
- **URL**: 
```
abfss://raw@azuredatabricksname.dfs.core.windows.net/
```
- **Storage credential**: select the credential you created earlier (`my-credential`).

**Step 9** — Click **Create**.

---

## Part 4 — 🚨 The Real Error You'll Likely Hit (and How to Fix It)

### The error
```
User does not have CREATE EXTERNAL LOCATION on Metastore [your-metastore-name]
```

### Doubt: "But I'm literally the admin — I created this whole workspace! Why am I being denied?"

**Answer — this is the most important insight in this lecture**: Being an **Azure Databricks Account Admin** (workspace-level admin) is **NOT the same thing** as being a **Metastore Admin** (a separate role, scoped specifically to that one Metastore object).

```
   ACCOUNT ADMIN                          METASTORE ADMIN
   (manages the whole Databricks           (manages permissions/objects
    ACCOUNT — workspaces, users,            specifically WITHIN one
    billing, etc.)                          Metastore — catalogs, external
                                             locations, credentials, etc.)
   These are TWO DIFFERENT ROLES — being one does NOT automatically make you the other!
```

**Step 10** — To check who your Metastore Admin actually is: go to **Account Console → Catalog → [your Metastore] → look for "Metastore Admin."**

⚠️ In this lecture's case, the Metastore Admin turned out to be the instructor's **long, auto-generated admin email** (the same "real admin" account from the previous lecture) — NOT the everyday Gmail-linked account being used day-to-day.

### First (incomplete) attempt at a fix
**Step 11** — Click **Edit** next to Metastore Admin → **Remove** the current admin → assign a **different individual user** instead (e.g., switch it directly to the everyday account).

⚠️ **Problem with this "fix"**: Now the *original* admin account (the long email) loses metastore-admin rights, while only the *new* individual user has it. This just **shifts** the problem to a different single person — it doesn't actually solve the underlying issue of needing **multiple people** to reliably have this access.

### The REAL fix: Use a Group, not an Individual

**Step 12** — Go to **Account Console → User Management → Groups**.

**Step 13** — Check if a group like `admins` already exists (many accounts have one by default). If not, create a new group.

**Step 14** — Click into the group → **Add members** → add **all** the accounts that should have admin rights (e.g., both your everyday account AND your long admin account).

⚠️ **Cleanup tip while you're here**: If you see old/unused test accounts cluttering the group, feel free to remove them — no harm in tidying up.

**Step 15** — Go back to **Account Console → Catalog → [your Metastore] → Edit Metastore Admin** → this time, instead of picking an individual email, select your **Group** (e.g., `admins`).

**Step 16** — Click **Save**.

✅ **Checkpoint**: Now **everyone** who is a member of that group is automatically a Metastore Admin — future team members can simply be added to the group, rather than repeatedly reconfiguring this setting one person at a time.

**Step 17** — Go back and retry creating your External Location (Step 8 again) — it should now succeed without any error.

✅ **Final Checkpoint**: You should now see **two** External Locations: one auto-created for your `metastore` container, and one you manually created for `raw` (or whichever name you chose). You can even rename either one directly in the UI if you want clearer naming.

---

## 🤔 Common Doubts — Clear, Simple Answers

### Doubt 1: "Why do we need an External Location if the Access Connector already has permission to read/write the storage?"
**Answer**: The Access Connector handles the **Azure-level permission** ("yes, this identity is allowed to touch this storage account"). The External Location handles the **Unity Catalog-level registration and governance** — it's what lets Databricks *users* and *table/volume definitions* actually reference and use that storage location, with Unity Catalog's access control, auditing, and lineage layered on top. Without registering it as an External Location, Unity Catalog doesn't know this path exists as something it should govern.

### Doubt 2: "What's actually the difference between a Credential and an Access Connector — aren't they the same thing?"
**Answer**: The Access Connector is the actual **Azure resource** (a managed identity) that holds real permissions on your storage account. The **Storage Credential** is simply Unity Catalog's own internal object that **references** that Access Connector, so Unity Catalog objects (like External Locations) have something to point to. Think of the Access Connector as "the actual keys," and the Credential as "the labeled keychain that Unity Catalog uses to grab those keys when needed."

### Doubt 3: "Why did creating an external location for the 'metastore' container throw an 'overlap' error?"
**Answer**: Because it already existed — automatically created by Databricks the moment you gave your Metastore a root ADLS Gen2 path during its creation (previous lecture). Unity Catalog doesn't allow two External Locations to point at the same overlapping path, so trying to manually create a duplicate is rejected.

### Doubt 4: "I'm the Databricks Account Admin — why can't I create an External Location?"
**Answer**: Because Account Admin and Metastore Admin are two separate, independently-assigned roles. Account Admin controls account-wide settings (workspaces, billing, users). Metastore Admin specifically controls permissions and object-creation rights **within one specific Metastore** (catalogs, external locations, credentials, etc.). You must explicitly be assigned as (or be part of a group assigned as) the Metastore Admin to create objects like External Locations.

### Doubt 5: "Why use a Group instead of just assigning a single person as Metastore Admin?"
**Answer**: Because assigning a single individual creates a fragile setup — the moment you switch it to a different person, whoever had it before loses access, and you're back to a single point of failure/bottleneck. A Group lets you manage a whole team's access in one place: add someone to the group, and they instantly gain Metastore Admin rights; remove them, and access is revoked — without ever having to touch the Metastore's admin setting itself again.

### Doubt 6: "What does `abfss://` actually mean?"
**Answer**: It stands for **Azure Blob File System Secure** — it's the specific URI protocol/scheme used to reference paths inside Azure Data Lake Storage Gen2, in the format:
```
abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<optional-path>
```

### Doubt 7: "Do I need a separate External Location for every single container (raw, bronze, silver, gold, etc.)?"
**Answer**: Yes — each container you want Unity Catalog to be able to govern/reference needs its own registered External Location, since each one is a distinct path. The `metastore` container's External Location was auto-created for you; you'll need to manually create one for each additional container you use for your actual project data.

---

## Full Recap Diagram

```
                    UNITY CATALOG (Metastore)
                              │
              ┌────────────────┴────────────────┐
              ▼                                     ▼
     STORAGE CREDENTIAL                    (wraps the Access Connector —
     ("my-credential")                      the actual Azure identity/permission)
              │
              │  used by
              ▼
     EXTERNAL LOCATIONS:
       ├── "metastore_ext"  → auto-created → points to the metastore container
       └── "raw"            → manually created by you → points to your raw container

   RESULT: Databricks users/compute can now directly read/write BOTH
   the metastore's root storage AND your own project containers,
   all governed and tracked by Unity Catalog.
```

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What is a Storage Credential?** → A Unity Catalog object that wraps/references your Access Connector, so other Unity Catalog objects can use it.
- **Q: What is an External Location?** → A Storage Credential + a specific storage path, packaged together as one reusable "connect here" object.
- **Q: Which do you create first — Credential or External Location?** → Credential first, since the External Location needs to reference it.
- **Q: Why did creating an external location for the metastore container fail?** → It already existed — auto-created when the Metastore was first set up with a root storage path.
- **Q: What's the difference between Account Admin and Metastore Admin?** → Account Admin manages the whole Databricks account (workspaces, users, billing); Metastore Admin manages permissions/objects specifically within one Metastore (catalogs, external locations, credentials).
- **Q: Why should Metastore Admin be assigned to a Group instead of an individual?** → So multiple people can reliably share admin rights, and access can be added/removed just by managing group membership, rather than repeatedly reassigning a single admin setting.
- **Q: What does `abfss://` stand for?** → Azure Blob File System Secure — the URI protocol for referencing ADLS Gen2 paths.
- **Q: Do you need one External Location per container?** → Yes — each container needs its own registered External Location if Unity Catalog is going to govern access to it.

### One-line mental model
```
Access Connector  = the actual Azure permission (keys)
Storage Credential = Unity Catalog's reference to those keys
External Location   = Credential + specific path = ready-to-use governed connection
Account Admin ≠ Metastore Admin — you need the latter specifically, ideally via a GROUP
```

---

## Step-by-Step Checklist

- [ ] 1. Go to Catalog → Connect → External Data → Credentials tab.
- [ ] 2. Create a new Storage Credential: type = Azure Managed Identity, provide your Access Connector's Resource ID.
- [ ] 3. Go to External Location tab → attempt to create one for your `metastore` container → observe the "overlap" error, confirming it already exists automatically.
- [ ] 4. Create a new container (e.g., `raw`) in your Storage Account for your own project data.
- [ ] 5. Create a new External Location pointing to that container, using your new credential.
- [ ] 6. If you hit "User does not have CREATE EXTERNAL LOCATION on Metastore": check who the current Metastore Admin is (Account Console → Catalog → your Metastore).
- [ ] 7. Go to User Management → Groups → find/create an `admins` group → add all relevant user accounts as members.
- [ ] 8. Go back to Catalog → your Metastore → Edit Metastore Admin → assign the GROUP (not an individual) as admin.
- [ ] 9. Retry creating the External Location — it should now succeed.
- [ ] 10. Confirm both External Locations (metastore's auto-created one + your new one) appear in the list.

---
