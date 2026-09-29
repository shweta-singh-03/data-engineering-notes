
# Databricks Unity Catalog — Table Functions / UDTFs

## 1. What is a Table Function?

**UDTF = User-Defined Table Function**

It is a Unity Catalog function that:

> **Takes a parameter and returns a table (multiple rows + columns).**

Think:

```text
Parameter
   ↓
UDTF
   ↓
Rows + Columns
   ↓
Table result
```

This is different from a scalar function.

---

# 2. Scalar Function vs Table Function ⭐⭐⭐

### Scalar Function

```text
Input
 ↓
Function
 ↓
One value
```

Example:

```text
25 → ×100 → 2500
```

### Table Function

```text
Input parameter
      ↓
    Function
      ↓
SELECT query
      ↓
Rows + Columns
```

Example:

```text
30
 ↓
Find people where age > 30
 ↓
Entire matching table
```

### Memory trick

```text
Scalar → value
Table  → table
```

---

# 3. Why does a Table Function return a table?

Because its internal logic is based on a **SELECT statement**.

Conceptually:

```sql
SELECT *
FROM some_table
WHERE age > parameter;
```

The result of that query contains:

```text
multiple rows
+
multiple columns
```

So the function returns a **table result**.

---

# 4. Example from the lecture ⭐⭐⭐

The requirement:

> Create a reusable function that returns records from the OBT where age is greater than a value provided by the user.

For example:

```text
Input parameter = 30

Result:
all OBT records where age > 30
```

---

# 5. Creating the UDTF

The lecture uses the structure:

```sql
CREATE OR REPLACE FUNCTION
catalog.schema.table_function(
    p_age INT
)
RETURNS TABLE
RETURN
SELECT *
FROM catalog.gold.OBT
WHERE age > p_age;
```

### Understand the important parts

```text
CREATE OR REPLACE FUNCTION
```

→ Create the Unity Catalog function or replace its existing definition.

```text
catalog.schema.table_function
```

→ Where the function is stored.

```text
p_age INT
```

→ Input parameter.

```text
RETURNS TABLE
```

→ This function returns rows and columns, not one scalar value.

```text
RETURN SELECT ...
```

→ The result of the SQL query becomes the function's output.

---

# 6. Why use a parameter?

Without a parameter, you might write:

```sql
WHERE age > 30
```

Then the function is fixed to `30`.

With:

```sql
WHERE age > p_age
```

the user can provide different values.

For example:

```text
table_function(30)
→ age > 30

table_function(50)
→ age > 50
```

So:

> **Parameters make the table function reusable and dynamic.**

---

# 7. Calling a Table Function ⭐⭐⭐

A table function is used differently from a scalar function.

Because it returns a table, the lecture calls it through the `FROM` clause:

```sql
SELECT *
FROM catalog.schema.table_function(30);
```

Conceptually:

```text
table_function(30)
      ↓
SELECT *
      ↓
Table result
```

---

# 8. Why isn't it called like a normal scalar function?

Scalar:

```sql
SELECT catalog.schema.scalar_function(age)
FROM ...
```

Because it produces a value for a row.

Table function:

```sql
SELECT *
FROM catalog.schema.table_function(30);
```

Because it produces a **table result**.

So remember:

```text
Scalar Function
→ used like a column/value

Table Function
→ used like a table in FROM
```

---

# 9. Example

Suppose OBT contains:

```text
customer_id | name  | age
------------|-------|----
1           | Alice | 22
2           | Bob   | 35
3           | John  | 42
4           | Sara  | 51
```

Call:

```sql
SELECT *
FROM catalog.silver.table_function(40);
```

Function internally applies:

```sql
WHERE age > 40
```

Result:

```text
customer_id | name | age
------------|------|----
3           | John | 42
4           | Sara | 51
```

---

# 10. Main advantage — Reusability ⭐⭐⭐

Without a table function, you might repeatedly write:

```sql
SELECT *
FROM OBT
WHERE age > 30;
```

Then somewhere else:

```sql
SELECT *
FROM OBT
WHERE age > 50;
```

Instead, create one reusable function:

```text
table_function(age_limit)
```

Then:

```sql
SELECT *
FROM table_function(30);
```

or:

```sql
SELECT *
FROM table_function(50);
```

The same logic is reused.

---

# 11. Unity Catalog advantage

Because this is a **Unity Catalog Function**, the function is stored in the catalog:

```text
Catalog
   ↓
Schema
   ↓
Function
```

So you can:

```text
Create once
   ↓
Reuse many times
```

and update the function definition centrally using:

```sql
CREATE OR REPLACE FUNCTION ...
```

The lecture specifically emphasizes that the function remains stored in the catalog and can be replaced with updated logic.

---

# ⭐ Notes-ready Cheat Sheet

```text
UNITY CATALOG TABLE FUNCTIONS / UDTF

UDTF = User-Defined Table Function

→ Takes parameter(s)
→ Returns a TABLE
→ Table = rows + columns

Scalar Function:
Input → Function → One value

Table Function:
Parameter → Function → Table

Example:

CREATE OR REPLACE FUNCTION
catalog.schema.table_function(
    p_age INT
)
RETURNS TABLE
RETURN
SELECT *
FROM catalog.gold.OBT
WHERE age > p_age;


Call:

SELECT *
FROM catalog.schema.table_function(30);


Important:
RETURNS INT / STRING
→ scalar function

RETURNS TABLE
→ table function

Scalar function
→ generally used as a value/expression

Table function
→ called in FROM because it returns a table

Main benefit:
→ reusable + parameterized + stored in Unity Catalog
```

### ⭐ One-line definition

> **A Unity Catalog UDTF is a reusable, parameterized function that executes query logic and returns a table containing rows and columns.**

### ⭐ Most important difference

```text
Scalar UDF
    ↓
25
    ↓
2500

UDTF
    ↓
30
    ↓
SELECT ... WHERE age > 30
    ↓
Table of matching records
```

So the previous lecture was:

**"Create a reusable function that returns a value."**

This lecture is:

**"Create a reusable function that returns a table."**
