# Creating the Unity Metastore via Account Console (Follow-Along Guide)

> Topic: Finding the Account Console (where Metastore management actually lives), understanding the "admin account" concept, deleting the auto-created default Metastore, and creating your own Metastore attached to your Data Lake + Access Connector from the previous lectures.
> This is a **hands-on lecture** — numbered follow-along guide, with a **Common Doubts** section.

💰 **Cost note**: Nothing new and billable is created in this lecture — you're only configuring/attaching resources you already created (Storage Account + Access Connector from the last lecture) to a Metastore object, and managing user roles. **No cost impact.**

---

## Prerequisites
- A deployed Azure Databricks workspace.
- The Storage Account (with a `metastore` container) and Access Connector from the previous lecture, with all 4 IAM roles assigned.

---

## Part 1 — Finding Where Metastore Setup Actually Lives

### Doubt: "I can see 'Catalog' in my Databricks workspace sidebar, but there's no 'Metastore' option anywhere. Where is it?"

**Answer**: Metastore management doesn't live inside your regular Databricks **Workspace** UI at all — it lives in a completely separate portal called the **Account Console**.

⚠️ **Simple English callout — Account Console**: This is a dedicated admin-level portal where **account admins** manage settings that apply across **all** of an organization's Databricks workspaces (not just one) — things like Metastores, account-wide user management, and billing usage. Think of your normal Databricks Workspace as "one office branch," while the Account Console is "corporate headquarters" — it oversees and configures things at a level above any single workspace.

---

## Part 2 — Understanding WHO is Actually the "Admin"

### Doubt: "I created this whole workspace myself — surely I'm the admin?"

**Answer**: Yes, but **not through the account you normally log in with** (e.g., your regular Gmail-linked login). Here's the twist:

- When you log into Databricks day-to-day, you're often using a simple, personal-feeling login (like a Gmail account).
- But the **actual admin identity** recognized by Azure/Databricks is a **different, auto-generated account** — a long email-address-style identity tied to your Microsoft Entra ID (recall: Entra is the hub for all users/identities in Azure).

**Step 1** — To find this real admin identity: go to **Azure Portal → Entra ID → Users**.

**Step 2** — Click on your account — you'll see a long, system-generated email address. **This** is the actual admin of your Databricks account, not your everyday login.

🌟 **Everyday example**: Think of it like a company where you personally set up a new office, but the building's official ownership paperwork is registered under the company's formal legal name — not your personal nickname. You're still "in charge," but the *official* recognized identity for high-level admin actions is that formal registration, not your everyday casual identity.

---

## Part 3 — Follow-Along: Logging Into the Account Console

