import mlflow

import sys
from mlflow_pythonfiles.data import load_raw_data
from mlflow_pythonfiles.data_preprocessing import preprocess_data
from mlflow_pythonfiles.Model_Tuning import tune_model
from mlflow_pythonfiles.model_training import train_model
def pipeline():
    mlflow.set_experiment("DetectionFraud")
    file_location = load_raw_data(sys.argv[1])

    file_dirs = data_preprocessing(file_location, missing_thr=0.95)
    best_params = Model_Tuning(
        train_path=file_dirs["train-data-dir"],
        val_path=file_dirs["val-data-dir"],
        n_trials=int(sys.argv[2]),
    )
    print("HP tuning is finished")
    best_params["n_estimators"] = 1000
    best_params["objective"] = "Logloss"

    roc, pr = model_training(
        best_params,
        train_path=file_dirs["train-data-dir"],
        val_path=file_dirs["val-data-dir"],
        test_path=file_dirs["test-data-dir"],
    )
    print("Final model is trained")


if __name__ == "__main__":
    pipeline()
