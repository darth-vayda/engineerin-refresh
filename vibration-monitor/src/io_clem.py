import pandas as pd
from zipfile import ZipFile
from pathlib import Path
import pickle

DATA_FILE = "raw data.csv"

def import_data(data_path: Path) -> dict[str, pd.DataFrame]:

   # speichert die liste aller zip files in zip_paths
    zip_paths = sorted(data_path.glob("*.zip")) 

    # raise error if no zip file was found
    if not zip_paths: #wenn nix in der liste ist:
        raise   FileNotFoundError(f"Keine Zip files in {data_path.name} gefunden")

    measurements = {} #dictionary initialisieren

    for zip_path in zip_paths: #alle zip dateien durchgehen
        measurement_name = zip_path.stem #namen der zip datei speichern
        
        with ZipFile(zip_path, "r") as open_zipfile: # opens zip to read in open_zipfile
            data_file = None

            for zipname in open_zipfile.namelist(): #liest die dateien darin
                zipname_without_folder = zipname.rsplit("/",1)[-1] #gib den namen der datei zurück

                if zipname_without_folder.casefold() == DATA_FILE: # wenn es eine raw data.csv gibt
                    data_file = zipname # speichere den ganzen pfad in data_file
                    with open_zipfile.open(data_file) as data_file_csv:
                        data = pd.read_csv(data_file_csv) #lies die datei ein
                    break
      
            if data_file is None:
                raise FileNotFoundError( f"Keine '{DATA_FILE}' in {zip_path.name} gefunden.")
            
        #.rsplit=nimm nur den rechten letzten teil (zeit der messungen brauchen wir nicht)
        measurement_name_short = measurement_name.rsplit(" ",1)[-1]
        measurements[measurement_name_short] = data 
    return measurements

def select_measurement(
    measurements: dict[str, pd.DataFrame],
    fan: str,
    level: int,
    version: int,
) -> tuple[str, pd.DataFrame]:

    search_text = f"{fan}_level{level}_v{version:02d}"

    matches = [] #liste indizieren

    for name in measurements.keys():
        if search_text.casefold() in name.casefold(): # wenn der suchtext im dateinamen vorkommt
            matches.append(name) #häng den dateinamen in die liste

    if not matches:
        raise KeyError(f"Keine Messung für '{search_text}' gefunden.")

    if len(matches) > 1:
        raise ValueError(f"Mehrere Messungen für '{search_text}' gefunden: {matches}")

    selected_name = matches[0]
    selected_data = measurements[selected_name]

    return selected_name, selected_data