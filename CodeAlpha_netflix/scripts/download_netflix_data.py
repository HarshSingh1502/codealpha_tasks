"""Download the Netflix titles dataset from a public source."""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import NETFLIX_DATASET_FILE, NETFLIX_URL, RAW_DATA_DIR  # noqa: E402

RAW_PATH = RAW_DATA_DIR / NETFLIX_DATASET_FILE


def main() -> None:
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading from {NETFLIX_URL} ...")
    df = pd.read_csv(NETFLIX_URL)
    df.to_csv(RAW_PATH, index=False)
    print(f"Saved {len(df):,} titles -> {RAW_PATH}")


if __name__ == "__main__":
    main()
