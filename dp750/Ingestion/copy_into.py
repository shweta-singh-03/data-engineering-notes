# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS dummy.ingest;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dummy.ingest.flight_json;

# COMMAND ----------

# MAGIC %sql
# MAGIC COPY INTO dummy.ingest.flight_json
# MAGIC FROM "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/copyinto"
# MAGIC FILEFORMAT = JSON
# MAGIC FORMAT_OPTIONS ('mergeSchema' = 'true', 'multiline' = 'true')
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dummy.ingest.flight_json;