import os
import zipfile
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi


DATASET = "uciml/default-of-credit-card-clients-dataset"
DATA_DIR = Path("data/raw")


def download_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")

    if not username or not key:
        raise RuntimeError(
            "KAGGLE_USERNAME and KAGGLE_KEY environment variables "
            "must be configured"
        )

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files(
        DATASET,
        path=DATA_DIR,
        unzip=True,
    )

    print(f"Dataset downloaded to {DATA_DIR}")


if __name__ == "__main__":
    download_dataset()