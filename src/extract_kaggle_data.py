"""
Step 1 - Data Extraction
Download the 'Sales of a Supermarket' dataset from Kaggle
and extract the CSV file locally.
"""

import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
DATASET = "lovishbansal123/sales-of-a-supermarket"
RAW_DATA_DIR = os.path.join(os.getcwd(), "data_raw")
ZIP_FILE = os.path.join(RAW_DATA_DIR, "supermarket_sales.zip")

# ---------------------------------------------------------------------
# Main extraction routine
# ---------------------------------------------------------------------
def download_kaggle_dataset():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    print(f"Downloading dataset to: {RAW_DATA_DIR}")

    api = KaggleApi()
    api.authenticate()

    # Download and unzip dataset
    api.dataset_download_files(DATASET, path=RAW_DATA_DIR, unzip=False)
    print("Download complete.")

    # Find downloaded zip (Kaggle saves as <dataset>.zip)
    downloaded_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".zip")]
    if not downloaded_files:
        raise FileNotFoundError("No zip file found after Kaggle download.")
    zip_path = os.path.join(RAW_DATA_DIR, downloaded_files[0])

    # Extract contents
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(RAW_DATA_DIR)
        print(f"Extracted: {zip_ref.namelist()}")

    print("\n Dataset extraction complete.")
    print(f"Files are now available in: {RAW_DATA_DIR}")

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    download_kaggle_dataset()
