import sys
import os
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def validate_paths(test_dir, model_dir):
    if not (os.path.isdir(test_dir) and os.path.isdir(model_dir)):
        sys.exit(1)

def load_test_data(spark, path):
    full_path = os.path.join(path, "*.csv")
    return spark.read.option("header", True).option("inferSchema", True).csv(full_path)

def assemble_features(data_frame, label="quality"):
    input_features = [col for col in data_frame.columns if col != label]
    assembler = VectorAssembler(inputCols=input_features, outputCol="features")
    return assembler.transform(data_frame).select("features", label)

def evaluate_model(model, data):
    evaluator = MulticlassClassificationEvaluator(
        labelCol="quality", predictionCol="prediction", metricName="f1"
    )
    return evaluator.evaluate(model.transform(data))

if len(sys.argv) != 3:
    sys.exit(1)

test_data_path, model_dir_path = sys.argv[1], sys.argv[2]
validate_paths(test_data_path, model_dir_path)

spark = SparkSession.builder.appName("PredictWineQuality").getOrCreate()

test_data = load_test_data(spark, test_data_path)
test_features = assemble_features(test_data)

model = RandomForestClassificationModel.load(model_dir_path)
f1 = evaluate_model(model, test_features)

print(f"F1 Score on Test Set: {f1:.4f}")

spark.stop()
