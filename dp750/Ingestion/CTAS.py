# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE dummy.ingest.ctas_table
# MAGIC USING delta
# MAGIC LOCATION "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/ctas"
# MAGIC AS
# MAGIC SELECT * FROM dummy.ingest.flight_json
# MAGIC WHERE LoyaltyPoints IS NOT NULL

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dummy.ingest.ctas_table