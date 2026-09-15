# Compute Permissions & Groups (Follow-Along Guide)

> Topic: The three permission levels for controlling who can do what with a specific compute resource (Can Manage / Can Restart / Can Attach To), and how to create a Group and assign compute-related permissions to it — completing the "who can create compute" story from earlier in this course.
> This is a **hands-on lecture** — numbered follow-along guide with a **Common Doubts** section.

💰 **Cost note**: Nothing billable happens here — this is pure permissions/access configuration. **No cost impact.**

🌟 **Direct connection to earlier notes**: Remember way back when you learned *"who can create compute"* (Admins, or non-admins with the "Unrestricted cluster creation" permission)? This lecture shows you **exactly how that permission actually gets granted** in practice — via Groups. This is the missing piece that completes that earlier concept.

---

## Why This Topic Matters

Once a compute resource exists, a new question arises: **who should be allowed to touch it, and how much?** Not everyone needs — or should have — full control over every cluster. This lecture gives you the exact three-tier permission model Databricks uses to answer that.

---

## Part 1 — The Three Compute Permission Levels

**Step 1** — On any compute resource, click the **three-dot menu (⋮) → Edit permissions**.

```
        CAN MANAGE                  CAN RESTART                CAN ATTACH TO
     (most privileged)            (middle privilege)          (least privileged)
           │                             │                            │
           ▼                             ▼                            ▼
   Can change ANY setting        Can turn the compute        Can ONLY attach a
   (worker type, runtime,        back ON if it's              notebook/cluster to
   auto-termination,             currently stopped —           already-running compute
   permissions, delete it,       but CANNOT change             — cannot even START it
   everything)                   any of its settings           if it's off
```
*Caption: Three clear tiers of privilege — from full control, down to "can only use it while it's already running."*

### Definitions, Simple English