**Step 3** — Go to your browser and type this URL **directly** (don't rely on clicking through menus — it can sometimes fail to redirect properly):
```
accounts.azuredatabricks.net
```
⚠️ You can optionally add `/login` at the end, but it's not required — typing the base URL alone works fine.

**Step 4** — You'll be asked for an email/account. ⚠️ **Common error**: If you enter your normal, everyday login email here, you may see an error like *"Selected user account does not exist in tenant."* This happens because that everyday account isn't recognized as a valid identity within this specific Entra tenant for this purpose.

**Step 5** — Instead, enter the **long, auto-generated admin email address** you found in Entra ID → Users (from Part 2).

**Step 6** — Complete login — if it's your first time, you may be asked to reset your password and/or complete multi-factor authentication (MFA) verification (e.g., entering a code).

✅ **Checkpoint**: You should now land on the **Account Console** — a different-looking portal from your regular Databricks workspace.

---

## Part 4 — Optional Shortcut: Making Your Everyday Account an Account Admin Too

### Doubt: "Do I have to keep using that long, awkward email every single time just to reach the Account Console?"

**Answer**: No — you can promote your everyday, normal-feeling account to also be an Account Admin, which then makes a **"Manage Account"** option appear directly inside your regular Databricks workspace menu (instead of needing the separate URL).

**Step 7** — While logged into the Account Console (using the long admin account), go to **User Management**.

**Step 8** — Click **Add User** → enter the email/username you'd like to add (e.g., your everyday Gmail-linked account).

**Step 9** — Click on that newly added user → go to **Roles** → set the role to **Account Admin**.

⚠️ **Note**: You may need to refresh your regular Databricks workspace for the "Manage Account" option to visibly appear in the menu afterward. Even if it doesn't show up immediately, you can always fall back to directly visiting `accounts.azuredatabricks.net`.

---

## Part 5 — Follow-Along: Dealing With the Default (Auto-Created) Metastore

**Step 10** — In the Account Console, click **Catalog**. You'll likely see a Metastore already listed here.

### Doubt: "Wait — I didn't create this Metastore. Where did it come from?"

**Answer**: This connects directly back to earlier notes: since 2024, Unity Catalog (including a default Metastore) is **automatically created** by Azure Databricks for new workspaces — you never manually set this up.

### Doubt: "Should I just use this existing default Metastore instead of creating my own?"

**Answer**: **No — the recommended approach is to delete it and create your own from scratch.** Two reasons:
1. **Best practice/control**: Building your own Metastore means you know exactly how it's configured, which storage it's tied to, and how it's set up — rather than inheriting an auto-generated default you didn't design.
2. **A hard technical constraint**: ⚠️ **You can only have ONE Metastore per Azure region.** Since the default one already occupies your region, you must delete it before you can create your own in that same region.

**Step 11** — Click into the default Metastore → **Delete**.

**Step 12** — Confirm the deletion by typing the Metastore's name exactly as prompted.

✅ **Checkpoint**: The default Metastore is now removed, freeing up your region to host your own custom Metastore.

---

## Part 6 — Follow-Along: Creating Your Own Metastore

**Step 13** — In the Account Console, go to **Catalog → Create Metastore**.

**Step 14** — Fill in the form:

| Field | What to enter | Notes |
|---|---|---|
| **Name** | e.g., `azure-databricks-metastore` | Just a label |
| **Region** | Ideally the same region as your Databricks workspace | Best practice, not strictly forced — a single Metastore *can* serve multiple catalogs regardless of workspace region matching, but keeping them aligned avoids unnecessary cross-region complexity |
| **ADLS Gen2 path** | ⚠️ Technically **optional** (as established in earlier notes) — but this course chooses to provide it | Format: `<container-name>@<storage-account-name>.dfs.core.windows.net/` |
| **Access Connector ID** | The full Resource ID of your Access Connector | Needed because the Metastore cannot access the storage account directly — same "secured by default" principle from earlier notes |

**Worked example of the ADLS Gen2 path**, using this course's exact resource names:
```
metastore@azuredatabricksanj.dfs.core.windows.net/
```
- `metastore` = the container name (created in the previous lecture).
- `azuredatabricksanj` = the storage account name.
- `.dfs.core.windows.net` = the standard fixed domain suffix for ADLS Gen2 endpoints.

**Step 15** — For the Access Connector ID: go to your **Access Connector** resource in the Azure Portal → copy its **Resource ID** → paste it into the form.

**Step 16** — Click **Create**.

✅ **Checkpoint**: Your Metastore is now created, with your Data Lake storage attached to it.

---

## Part 7 — Follow-Along: Attaching Your Workspace to the Metastore

**Step 17** — Immediately after creation, you'll be prompted: *"Do you want to attach your existing workspace to this Metastore?"* → **Yes, select your workspace.**

⚠️ **Optional setting you'll also see**: *"Automatically assign new workspaces in [region] to this Metastore."* This is optional — it just means any *future* new workspaces you create in that same region would auto-attach to this Metastore without you needing to do this step manually again. Feel free to ignore it if you don't plan on creating more workspaces right now.

**Step 18** — Click **Assign** (or **Enable**).

✅ **Checkpoint**: Your Databricks Unity Catalog is now successfully attached to your custom Metastore.

### What does this actually unlock now?
From this point forward, whenever you create a **Managed** resource (table, volume, etc.) without specifying its own storage location, it will automatically be saved into your `metastore` container within your Data Lake — exactly matching everything covered in the previous conceptual lecture.

---

## Part 8 — Doubt: "What if I forgot to attach my workspace during setup?"

**Answer**: Not a problem — it's fully recoverable after the fact:

**Step 19 (if needed later)** — In the Account Console, go to **Workspaces** → click your Databricks workspace → check if it's attached to a Metastore.

**Step 20 (if needed later)** — Alternatively, go to **Catalog → [your Metastore] → Workspaces tab** → attach your workspace from there.

---

## Full Recap Diagram

```
NORMAL DATABRICKS WORKSPACE                    ACCOUNT CONSOLE
(accessed via your everyday login)             (accounts.azuredatabricks.net —
 - Catalog (browse/use Unity Catalog)             requires ADMIN identity, e.g. the
 - Compute, Jobs, etc.                             long auto-generated Entra email)
 - NO Metastore creation option here      ◄────  - Catalog → CREATE/DELETE Metastore
                                                   - User Management → assign Account Admin
                                                   - Workspaces → attach/detach Metastore

METASTORE CREATION FORM NEEDS:
  1. Name
  2. Region (match your workspace region — best practice)
  3. ADLS Gen2 path → "metastore@<storage-account>.dfs.core.windows.net/"
  4. Access Connector ID → so the Metastore can actually reach the storage
```

---

## 🤔 Common Doubts — Quick Recap

### Doubt: "Why can't I just create the Metastore from inside my normal Databricks workspace?"
**Answer**: Because a Metastore is an account-wide (not workspace-specific) object — it can be shared across multiple workspaces in the same region. Managing something that spans multiple workspaces has to happen at a level above any single workspace — that's exactly what the Account Console is for.

### Doubt: "Why does Databricks force only ONE Metastore per region?"
**Answer**: This is a deliberate design decision to keep governance simple and centralized — rather than having multiple competing, possibly conflicting Metastores fragmenting your organization's data governance within the same region. All catalogs for that region live under this one shared Metastore.

### Doubt: "Is it a problem that I have to delete the auto-created default Metastore?"
**Answer**: No — since this is a fresh learning workspace, the default Metastore has no important data or configuration in it yet, so deleting it is completely safe. (In a real production environment already actively using that default Metastore, you would obviously need to be far more careful before deleting it.)

### Doubt: "Why did entering my normal email give an error on the Account Console login page?"
**Answer**: Because the Account Console strictly authenticates against actual Entra ID tenant identities, and your everyday/casual login (e.g., a personal Gmail tied loosely to the workspace) isn't necessarily registered as a full identity within that Entra tenant — only the proper, long, system-recognized admin email is.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: Where do you create/manage a Unity Metastore?** → The Account Console (`accounts.azuredatabricks.net`), not the regular Databricks workspace UI.
- **Q: Who is the "real" admin of your Databricks account?** → A long, auto-generated Entra ID identity — not necessarily your everyday login account.
- **Q: How many Metastores can exist per Azure region?** → Exactly one.
- **Q: Why must the default auto-created Metastore be deleted before creating your own?** → Because only one Metastore is allowed per region, and the default one already occupies that slot.
- **Q: What four things does the "Create Metastore" form need?** → Name, Region, ADLS Gen2 path (optional but recommended here), and Access Connector ID.
- **Q: How can you make "Manage Account" appear directly in your normal workspace menu?** → Add your everyday account as a user in User Management (via Account Console), then assign it the "Account Admin" role.
- **Q: What happens if you forget to attach your workspace to the Metastore during creation?** → You can attach it later, either via Account Console → Workspaces, or via Account Console → Catalog → [Metastore] → Workspaces tab.

### One-line mental model
```
Account Console = admin HQ for ALL workspaces (Metastore lives here)
Databricks Workspace = day-to-day work area (Catalog browsing lives here, not Metastore creation)
Real admin identity = long Entra ID email, not your casual login
One Metastore per region — delete the auto-created default before making your own
```

---

## Full Step-by-Step Recap Checklist

- [ ] 1. Find your real admin identity: Azure Portal → Entra ID → Users → note the long email address.
- [ ] 2. Go to `accounts.azuredatabricks.net` and log in using that long admin email (not your everyday login).
- [ ] 3. (Optional) In Account Console → User Management → Add User → assign your everyday account the "Account Admin" role, so "Manage Account" appears in your normal workspace menu going forward.
- [ ] 4. In Account Console → Catalog, locate the auto-created default Metastore.
- [ ] 5. Delete the default Metastore (type its name to confirm).
- [ ] 6. Go to Catalog → Create Metastore.
- [ ] 7. Fill in Name, Region (match workspace region), ADLS Gen2 path (`container@storageaccount.dfs.core.windows.net/`), and Access Connector ID (from your Access Connector resource).
- [ ] 8. Click Create.
- [ ] 9. When prompted, attach your existing workspace to the new Metastore.
- [ ] 10. (Optional) Enable "Automatically assign new workspaces in this region" if you plan to create more workspaces later.
- [ ] 11. Confirm success, then close the dialog.

---
