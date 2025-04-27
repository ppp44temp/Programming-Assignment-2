import sys
import os
import subprocess

def validate_inputs(args):
    if len(args) != 3:
        sys.exit(1)

def execute_command(command):
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return process.stdout, process.returncode

def check_file_exists(file_path, description):
    if not os.path.isfile(file_path):
        sys.exit(1)

def run_pipeline(train_file, val_file):
    log_output = ""

    cleaned_train = "cleaned_train.csv"
    cleaned_val = "cleaned_validation.csv"

    for description, src, dest in [("Training", train_file, cleaned_train), ("Validation", val_file, cleaned_val)]:
        out, code = execute_command(["spark-submit", "clean_data.py", src, dest])
        # log_output += f"=== Cleaning {description} Dataset ===\n{out}\n"
        # if code != 0:
        #     log_output += f"[Error] Cleaning {description.lower()} dataset failed.\n"

    out, code = execute_command(["spark-submit", "training.py", cleaned_train, cleaned_val])
    # log_output += f"=== Model Training ===\n{out}\n"
    # if code != 0:
    #     log_output += "[Error] Model training failed.\n"

    out, code = execute_command(["spark-submit", "prediction.py", cleaned_val, "trained_model"])
    log_output += f"=== Prediction ===\n{out}\n"
    # if code != 0:
    #     log_output += "[Error] Model prediction failed.\n"

    return log_output

def main():
    validate_inputs(sys.argv)

    train_data_path = sys.argv[1]
    val_data_path = sys.argv[2]

    check_file_exists(train_data_path, "Training file")
    check_file_exists(val_data_path, "Validation file")

    # logs = run_pipeline(train_data_path, val_data_path)

    with open("output.txt", "w") as f:
        f.write(logs)

if __name__ == "__main__":
    main()