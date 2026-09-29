# Databricks Unity Catalog UDFs

## 1. What is a Unity Catalog Function? ⭐⭐⭐

**UDF = User Defined Function**

A **Unity Catalog Function** is a user-created function stored and managed inside Unity Catalog.

Think of it like:

```text
Unity Catalog
│
├── Catalog
│    └── Schema
│         ├── Tables
│         ├── Views
│         └── Functions
```

So a function can be stored under:

```text
catalog.schema.function
```

Example:

```text
azure_databricks.silver.scalar_function
```

### Main benefit

Instead of creating a function only for one Spark/Python session, you can create a **catalog-level function** and reuse it.

The lecture highlights:

* **Reusability**
* **Governance**
* Stored in Unity Catalog
* Can be referenced by catalog/schema/name
* Useful for things such as data masking and row-level security

---

# 2. Unity Catalog UDF vs traditional PySpark UDF

The lecture's main distinction is:

```text
Traditional/session UDF
        ↓
Usually tied to the current session/application

Unity Catalog Function
        ↓
Stored in Unity Catalog
        ↓
Reusable + governable
```

### Easy way to remember

> **PySpark UDF → function created for processing**

> **Unity Catalog Function → function registered as a governed/reusable object**

---

# 3. What is a Scalar Function? ⭐⭐⭐

A **scalar function** takes a single value as input and returns a single value as output.

```text
Scalar Input
     ↓
  Function
     ↓
Scalar Output
```

Example:

```text
10
 ↓
× 100
 ↓
1000
```

Another example:

```text
"alice@gmail.com"
        ↓
function
        ↓
"gmail.com"
```

The input/output can be of the required scalar data type.

---

# 4. Creating a SQL Scalar Function

General syntax shown in the lecture:

```sql
CREATE OR REPLACE FUNCTION
catalog.schema.function_name(
    parameter_name INT
)
RETURNS INT
LANGUAGE SQL
RETURN parameter_name * 100;
```

Example:

```sql
CREATE OR REPLACE FUNCTION
azure_databricks.silver.scalar_function(
    p_num INT
)
RETURNS INT
LANGUAGE SQL
RETURN p_num * 100;
```

### Understand the parts

```text
CREATE OR REPLACE FUNCTION
```

→ Create the function, or replace it if it already exists.

```text
azure_databricks.silver.scalar_function
```

→ `catalog.schema.function`

```text
p_num INT
```

→ Input parameter and its data type.

```text
RETURNS INT
```

→ Output data type.

```text
LANGUAGE SQL
```

→ Function is written using SQL.

```text
RETURN p_num * 100
```

→ Actual function logic.

---

# 5. Why `CREATE OR REPLACE`?

It is useful during development.

If the function already exists:

```sql
CREATE FUNCTION ...
```

may fail because the object already exists.

With:

```sql
CREATE OR REPLACE FUNCTION ...
```

you can update the function definition.

---

# 6. Using the Function

Once the function is registered in Unity Catalog, you can call it using its full name:

```sql
SELECT
    azure_databricks.silver.scalar_function(age)
FROM azure_databricks.silver.OBD;
```

For example:

```text
age = 25

function:
25 × 100

result:
2500
```

The important pattern is:

```text
catalog.schema.function(column)
```

---

# 7. Why is this useful?

Suppose you have a function that performs a standard transformation:

```text
Customer age
    ↓
classification function
    ↓
Age category
```

Instead of rewriting the logic everywhere:

```text
Notebook 1 → same logic
Notebook 2 → same logic
Notebook 3 → same logic
```

you can create one reusable function:

```text
Unity Catalog Function
        ↓
Notebook 1
Notebook 2
Notebook 3
SQL query
```

That is the **reusability** benefit discussed in the lecture.

---

# 8. Python-based Unity Catalog Function ⭐⭐⭐

The same concept can be implemented using Python.

Example structure from the lecture:

```sql
CREATE OR REPLACE FUNCTION
azure_databricks.silver.scalar_function_python(
    p_num INT
)
RETURNS INT
LANGUAGE PYTHON
RETURN p_num * 100;
```

The important change is:

```text
LANGUAGE SQL
```

vs

```text
LANGUAGE PYTHON
```

---

# 9. SQL vs Python Unity Catalog Functions

```text
Unity Catalog Function
       │
       ├── SQL
       │
       └── Python
```

### SQL function

Use SQL logic:

