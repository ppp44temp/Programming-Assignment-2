import sys
import os
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def validate_input_paths(train_path, val_path):
    if not (os.path.exists(train_path) and os.path.exists(val_path)):
        sys.exit(1)

def load_dataset(spark, file_path):
    return spark.read.option("header", True).option("inferSchema", True).csv(file_path)

def prepare_features(df, label="quality"):
    feature_columns = [col for col in df.columns if col != label]
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    return assembler.transform(df).select("features", label)

def train_random_forest(training_data):
    rf = RandomForestClassifier(labelCol="quality", featuresCol="features", numTrees=100, maxDepth=10)
    return rf.fit(training_data)

def evaluate_model(model, validation_data):
    predictions = model.transform(validation_data)
    evaluator = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction", metricName="f1")
    return evaluator.evaluate(predictions)

if len(sys.argv) != 3:
    sys.exit(1)

train_path, val_path = sys.argv[1], sys.argv[2]
validate_input_paths(train_path, val_path)

spark = SparkSession.builder.appName("WineQualityModelTraining").getOrCreate()

train_data = load_dataset(spark, train_path)
val_data = load_dataset(spark, val_path)

train_features = prepare_features(train_data)
val_features = prepare_features(val_data)

model = train_random_forest(train_features)
model.write().overwrite().save("trained_model")

f1 = evaluate_model(model, val_features)
print(f"Validation F1 Score: {f1:.4f}")

spark.stop()
