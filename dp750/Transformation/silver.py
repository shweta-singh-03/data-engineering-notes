# Databricks notebook source
from pyspark.sql.types import *
from pyspark.sql.functions import *

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS azuredatabricks.silver

# COMMAND ----------

# MAGIC %md
# MAGIC # Data Reading

# COMMAND ----------

# MAGIC %md
# MAGIC # Bronze Customers table - READ

# COMMAND ----------

df_customers = spark.read.table("azuredatabricks.bronze.customers")
# display(df_customers)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Handling Nulls

# COMMAND ----------

# dropping rows whichever column contains null value
# display(df_customers.dropna())

# dropping rows which contains null value in column 'country'
display(df_customers.dropna(subset=['country']))


# COMMAND ----------

# replacing nulls with value 'unknown' as we cannot always drop the data on null values as there will be data loss
# display(df_customers.fillna("unknown",subset = ["country"]))

df_customers = df_customers.fillna("unknown")
df_customers = df_customers.fillna(0,subset=["age"])
# display(df_customers)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Handling Duplicates

# COMMAND ----------

# drop duplicates based on entirely matching records/rows - which has exactly same values in all the columns for a records only that will get dropped
df_customers = df_customers.dropDuplicates()
# display(df_customers)

# COMMAND ----------

# we can also drop duplicates based on specific columns
# just to show the impact we are dropping dupes based on column country
display(df_customers.dropDuplicates(subset = ["country"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Filtering data

# COMMAND ----------

# here for example we will create df for every country
df_india = df_customers.filter(col("country") == "India")
display(df_india)

# COMMAND ----------

# multiple filters within one condition
df_ind_usa = df_customers.filter((col("country") == "India") | (col("country") == "USA"))
display(df_ind_usa)

# COMMAND ----------

# reverse - filter records where country is not India and USA
df_ind_usa_not = df_customers.filter((col("country") != "India") & (col("country") != "USA"))
display(df_ind_usa_not)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Union

# COMMAND ----------

# stacking one dataframe on top of another dataframe

# union - will stack the dataframe without checking the scheme, just one after another, if teh dataframe is not in the correct column order then it can create a messy combined data - so we use unionByName - when you have misorganized columns then use this!

df_combined = df_ind_usa.union(df_ind_usa_not)
display(df_combined)

# COMMAND ----------


# unionByName - will stack the dataframe by checking the schema, if the column order is not correct then it will throw an error

df_combined = df_ind_usa.unionByName(df_ind_usa_not)
display(df_combined)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Intersect

# COMMAND ----------

df_intersect = df_customers.intersect(df_ind_usa)
display(df_intersect)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Except / Subtract

# COMMAND ----------

# if you want to perform subtraction on dataframes

df_except = df_customers.subtract(df_ind_usa)
display(df_except)

# COMMAND ----------

# if there are nulls in the parent dataframe and you want to keep it, then use exceptAll

# df_except = df_customers.exceptAll(df_ind_usa)
# display(df_except)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Select

# COMMAND ----------

df_customers_selected = df_customers.select(col("customer_id"), col("customer_name"), col("email"), col("country"))
display(df_customers_selected)

# COMMAND ----------

# you can even alias your column names using col("col_name").alias("new_col_name")
df_customers_selected = df_customers.select(col("customer_id").alias("id"), col("customer_name"), col("email"), col("country"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### withColumn() - for creating & updating columns

# COMMAND ----------

df_customers = df_customers.withColumn("silver_processed_at", current_timestamp())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Split function

# COMMAND ----------

df_customers = df_customers.withColumn("domains", split(col("email"),"@")[1])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Date functions 
# MAGIC `col(col_name).cast(TimestampType())`
# MAGIC
# MAGIC `to_date(col(col_name), "MM-dd-yyyy")`

# COMMAND ----------

# df_customers = df_customers.withColumn(col("signup_date"), to_date(col("signup_date"), "MM-dd-yyyy"))

df_customers = df_customers.withColumn("signup_date", col("signup_date").cast(TimestampType()))

# COMMAND ----------

display(df_customers)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Case When Statements

# COMMAND ----------

df_customers = df_customers.withColumn("flag", when(col("age")< 15 , lit("junior"))\
                                              .when((col("age") >=15) & (col("age") <35), lit("middle"))\
                                              .otherwise(lit("senior"))\
                                               )

# COMMAND ----------

# MAGIC %md
# MAGIC # Data Writing [UPSERT]

# COMMAND ----------

# MAGIC %md
# MAGIC # Silver Customers table - Write

# COMMAND ----------

# checking if table exists in catalog or not
# initial load when the data is not there - and how do we know if data is already present or not?
# we check if the table exists in the catalog or not
# if it exists, we do a merge
# if it doesn't exist, we create the table and dump the initial data (first load/overwite after that we only do upsert/merge)

from delta.tables import DeltaTable

# check if table exists
if spark.catalog.tableExists("azuredatabricks.silver.customers"):
    # print("table exists")
    delta_obj = DeltaTable.forName(spark, "azuredatabricks.silver.customers")

    delta_obj.alias("trg").merge(
        df_customers.alias("src"), 
        "trg.customer_id == src.customer_id")\
            .whenMatchedUpdateAll(condition = "src.updated_at > trg.updated_at")\
            .whenNotMatchedInsertAll()\
            .execute()
else:
    print("table doesn't exist table will be created with initial load")
    df_customers.write\
                .format("delta")\
                .mode("overwrite")\
                .saveAsTable("azuredatabricks.silver.customers")

# COMMAND ----------

# MAGIC %md
# MAGIC # Bronze `Products` table - READ

# COMMAND ----------

df_products = spark.read.table("azuredatabricks.bronze.products")
df_products = df_products.fillna("Unknown")
df_products = df_products.fillna(0,subset = ["price"])
df_products = df_products.dropDuplicates()
df_products = df_products.withColumn("silver_processed_at", current_timestamp())


# COMMAND ----------

# MAGIC %md
# MAGIC # Silver Products table - Write

# COMMAND ----------

from delta.tables import DeltaTable

# check if table exists
if spark.catalog.tableExists("azuredatabricks.silver.products"):
    # print("table exists")
    delta_obj = DeltaTable.forName(spark, "azuredatabricks.silver.products")

    delta_obj.alias("trg").merge(
        df_products.alias("src"), 
        "trg.product_id == src.product_id")\
            .whenMatchedUpdateAll(condition = "src.updated_at > trg.updated_at")\
            .whenNotMatchedInsertAll()\
            .execute()
else:
    # print("table doesn't exist table will be created with initial load")
    df_products.write\
                .format("delta")\
                .mode("overwrite")\
                .saveAsTable("azuredatabricks.silver.products")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from azuredatabricks.silver.products where product_id = 1010

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from azuredatabricks.silver.products

# COMMAND ----------

# MAGIC %md
# MAGIC # Bronze `Orders` table - READ

# COMMAND ----------

df_orders = spark.read.table("azuredatabricks.bronze.orders")

# COMMAND ----------

df_orders = df_orders.fillna(0,subset=["discount", "order_amount","quantity"])
df_orders = df_orders.fillna("9999-01-01", subset = ["order_date"])
df_orders = df_orders.fillna("Unknown",subset = ["payment_status"])
df_orders = df_orders.withColumn("silver_processed_at", current_timestamp())
df_orders = df_orders.dropDuplicates()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Complex date transformations

# COMMAND ----------

df_orders = df_orders.withColumn(
    "order_date",
    coalesce(
        try_to_date(col("order_date"), "yyyy-MM-dd"),
        try_to_date(col("order_date"), "dd-MM-yyyy"),
    ),
)
df_orders = df_orders.withColumn(
    "order_date",
    col("order_date").cast(TimestampType())
)

df_orders = df_orders.withColumn(
    "updated_at",
    from_unixtime(col("updated_at")/1000).cast(TimestampType())
)

display(df_orders)

# COMMAND ----------

from delta.tables import DeltaTable

# check if table exists
if spark.catalog.tableExists("azuredatabricks.silver.orders"):
    # print("table exists")
    delta_obj = DeltaTable.forName(spark, "azuredatabricks.silver.orders")

    delta_obj.alias("trg").merge(
        df_orders.alias("src"), 
        "trg.order_id == src.order_id")\
            .whenMatchedUpdateAll(condition = "src.updated_at > trg.updated_at")\
            .whenNotMatchedInsertAll()\
            .execute()
else:
    # print("table doesn't exist table will be created with initial load")
    df_orders.write\
                .format("delta")\
                .mode("overwrite")\
                .saveAsTable("azuredatabricks.silver.orders")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from azuredatabricks.silver.orders