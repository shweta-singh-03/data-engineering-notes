# Databricks notebook source
# MAGIC %md
# MAGIC # OBT - Gold Table

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS azuredatabricks.gold

# COMMAND ----------

df_orders = spark.read.table("azuredatabricks.silver.orders")
df_products = spark.read.table("azuredatabricks.silver.products")
df_customers = spark.read.table("azuredatabricks.silver.customers")

# COMMAND ----------

orders = df_orders.alias("orders")
customers = df_customers.alias("customers")
products = df_products.alias("products")

# COMMAND ----------

# first join
df_orders_customers = (
    orders
    .join(
        customers,
        col("orders.customer_id") == col("customers.customer_id"),
        "left"
    )
)

# display(df_orders_customers.limit(10))

# COMMAND ----------

# second join
df_join = (
    df_orders_customers
    .join(
        products,
        col("orders.product_id") == col("products.product_id"),
        "left"
    )
)

# display(df_join.limit(10))

# COMMAND ----------

df_join = df_join.select(
    col("orders.customer_id"),
    col("orders.discount"),
    col("orders.order_amount"),
    col("orders.order_date"),
    col("orders.order_id"),
    col("orders.payment_status"),
    col("orders.product_id"),
    col("orders.quantity"),
    col("orders.updated_at").alias("orders_updated_at"),
    col("orders.silver_processed_at").alias("orders_silver_processed_at"),

    col("customers.customer_name"),
    col("customers.email"),
    col("customers.country"),
    col("customers.signup_date"),
    col("customers.customer_type"),
    col("customers.age"),
    col("customers.updated_at").alias("customers_updated_at"),
    col("customers.silver_processed_at").alias("customers_silver_processed_at"),

    col("products.product_name"),
    col("products.category"),
    col("products.price"),
    col("products.supplier"),
    col("products.available"),
    col("products.updated_at").alias("products_updated_at"),
    col("products.silver_processed_at").alias("products_silver_processed_at")
)

display(df_join.limit(10))

# COMMAND ----------

df_join = df_join.withColumn("gold_processed_at", current_timestamp())

# COMMAND ----------

# df_join -> is your complete OBT table (gold table)
# WRITE OBT TABLE AS UNITY CATALOG TABLE

from delta.tables import DeltaTable

# check if table exists
if spark.catalog.tableExists("azuredatabricks.gold.obt"):
    # print("table exists")
    delta_obj = DeltaTable.forName(spark, "azuredatabricks.gold.obt")

    delta_obj.alias("trg").merge(
        df_join.alias("src"), 
        "trg.order_id == src.order_id AND trg.customer_id == src.customer_id AND trg.product_id == src.product_id")\
            .whenMatchedUpdateAll(condition = "src.orders_updated_at > trg.orders_updated_at AND src.customers_updated_at > trg.customers_updated_at AND src.products_updated_at > trg.products_updated_at")\
            .whenNotMatchedInsertAll()\
            .execute()
else:
    # print("table doesn't exist table will be created with initial load")
    df_join.write\
                .format("delta")\
                .mode("overwrite")\
                .saveAsTable("azuredatabricks.gold.obt")

# COMMAND ----------

# MAGIC %md
# MAGIC # Business Views

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from azuredatabricks.gold.obt

# COMMAND ----------

df_agg = spark.read.table("azuredatabricks.gold.obt")

# COMMAND ----------

# MAGIC %md
# MAGIC ### GroupBy aggregation

# COMMAND ----------

df_agg = (
    df_agg.groupBy("country", "customer_type")
    .agg(
        count("order_id").alias("Total_orders"),
        count("customer_id").alias("Total_customers"),
    )
    .sort("country")
)

display(df_agg)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Pivot

# COMMAND ----------

df_pivot = spark.read.table("azuredatabricks.gold.obt")

df_pivot = df_pivot.withColumn("flag", when(col("age")<=15,lit("junior"))\
                                  .when((col("age")>15) & (col("age")<35), lit("middle"))\
                                  .otherwise(lit("senior"))
                              )

display(df_pivot)

# COMMAND ----------

df_pivot = df_pivot.groupBy("country").pivot("flag").agg(count("customer_id").alias("total_customers")).sort("country")
display(df_pivot)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Spark SQL

# COMMAND ----------

# MAGIC %md
# MAGIC ####  1st way - you have a sql query and wnat to create a dataframe using that sql

# COMMAND ----------

df = spark.sql("""
               SELECT * FROM azuredatabricks.gold.obt
               WHERE country = 'Canada' or country = 'USA'
               """
)

# COMMAND ----------

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### 2nd way - you have a dataframe and you wnat to run a sql query over it

# COMMAND ----------

df.createOrReplaceTempView("temp_view")

# COMMAND ----------

display(spark.sql("""
    SELECT * FROM temp_view
"""))

# COMMAND ----------

