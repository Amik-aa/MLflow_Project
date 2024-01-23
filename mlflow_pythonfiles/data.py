import os
import zipfile
import kaggle
def load_raw_data(dset_name):
    zip_destination_folder = "./data/"
    raw_destination_folder = os.path.join(zip_destination_folder, "raw")

     if not os.path.exists(os.path.expanduser("~/.kaggle/kaggle.json")):
        raise Exception(
            "Kaggle API key not found."
        )
     # Checking if the Kaggle API key was created
   
    kaggle.api.dataset_download_files(
        dset_name,
        path=zip_destination_folder,
    )
     # Downloading the dataset into a current folder
    if not os.path.exists(raw_destination_folder):
        os.makedirs(raw_destination_folder)
    # Checking if the destination folder exists, and create it if it does not
   
    zip_name = os.path.join(
        zip_destination_folder, "bank-account-fraud-dataset-neurips-2022.zip"
    )
    with zipfile.ZipFile(zip_name, "r") as zip_ref:
        zip_ref.extractall(raw_destination_folder)

    csv_location = os.path.join(raw_destination_folder, "Base.csv")

    return csv_location