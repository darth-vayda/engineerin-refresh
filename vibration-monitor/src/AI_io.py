import pandas as pd
from pathlib import Path
from zipfile import ZipFile

DATA_DIR = Path("data")
RAW_DATA_FILENAME = "raw data.csv"
# gibt den vollen pfad zurück in dem der Ordner "data" liegt

def find_zip_files(folder: Path) -> list[Path]:
    """finds all zip files in a given folder"""
    return sorted(folder.glob("*.zip"))

def show_zip_contents(zip_path: Path) -> None:
    """shows all files in a zip archive"""
    print(f"\nArchiv: {zip_path.name}")

    with ZipFile(zip_path, "r") as archive:
        for filename in archive.namelist():
            print(f" {filename}")


def load_raw_data(zip_path: Path) -> pd.DataFrame:
    """lädt raw data.csv direkt aus einem zip archiv"""

    with ZipFile(zip_path, "r") as archive:
        raw_data_path = None

        for 
   



def main() -> None:
    zip_files = find_zip_files(DATA_DIR)

    print(f"{len(zip_files)} ZIP-Dateien gefunden")

    if not zip_files:
        raise FileNotFoundError(
            f"Keine Zip-Dateien in {DATA_DIR.resolve()} gefunden."
        )

    for zip_path in zip_files:
        """geht alle arichve durch"""
        show_zip_contents(zip_path)

if __name__ == "__main__":
    main()


# data = pd.read_csv("./data/.csv")

# print(data.head())
# print(data.columns)