| Permission | What you CAN do | What you CANNOT do |
|---|---|---|
| **Can Manage** | Literally everything — change any configuration, restart it, delete it, manage its permissions | Nothing is off-limits |
| **Can Restart** | Turn the compute back on if it's currently stopped | Cannot change any settings/configuration |
| **Can Attach To** | Attach a notebook to the compute and run work on it (only while it's already running) | Cannot start the compute if it's off, and cannot change any settings |

### Doubt: "What happens if I only have 'Can Attach To' permission, and the compute I need is turned off?"
**Answer**: You genuinely **cannot start it yourself.** As the lecture puts it: *"person will call you or anyone else that please bro, turn on the compute... can you please do that?"* You'd need to ask someone with **Can Restart** (or higher) permission to turn it on for you before you can attach your notebook and start working.

🌟 **Everyday example**: Think of a shared company car.
- **Can Manage** = the fleet manager — can change the car's insurance, sell it, hand out keys to whoever they want.
- **Can Restart** = someone with a spare key — can start the engine if it's parked and off, but can't repaint it or change its settings.
- **Can Attach To** = a passenger — can ride in the car once it's already running, but has no key at all.

---

## Part 2 — Who Gets Permissions Automatically?

- **Admins** automatically inherit **Can Manage** on every compute resource, without needing to be explicitly assigned it.
- **Whoever CREATES a compute resource** also automatically gets **Can Manage** on it (you're the "owner" by default).

**Step 2** — To assign permission to someone new: in the Edit Permissions screen, search for the specific user (or, better, a **Group** — covered next) → assign them one of the three permission levels (e.g., `Can Attach To`).

⚠️ **Why data analysts, ML teams, and junior data engineers matter here**: The lecture's real-world example — a shared compute resource might be used by multiple different teams (Data Analysts, ML Engineers, Data Engineers, Junior Engineers). You almost certainly **don't** want all of them to have full `Can Manage` rights — that risks someone accidentally reconfiguring or breaking a shared resource everyone depends on. Assigning the right, minimal permission level per group protects against this.

---

## Part 3 — Follow-Along: Creating a Group

Instead of assigning permissions one individual user at a time (tedious and hard to maintain), the recommended approach is to **create a Group**, and assign permissions to the whole group at once — exactly the same pattern you already used for fixing the "Metastore Admin" issue several lectures ago!

**Step 3** — Go to your **profile icon → Settings → Identity and Access → Groups**.

✅ **Checkpoint**: You'll see two **default groups** that exist automatically: **`admins`** and **`users`**.

**Step 4** — Click **Add group** (or **Create group**).

**Step 5** — Name it, e.g., `data engineers`.

✅ **Checkpoint**: This new group starts completely empty — no members yet.

### Configuring the Group's Default Access
When creating the group, you'll be asked about several account-level access toggles:

| Access Toggle | What it controls | Example setting used in this lecture |
|---|---|---|
| **Workspace access** | Whether this group can access the Databricks workspace at all | ✅ Enabled |
| **Databricks SQL access** | Whether this group can use SQL-related features (SQL Editor, Warehouses) | ✅ Enabled |
| **Unrestricted cluster creation** | ⚠️ **This is the exact permission from the earlier "who can create compute" lecture!** | ✅ Enabled — this group CAN create compute |
| **Can create Pools?** | Whether this group can create Pools | ❌ Disabled — this group cannot create Pools |
| **Admin access** | Full account-wide admin rights | ❌ Disabled — this is not an admin group |

**Step 6** — Click **Add group** (or **Save/Create**) to finalize.

✅ **Checkpoint**: Your `data engineers` group now exists, with exactly the access profile you configured — it can log in, use SQL features, and create compute, but cannot create Pools or perform admin actions.

---

## Part 4 — Connecting the Dots: Groups + Compute Permissions Together

Now that you have a Group, you can go back to any specific compute resource's **Edit Permissions** screen and assign a permission level (Can Manage / Can Restart / Can Attach To) to the **entire group at once**, instead of individually managing each person.

```
   GROUP: "data engineers"
        │
        │  (account-level toggle: Unrestricted cluster creation = ON)
        ▼
   Members of this group CAN create their own NEW compute resources
        │
        │  (separately, on a SPECIFIC EXISTING compute resource's
        │   Edit Permissions screen)
        ▼
   Members of this group are ALSO granted, e.g., "Can Attach To"
   on a specific shared compute resource someone else created
```
*Caption: Two SEPARATE permission layers work together — "Unrestricted cluster creation" (account-level: can this group make NEW compute?) and per-resource permissions like "Can Attach To" (can this group use THIS SPECIFIC existing compute?).*

### Doubt: "Isn't 'Unrestricted cluster creation' the same thing as 'Can Manage' on a specific compute?"
**Answer**: No — these operate at **two different scopes**:
- **"Unrestricted cluster creation"** (an account/group-level toggle) = *"Can this group create BRAND-NEW compute resources at all?"*
- **"Can Manage" / "Can Restart" / "Can Attach To"** (assigned per specific compute resource) = *"What can this group DO with THIS ALREADY-EXISTING, SPECIFIC compute resource?"*

A user could have "Unrestricted cluster creation" (so they can make their OWN new clusters) while simultaneously only having "Can Attach To" permission on a DIFFERENT, shared compute resource someone else built — these are independent, layered controls.

---

## 🤔 Common Doubts — Quick Recap

### Doubt: "Why not just give everyone Can Manage — isn't that simpler?"
**Answer**: Simpler, but risky. Anyone with Can Manage could accidentally (or deliberately) change critical settings, delete the compute, or misconfigure something that breaks other teams' work relying on that same shared resource. Restricting most users to Can Restart or Can Attach To protects the resource's stability while still letting people actually use it.

### Doubt: "Do I really need to create Groups, or can I just assign permissions to individuals?"
**Answer**: You technically can assign to individuals directly — but Groups are the far more maintainable, scalable approach, especially as your team grows. Add/remove a person from the group, and their access updates everywhere that group has been granted permissions — much easier than hunting down every individual resource to update one person's access manually.

### Doubt: "Is this the same 'admins' group I used earlier to fix the Metastore Admin issue?"
**Answer**: Conceptually, yes — same underlying feature (Databricks Groups), same benefit (assign once, manage centrally). That earlier group was specifically about Metastore-level admin rights; this lecture's `data engineers` group is about workspace/compute-level access — different specific purposes, same general mechanism.

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What are the three compute permission levels, from highest to lowest privilege?** → Can Manage → Can Restart → Can Attach To.
- **Q: What can "Can Restart" do that "Can Attach To" cannot?** → Turn the compute back ON if it's currently stopped.
- **Q: What can "Can Manage" do that the other two cannot?** → Change ANY configuration setting on the compute (worker type, runtime, permissions, deletion, etc.).
- **Q: Who automatically gets "Can Manage" on a compute resource?** → Admins (always), and whoever originally created that specific compute resource.
- **Q: What are the two default Groups every Databricks account has?** → `admins` and `users`.
- **Q: What's the difference between "Unrestricted cluster creation" and per-resource compute permissions?** → "Unrestricted cluster creation" is an account/group-level toggle controlling whether a group can create BRAND-NEW compute; per-resource permissions (Can Manage/Restart/Attach To) control what a group can do with a SPECIFIC, ALREADY-EXISTING compute resource.
- **Q: Why use Groups instead of assigning permissions to individuals?** → Easier, centralized management — updating one group's membership automatically updates access everywhere that group has been granted permissions.

### One-line mental model
```
Can Manage    = full control (config + restart + attach)
Can Restart   = can turn it on, cannot reconfigure
Can Attach To = can only use it while already running

GROUPS = assign permissions once, to many people at once, instead of per-individual
"Unrestricted cluster creation" (account-level) ≠ "Can Manage" (per-resource) — two separate layers
```

---

## Full Step-by-Step Recap Checklist

- [ ] 1. On an existing compute → three-dot menu → Edit permissions.
- [ ] 2. Observe that Admins + the compute's creator already have "Can Manage" by default.
- [ ] 3. Go to Settings → Identity and Access → Groups.
- [ ] 4. Note the two default groups: `admins` and `users`.
- [ ] 5. Click Add group → name it (e.g., `data engineers`).
- [ ] 6. Configure its account-level access: Workspace access ✅, Databricks SQL access ✅, Unrestricted cluster creation ✅, Can create Pools ❌, Admin access ❌.
- [ ] 7. Save/Create the group.
- [ ] 8. Go back to a specific compute resource's Edit Permissions screen → assign the new group a permission level (e.g., "Can Attach To").
- [ ] 9. Confirm the group now has exactly the intended layered access: can create their own compute (account-level), plus a specific permission level on this particular shared resource.

---

*End of notes. This closes out the full Classic Compute section of the course — creation, configuration, monitoring, Libraries, Pools, Policies, and now Permissions/Groups. Next: the course moves into new territory beyond compute.*