```sql
RETURN p_num * 100
```

### Python function

Use Python logic:

```python
return p_num * 100
```

The lecture uses the Python version when more customized logic is needed.

---

# 10. Python gives more flexibility ⭐⭐

The lecture demonstrates an issue with NULL values.

Suppose:

```text
p_num = NULL
```

and you do:

```python
p_num * 100
```

Python cannot multiply `None` by an integer.

So you can explicitly handle it:

```python
if p_num is not None:
    return p_num * 100
else:
    return p_num
```

Meaning:

```text
Input
 │
 ├── value exists → multiply by 100
 │
 └── NULL         → keep NULL
```

### Important lesson

> **When writing Python UDF logic, explicitly think about NULL handling.**

---

# 11. Why the NULL issue happened

Example:

```text
p_num = 20
```

works:

```text
20 × 100 = 2000
```

But:

```text
p_num = NULL
```

becomes Python:

```python
None
```

and:

```python
None * 100
```

causes an error.

So robust UDFs should consider edge cases such as NULL inputs.

---

# 12. SQL Function vs Python Function

| SQL Function                       | Python Function                         |
| ---------------------------------- | --------------------------------------- |
| `LANGUAGE SQL`                     | `LANGUAGE PYTHON`                       |
| SQL expressions                    | Python logic                            |
| Good for SQL-based transformations | More customizable logic                 |
| Simple calculations are easy       | Can implement more complex Python logic |

For this lecture, the important point is **flexibility**, not memorizing complicated Python syntax.

---

# 13. Unity Catalog Governance ⭐⭐⭐

Because the function is stored in Unity Catalog:

```text
catalog
   ↓
schema
   ↓
function
```

it becomes a managed catalog object.

The lecture connects this with:

```text
Data governance
Reusability
Data masking
Row-level security
```

So Unity Catalog is not just storing tables.

It can also manage functions.

---

# 14. Important mental model

Think of a Unity Catalog function like a **company-approved reusable tool**.

Instead of every developer creating:

```text
their own masking logic
their own transformation logic
their own function
```

you can have:

```text
Catalog
   ↓
Approved Function
   ↓
Multiple users / queries / workloads
```

That makes reuse and centralized management easier.

---

# 15. Scalar Function vs Table Function

The lecture ends by introducing the next topic: **UDTF / table functions**.

You only need this distinction for now:

### Scalar Function

```text
1 input
 ↓
1 output
```

Example:

```text
25 → 2500
```

### Table Function

Conceptually:

```text
Input
 ↓
Function
 ↓
Multiple rows / table
```

So:

```text
Scalar UDF → returns a value
UDTF       → returns a table/result set
```

The actual table-function implementation is **not covered in this lecture**.

---

# ⭐ Notes-ready cheat sheet

```text
DATABRICKS UNITY CATALOG UDFs

UDF = User Defined Function

Unity Catalog Function:
→ Function stored inside Unity Catalog
→ Reusable
→ Governable
→ Referenced as catalog.schema.function

Hierarchy:
Catalog
  ↓
Schema
  ↓
Function

Scalar Function:
→ Scalar input
→ Scalar output

Example:
25 → function → 2500

SQL function:

CREATE OR REPLACE FUNCTION
catalog.schema.function_name(
    p_num INT
)
RETURNS INT
LANGUAGE SQL
RETURN p_num * 100;


Python function:

CREATE OR REPLACE FUNCTION
catalog.schema.function_name(
    p_num INT
)
RETURNS INT
LANGUAGE PYTHON
RETURN p_num * 100;


Calling function:

SELECT
    catalog.schema.function_name(age)
FROM catalog.schema.table;


Important:
→ SQL UDF → SQL logic
→ Python UDF → Python logic
→ Python logic needs explicit NULL handling

Scalar UDF:
→ returns ONE value

UDTF:
→ returns TABLE/multiple rows
→ covered in next lecture
```

### ⭐ Most important things to remember

```text
Unity Catalog Function
        ↓
Stored centrally
        ↓
Reusable
        ↓
Governable

Scalar function
        ↓
1 value in
        ↓
1 value out

SQL → simple SQL logic
Python → more customizable logic
```

### Interview-style definition

> **A Unity Catalog function is a reusable, governed user-defined function registered in Unity Catalog, addressable by catalog, schema, and function name. A scalar function accepts scalar input and returns a scalar value; it can be implemented using SQL or Python.**
