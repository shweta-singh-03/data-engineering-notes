# Databricks notebook source
# MAGIC %md
# MAGIC ## addNewColumns

# COMMAND ----------

checkpoint_location = "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_sink/checkpoint"

schema_location = "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_sink/checkpoint/schema_location"

# COMMAND ----------

df = spark.readStream.format("cloudFiles")\
    .option("cloudFiles.format", "json")\
    .option("multiLine", "true")\
    .option("cloudFiles.schemaLocation", schema_location)\
    # .option("cloudFiles.schemaEvolutionMode", "addNewColumns")\ 
    .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_raw/")\
    .writeStream.format("delta")\
    .option("checkpointLocation", checkpoint_location)\
    .trigger(once=True)\
    .option("mergeSchema", "true")\
    .option("path","abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_sink/data")\
    .start()

# COMMAND ----------

df = spark.read.format("delta")\
    .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_sink/data")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## rescue

# COMMAND ----------

checkpoint_location = "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_sink_rescue/checkpoint"

schema_location = "abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_sink_rescue/checkpoint/schema_location"

# COMMAND ----------

df = spark.readStream.format("cloudFiles")\
    .option("cloudFiles.format","json")\
    .option("multiline","true")\
    .option("cloudFiles.schemaLocation",schema_location)\
    .option("cloudFiles.schemaEvolutionMode","rescue")\
    .load("abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_raw/")\
    .writeStream.format("delta")\
    .option("checkpointLocation",checkpoint_location)\
    .trigger(once=True)\
    .option("path","abfss://raw@databricksdp750storage.dfs.core.windows.net/standard/autoloader_sink_rescue/data")\
    .toTable("dummy.ingest.autoloader_rescue")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dummy.ingest.autoloader_rescue