# Databricks notebook source
# MAGIC %md
# MAGIC ## Creating Managed Volume

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS dummy.ingest.managed_volume;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM csv.`/Volumes/dummy/ingest/managed_volume/rawdata/flights.csv`

# COMMAND ----------

df = spark.read.format('csv')\
    .option('header', 'true')\
    .option('inferSchema', 'true')\
    .load('/Volumes/dummy/ingest/managed_volume/rawdata/flights.csv')

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating External Volume

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL VOLUME IF NOT EXISTS dummmy.ingest.external_volume
# MAGIC LOCATION 'abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/volume_dir'

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM csv.`/Volumes/dummy/ingest/managed_volume/rawdata/flights.csv`