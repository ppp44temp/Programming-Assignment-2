import sys
from pyspark.sql import SparkSession

if len(sys.argv) != 3:
    sys.exit(1)

input_file, output_dir = sys.argv[1], sys.argv[2]

spark = SparkSession.builder.appName("WineDataCleaner").getOrCreate()

data_frame = (
    spark.read.option("header", "true").option("delimiter", ";").option("quote", '"').csv(input_file)
)

updated_columns = [
    col_name.strip().replace('"""', '').replace('""', '').replace('"', '') 
    for col_name in data_frame.columns
]
cleaned_data = data_frame.toDF(*updated_columns)

(
    cleaned_data.write.mode("overwrite").option("header", "true").csv(output_dir)
)

spark.stop()