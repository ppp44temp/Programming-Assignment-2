
# Programming Assignment 2

  

A scalable machine learning pipeline for predicting wine quality using Apache Spark's MLlib. Built for distributed computing environments such as AWS EMR, but can also be run locally using Docker.

  

## Overview
This project uses the `TrainingDataset.csv` and `ValidationDataset.csv` to train and validate a **Random Forest** model that predicts the quality of wine (on a scale of 1 to 10). The final model performance is reported using an **F1 Score**.  

## Setup Instructions
### 1. Clone the Repo

  

```bash

git  clone  https://github.com/ppp44temp/Programming-Assignment-2.git

cd  Programming-Assignment-2

```

### 2. Build the Docker Image  

Pull the image
```bash
docker  pull  ppp44/programmingassignment2
```

Build the image by running the following command:
```bash
docker build -t ppp44/programmingassignment2 .
```

### 3. Run the Container
```bash
docker run -it ppp44/programmingassignment2
```  

### 4. Get the Output

The ```output.txt``` should contain the F1 score. When the docker container is ran, the output should be at :
```bash
app\output.txt
```

### 5. Get the F1 Score

The ```output.txt``` file will contain the F1 score:
```
Validation F1 Score: 0.5264
```

## Cleanup

Remove all containers/images after testing:
```bash
docker  container  prune
docker  image  prune  -a
```
