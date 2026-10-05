# Databricks notebook source
# DBTITLE 1,Ingest csv form data lake/cloud storage
df = spark.read.format("csv")\
     .option("header", "true")\
     .option("inferSchema", "true")\
     .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/notebook/flights.csv")

# COMMAND ----------

# DBTITLE 1,Display the flights data
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Registering the Ingested data into External Table in unity catalog

# COMMAND ----------

# DBTITLE 1,Create external table from CSV
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dummy.raw.flights_table_ext 
# MAGIC USING delta
# MAGIC LOCATION "abfss://raw@databricksdp750storage.dfs.core.windows.net/external_table"
# MAGIC AS
# MAGIC SELECT * FROM read_files(
# MAGIC     "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/notebook/flights.csv",
# MAGIC     format => "csv",
# MAGIC     header => true
# MAGIC )
# MAGIC
# MAGIC -- SAME THING CAN BE DONE VIA SPARK! - REFER NOTEBOOK `API` to see that method, where we save the ingested data into datalake & created table(unity catalog object) on top of the ingested data using pyspark.
# MAGIC
# MAGIC -- here we are reading the files form the datalake & creating table on top of the ingested data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Confirm the table now exists and check its format
# MAGIC DESCRIBE DETAIL dummy.raw.flights_table_ext;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dummy.raw.flights_table_ext

# COMMAND ----------

# MAGIC %md
# MAGIC ### Registering the Ingested data into Managed Table in unity catalog

# COMMAND ----------

# DBTITLE 1,Creating managed table from CSV
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dummy.raw.flights_table_managed 
# MAGIC USING delta
# MAGIC AS
# MAGIC SELECT * FROM read_files(
# MAGIC     "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/notebook/flights.csv",
# MAGIC     format => "csv",
# MAGIC     header => true
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM dummy.raw.flights_table_managed