# Azure Databricks Architecture (Study Notes)

> Topic: The two core "planes" of Databricks architecture (Control Plane vs. Compute Plane), and the newer addition — Serverless Compute — which recently changed how this architecture works.
> Includes: Interview Questions & DP-750 style exam questions at the end.

---

## Why This Topic Matters

Databricks' architecture recently changed with the addition of **serverless compute**, so this is a genuinely important, exam-relevant, and interview-relevant topic — not just old, static theory. Understanding **where things physically live and run** (and who manages what) is the foundation for everything else you'll do in Databricks.

```
DATABRICKS ARCHITECTURE = CONTROL PLANE + COMPUTE PLANE
                                              │
                                    (recently gained a NEW option:
                                     Serverless Compute Plane)
```

---

## Part 1 — The Two Core Planes

Databricks architecture is built around **two separate layers** (called "planes"):

| Plane | Simple English Meaning |
|---|---|
| **Control Plane** | The place from which you *control* almost everything in Databricks — think of it as the "dashboard" / interface layer |
| **Compute Plane** | The place where your data actually gets *processed* — think of it as the "engine room" |

🌟 **Everyday example**: Think of a large factory. The **control plane** is like the manager's office with the control panel, screens, and buttons — where you decide what should happen. The **compute plane** is like the actual factory floor with the heavy machinery — where the real work (processing raw materials into finished products) physically takes place.

```
   ┌─────────────────┐              ┌─────────────────┐
   │   CONTROL PLANE   │             │   COMPUTE PLANE   │
   │  "the dashboard"   │             │  "the engine room" │
   │  (where you        │◄──sends───►│  (where your data   │
   │   control things)  │  commands   │   is processed)     │
   └─────────────────┘              └─────────────────┘
```
*Caption: Two separate layers — one for controlling/interacting, one for the actual heavy-lifting of data processing.*

---

## Part 2 — Control Plane Explained

### Simple English: What is the Control Plane?
The Control Plane is basically **your Databricks web application** — the nice user interface (UI) you log into and click around in. This includes:
- The web UI / dashboard itself.
- Notebooks (where you write code).
- Code files — SQL files, Python files, and so on.

### Key fact: Who manages the Control Plane?
⚠️ **The Control Plane does NOT live inside your own cloud account.** It's directly **managed by Databricks itself** (not by Azure, and not by you). This is exactly why you get a smooth, ready-to-use portal experience — Databricks takes care of hosting and maintaining that interface for you, so you can simply log in and start navigating.

🌟 **Everyday example**: It's like using a banking app — the app's interface (buttons, screens, login system) is built and hosted by the bank itself, not something you personally installed and manage on your own private server. You just interact with it.

### What is the Control Plane actually good for?
It's purely the **interface** — a place to write code, click buttons, and interact with Databricks. It is **NOT** where your actual data gets crunched/processed. That job belongs to the Compute Plane.

---

## Part 3 — Compute Plane Explained

### Simple English: What is the Compute Plane?
This is where the real data processing work happens. When you write, say, an Apache Spark code snippet and hit "run," the actual number-crunching happens here — not in the Control Plane.

