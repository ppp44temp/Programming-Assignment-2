FROM bitnami/spark:latest

WORKDIR /app

COPY training.py prediction.py clean_data.py main.py ./

COPY TrainingDataset.csv ValidationDataset.csv ./

RUN pip3 install pandas numpy

ENV PYSPARK_PYTHON=python3

CMD ["spark-submit", "run_model.py", "TrainingDataset.csv", "ValidationDataset.csv"]
