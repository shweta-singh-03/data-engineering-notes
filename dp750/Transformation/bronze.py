# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS azuredatabricks

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS azuredatabricks.bronze

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Reading

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC ### Customers data - CSV

# COMMAND ----------

df_customers = spark.read.format("csv")\
                .option("header", "true")\
                .option("inferSchema", "true")\
                .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/staging/customers")
display(df_customers)

# COMMAND ----------

df_customers.printSchema()

# COMMAND ----------

df_customers.schema

# COMMAND ----------

print(df_customers.schema.toDDL())

# COMMAND ----------

# struct schema
my_struct_schema = StructType(
    [
        StructField("customer_id", IntegerType(), True),
        StructField("customer_name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("country", StringType(), True),
        StructField("signup_date", DateType(), True),
        StructField("customer_type", StringType(), True),
        StructField("age", DoubleType(), True),
        StructField("updated_at", TimestampType(), True),
    ]
)

# ddl schema
my_ddl_schema = """ 
customer_id STRING,
customer_name STRING,
email STRING,
country STRING,
signup_date DATE,
customer_type STRING,
age DOUBLE,
updated_at TIMESTAMP
"""

# COMMAND ----------

# Reading the customer data using our own schema defined above - we dont always use inferschema = true, we define our schema ourselves 

# I want to apply "string" datatype to "customer_id" column
df_customers = spark.read.format("csv")\
                .option("header", "true")\
                .schema(my_struct_schema)\
                .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/staging/customers")
display(df_customers)

# COMMAND ----------

df_customers.write.format("delta")\
    .mode("append")\
    .saveAsTable("azuredatabricks.bronze.customers")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Products Data - Parquet

# COMMAND ----------

df_products = spark.read.format("parquet")\
                .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/staging/products")


df_products.write.format("delta")\
    .mode("append")\
    .saveAsTable("azuredatabricks.bronze.products")

# COMMAND ----------

# MAGIC %md
# MAGIC ## other way to read into bronze (incrementally)

# COMMAND ----------

# MAGIC %sql
# MAGIC COPY INTO azuredatabricks.bronze.products
# MAGIC FROM "abfss://raw@databricksdp750storage.dfs.core.windows.net/staging/products"
# MAGIC FILEFORMAT = PARQUET
# MAGIC FORMAT_OPTIONS ('mergeSchema' = 'true')
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Orders data - JSON 

# COMMAND ----------

df_orders = spark.read.format("json")\
                .option("multiline",False)\
                .option("inferSchema",True)\
                .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/staging/orders")

# COMMAND ----------

df_orders.write.format("delta")\
    .mode("append")\
    .saveAsTable("azuredatabricks.bronze.orders")