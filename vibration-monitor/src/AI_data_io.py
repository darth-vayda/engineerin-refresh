import pandas as pd
from pathlib import Path
from zipfile import ZipFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent 
# __file__: ist der ganze pfad von der datei, .resolve() gibt den 
# absoluten pfad zurück, .parent ein ordner rückwärts, also src, nochmal
# also vibration-monitor
DATA_DIR = PROJECT_ROOT / "data" # hängt den data ordner an. 
RAW_DATA_FILENAME = "raw data.csv"


def find_zip_files(folder: Path) -> list[Path]:
    """Find all ZIP files in a given folder."""
    return sorted(folder.glob("*.zip"))


def load_raw_data(zip_path: Path) -> pd.DataFrame:
    """Load Raw Data.csv directly from a ZIP archive."""
    with ZipFile(zip_path, "r") as archive:
        raw_data_path = None

        for filename in archive.namelist():
            filename_without_folder = filename.rsplit("/", 1)[-1]

            if filename_without_folder.casefold() == RAW_DATA_FILENAME:
                raw_data_path = filename
                break

        if raw_data_path is None:
            raise FileNotFoundError(
                f"Keine '{RAW_DATA_FILENAME}' in {zip_path.name} gefunden."
            )

        with archive.open(raw_data_path) as csv_file:
            data = pd.read_csv(csv_file)

    return data


def load_measurements(zip_files: list[Path]) -> dict[str, pd.DataFrame]:
    """Load all measurements and map them to their archive names."""
    measurements = {}

    for zip_path in zip_files:
        measurement_name = zip_path.stem

        if measurement_name in measurements:
            raise ValueError(f"Doppelter Messungsname: {measurement_name}")

        measurements[measurement_name] = load_raw_data(zip_path)

    return measurements


def main() -> None:
    zip_files = find_zip_files(DATA_DIR)

    if not zip_files:
        raise FileNotFoundError(
            f"Keine ZIP-Dateien in {DATA_DIR.resolve()} gefunden."
        )

    measurements = load_measurements(zip_files)

    print(f"{len(measurements)} Messungen geladen.")

    for name, data in measurements.items():
        print(f"\n{name}")
        print(f"Dimension: {data.shape}")
        print(f"Spalten: {list(data.columns)}")


if __name__ == "__main__":
    main()
