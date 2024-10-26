from pyspark.sql import SparkSession
import tempfile
import os

# Create a temporary directory for table storage
temp_dir = tempfile.mkdtemp()
table_location = f"file://{temp_dir}/unity_catalog_tables"

# Create SparkSession
spark = SparkSession.builder \
    .appName("local-uc-test") \
    .master("local[*]") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.1,io.unitycatalog:unitycatalog-spark_2.12:0.2.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.catalog.unity", "io.unitycatalog.spark.UCSingleCatalog") \
    .config("spark.sql.catalog.unity.uri", "http://localhost:8080") \
    .config("spark.sql.defaultCatalog", "unity") \
    .getOrCreate()

# Your PySpark code goes here

# create a table and display it using pyspark

# Create a sample DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Create a table from the DataFrame
catalog_name = "unity"  # This should match your Unity Catalog name
schema_name = "default"  # Replace with your desired schema name
table_name = "sampletable"
full_table_name = f"{catalog_name}.{schema_name}.{table_name}"

# Create the schema if it doesn't exist
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")

# Create a table from the DataFrame with a specified location
df.write.mode("overwrite").option("path", f"{table_location}/{table_name}").saveAsTable(full_table_name)

# Display the table contents
print(f"Contents of {full_table_name}:")
spark.table(full_table_name).show()

# Don't forget to stop the SparkSession when you're done
spark.stop()

# Clean up the temporary directory
os.system(f"rm -rf {temp_dir}")
