import pandas as pd
from zipfile import ZipFile
from pathlib import Path

# set root dir to "data" folder
ROOT_DIR = Path(__file__).absolute().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_FILE = "raw data.csv"

def import_data(data_path: Path) -> dict[str, pd.DataFrame]:
    # speichert die liste aller zip files in all_files
    zip_paths = sorted(data_path.glob("*.zip"))
    # raise error if no zip file was found
    if not zip_paths: #wenn nix in der liste ist:
        raise   FileNotFoundError(f"Keine Zip files in {data_path.name} gefunden")

    measurements = {}

    for zip_path in zip_paths:
        measurement_name = zip_path.stem
        
        with ZipFile(zip_path, "r") as open_zipfile: # opens zip to read in open_zipfile
            data_file = None
            for zipname in open_zipfile.namelist(): #liest die dateien darin
                zipname_without_folder = zipname.rsplit("/",1)[-1] #gib den namen der datei zurück

                if zipname_without_folder.casefold() == DATA_FILE: # wenn es eine raw data.csv gibt
                    data_file = zipname # speichere den ganzen pfad in data_file
                    with open_zipfile.open(data_file) as data_file_csv:
                        data = pd.read_csv(data_file_csv) #lies die datei ein
      
            if data_file is None:
                raise FileNotFoundError( f"Keine '{DATA_FILE}' in {zip_path.name} gefunden.")
        measurements[measurement_name] = data
    return measurements
    # for zip_file in data_path:

measurements = import_data(DATA_DIR)

print(f"{len(measurements)} Messungen geladen")

for name, data in measurements.items():
    print(f"{name}")
    print(f"Dimension: {data.shape}")
    print(f"Spalten: {list(data.columns)}")

    