### Key fact: Where does the Compute Plane physically live?
The Compute Plane consists of a **cluster** — a group of machines (VMs, or Virtual Machines) — and these machines physically reside **in your own cloud account** (in this course's case, **Azure**).

⚠️ **Simple English callout — Cluster**: A "cluster" is just a technical term for a **group of machines working together**. Think of it as a small team of computers, all cooperating to process your data faster than a single computer could alone (this connects back to the "Apache Spark = distributed processing" idea from the previous lecture).

### Where does your data live?
Your actual data also resides in the **same cloud account** (Azure) — typically in your **Data Lake**. So both your compute (the cluster of VMs) and your storage (the data lake) sit together, inside your own Azure account.

```
                     ┌──────────────────────────────┐
                     │        AZURE (your cloud)       │
                     │                                  │
                     │   ┌───────────────┐              │
                     │   │  COMPUTE PLANE   │              │
                     │   │  (cluster of VMs) │              │
                     │   └───────────────┘              │
                     │                                  │
                     │   ┌───────────────┐              │
                     │   │  DATA LAKE       │              │
                     │   │  (your data)      │              │
                     │   └───────────────┘              │
                     └──────────────────────────────┘
```
*Caption: In your cloud account (Azure), both the compute cluster (VMs that process data) and the data lake (where data lives) reside together.*

---

## Part 4 — Putting It Together: The Classic ("Without Serverless") Architecture

This is the **original / standard** Databricks architecture — before serverless compute was introduced.

```
┌────────────────────┐              ┌─────────────────────────────────┐
│    CONTROL PLANE     │             │              AZURE (your cloud)     │
│  (managed by          │             │                                       │
│   Databricks, NOT      │◄───talks───►│  ┌───────────────┐                    │
│   in your cloud)        │   to each   │  │  COMPUTE PLANE   │                    │
│                        │    other    │  │  (all-purpose     │◄──talks──►  ┌──────────┐│
│  - Web UI               │             │  │   compute cluster) │            │ DATA LAKE ││
│  - Notebooks             │             │  └───────────────┘            └──────────┘│
│  - Code (SQL/Python)      │             │                                       │
└────────────────────┘              └─────────────────────────────────┘
```
*Caption: The classic architecture — the Control Plane (Databricks-managed interface) sits outside your cloud account, and it communicates with the Compute Plane (your cluster of VMs), which sits inside your Azure account alongside your data.*

⚠️ **Simple English callout — "All-purpose compute"**: This classic type of compute (the cluster living inside your Azure account) is also called **"all-purpose compute."** This is simply the *name* given to this original/standard way of running compute, to distinguish it from the newer serverless option (explained next).

**Key summary of this classic architecture:**
- Web UI interactions happen on the **Control Plane** side (outside your cloud account).
- Data processing AND data storage both happen on **your cloud (Azure)** side.
- The Control Plane and Compute Plane **communicate with each other** (send commands back and forth) to make everything work together.

---

## Part 5 — The New Addition: Serverless Compute

⚠️ This is the important recent change mentioned at the very start of this lecture — Databricks has added a brand-new option called **Serverless Compute**, and it comes with its **own dedicated plane**: the **Serverless Compute Plane**.

### Simple English: What is Serverless Compute?
Serverless Compute is a type of compute that is **managed directly by Databricks itself — NOT by Azure.**

This is the single biggest difference to understand:
| Classic (All-Purpose) Compute | Serverless Compute |
|---|---|
| Cluster of VMs lives **inside your Azure account** | Compute resources are **managed by Databricks**, not sitting inside your Azure account |
| Managed by you/Azure | Managed by Databricks |
| Needs to talk to Azure's cluster resources | Does **not** need to talk to an Azure-hosted cluster at all |

⚠️ **Important — both architectures are still in use today.** Serverless compute is **not a replacement** that made the classic (all-purpose) architecture obsolete — both continue to run and be used. You need to understand both.

### How does the architecture change with Serverless Compute?

```
┌────────────────────┐         ┌─────────────────────┐         ┌──────────────┐
│    CONTROL PLANE     │◄──────►│  SERVERLESS COMPUTE    │◄──────►│  AZURE (cloud) │
│  (managed by           │ talks  │  PLANE                  │ talks  │                │
│   Databricks)           │        │  (managed by Databricks, │  directly│  ┌──────────┐  │
│                        │        │   NOT inside your Azure  │  to    │  │ DATA LAKE  │  │
│  - Web UI               │        │   account — has its own   │  data  │  │ (your data) │  │
│  - Notebooks             │        │   VM resources)            │        │  └──────────┘  │
│  - Code                  │        │                          │        │                │
└────────────────────┘         └─────────────────────┘         └──────────────┘
```
*Caption: With serverless compute, the compute layer is no longer sitting inside your Azure account — it's a separate plane managed entirely by Databricks, and it talks DIRECTLY to your data (which still lives in Azure) and DIRECTLY back to the Control Plane.*

### What exactly changed, step by step:
1. There is now a **dedicated Serverless Compute Plane** — separate from the classic Compute Plane.
2. This serverless compute **does not need to talk to** the all-purpose (classic) compute cluster at all — it's an entirely independent path.
3. The serverless compute plane **still has VMs** (machines that actually do the processing) — but critically, these VMs are **not sitting inside your Azure account.**
4. This serverless compute **can talk directly to your data** (which is still sitting in Azure — that part is non-negotiable, your data storage stays in Azure).
5. This serverless compute **also talks directly back to the Control Plane**, to send results back to you.

🌟 **Everyday example**: Imagine ordering food delivery. In the "classic" model, you'd have to personally manage a kitchen (your own Azure-hosted cluster) to cook your food. In the "serverless" model, a delivery/catering company (Databricks) manages their own kitchen entirely, and they just bring the finished food (results) straight to you and pick up ingredients (your data) directly — you never had to set up or manage that kitchen infrastructure yourself at all.

### One More Detail: Default Location / Default Storage
⚠️ **Simple English callout**: When using serverless compute, there is also something called a **default location** (or **default storage**). This is a fallback storage location that Serverless Compute uses automatically.
- In real production environments, this is **hardly used** — most serious production setups still point to their own proper data lake.
- However, it's becoming increasingly popular for lighter/simpler use cases, so it's worth knowing it exists, even if you won't rely on it heavily in production scenarios.

---

## Part 6 — Side-by-Side Comparison: Without Serverless vs. With Serverless

| Aspect | Without Serverless (Classic) | With Serverless |
|---|---|---|
| **Compute cluster location** | Inside your Azure account | Managed by Databricks, NOT inside your Azure account |
| **Who manages compute** | You/Azure (all-purpose compute) | Databricks directly |
| **Talks to Azure-hosted cluster?** | N/A — it IS the Azure-hosted cluster | No — bypasses that entirely |
| **Talks to your data lake** | Yes, directly (compute + data both in Azure) | Yes, directly (serverless compute talks straight to Azure-hosted data) |
| **Talks to Control Plane** | Yes | Yes |
| **Has a "default storage" option** | Not a defining feature | Yes — a default location/storage, used more for lighter/simple use cases (rarely for serious production) |
| **Still actively used today?** | ✅ Yes | ✅ Yes — both coexist |

```
WITHOUT SERVERLESS:                       WITH SERVERLESS:
Control Plane ◄──► Compute Plane          Control Plane ◄──► Serverless Compute Plane
                    (inside Azure,                            (managed by Databricks,
                     talks to Data Lake                        NOT inside Azure,
                     in same Azure account)                    talks directly to
                                                                 Data Lake in Azure)
```
*Caption: The key shift — compute moves OUT of your Azure account and becomes a Databricks-managed plane of its own, while your data STAYS in Azure either way.*

---

## Final Revision Cheat Sheet

### Rapid-fire Q&A
- **Q: What are the two core planes in Databricks architecture?** → Control Plane (the interface/dashboard, managed by Databricks) and Compute Plane (where data is actually processed).
- **Q: Where does the Control Plane physically live?** → It's managed directly by Databricks — it does NOT live inside your own cloud (Azure) account.
- **Q: What does the Control Plane contain?** → The web UI/application, notebooks, and code files (SQL, Python, etc.).
- **Q: Where does the classic (all-purpose) Compute Plane physically live?** → Inside your own Azure account, as a cluster of VMs.
- **Q: What is a "cluster"?** → A group of machines (VMs) working together to process data.
- **Q: Where does your data live?** → In your Azure account (typically in a Data Lake) — this stays true whether you use classic or serverless compute.
- **Q: What is "all-purpose compute"?** → The name for the classic/original compute type, where the cluster of VMs lives inside your Azure account.
- **Q: What is the key difference with Serverless Compute?** → It's managed directly by Databricks (not sitting inside your Azure account), has its own dedicated plane, doesn't need to talk to an Azure-hosted all-purpose cluster, and talks directly to both your data (in Azure) and back to the Control Plane.
- **Q: Did serverless compute replace the classic architecture?** → No — both architectures are still actively used today; you need to understand both.
- **Q: What is "default location" / "default storage" in the context of serverless compute?** → A fallback storage location automatically used by serverless compute; rarely used in serious production scenarios, but increasingly popular for lighter/simpler use cases.

### One-line mental model
```
Control Plane   = the interface (Databricks-managed, outside your cloud)
Compute Plane   = where data processing happens
   - Classic (all-purpose): cluster of VMs INSIDE your Azure account
   - Serverless: compute managed by Databricks, OUTSIDE your Azure account,
                 but still talks directly to your data (in Azure) and to the Control Plane
Data            = always lives in your Azure account (e.g., Data Lake), regardless of compute type
```

---

## Interview Questions & Answers

### 1. "Explain the difference between the Control Plane and the Compute Plane in Databricks."

**Answer:** The Control Plane is the interface layer — it's the Databricks web application, including the UI, notebooks, and code files. It's managed directly by Databricks and does not reside inside the customer's own cloud account. The Compute Plane, on the other hand, is where the actual data processing happens — it consists of a cluster of virtual machines that execute the code (e.g., Apache Spark jobs) written in the Control Plane. In the classic architecture, the Compute Plane's cluster resides inside the customer's own cloud account (e.g., Azure), alongside the data itself.

**Example**: When you write and run a PySpark notebook cell in Databricks, you're interacting with the Control Plane (the notebook UI), but the actual computation of that code happens on the Compute Plane's cluster of VMs.

### 2. "What changed with the introduction of Serverless Compute in Databricks' architecture?"

**Answer:** Before serverless compute, the only compute option (now referred to as "all-purpose compute") required a cluster of VMs to be provisioned inside the customer's own cloud account, and the Control Plane would communicate with that Azure-hosted cluster. With serverless compute, Databricks introduced a new, dedicated Serverless Compute Plane that is managed entirely by Databricks itself — not sitting inside the customer's Azure account at all. This serverless compute plane talks directly to the customer's data (still stored in their Azure data lake) and directly back to the Control Plane, without needing to interact with an Azure-hosted all-purpose cluster.

**Example**: A team wanting quick, ad-hoc SQL query results without provisioning and managing their own cluster infrastructure could use serverless compute, letting Databricks handle the underlying compute resources entirely.

### 3. "Is serverless compute a replacement for all-purpose (classic) compute? Why or why not?"

**Answer:** No, it's not a replacement — both architectures continue to run and be actively used today. All-purpose compute (cluster inside the customer's own Azure account) and serverless compute (managed entirely by Databricks) coexist as two valid compute options, and the right choice depends on the specific use case, cost considerations, and operational preferences of the team or organization.

### 4. "Where does customer data live, regardless of whether all-purpose or serverless compute is used?"

**Answer:** In both cases, the customer's actual data continues to reside in their own cloud account — for example, in Azure Data Lake Storage. What differs between the two compute options is only where the *processing* happens (inside the customer's Azure account for all-purpose compute, versus managed by Databricks outside the customer's Azure account for serverless compute) — not where the data is stored.

### 5. "Scenario: A security-conscious client is concerned about serverless compute because 'it's not inside our Azure account.' How would you address this concern?"

**Answer:** I'd clarify that while serverless compute's processing resources are indeed managed by Databricks rather than sitting inside the customer's Azure tenant, the customer's actual data still remains stored in their own Azure account (e.g., their data lake) at all times — serverless compute simply connects to that data directly to process it, rather than hosting a persistent cluster inside the customer's cloud environment. I'd also mention the existence of a "default location/storage" option that serverless compute can use, noting that in production, most organizations still point serverless compute at their own governed data lake rather than relying on this default storage, keeping data governance and location under the customer's control.

---
