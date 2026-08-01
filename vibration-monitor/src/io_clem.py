import pandas as pd
import matplotlib.pyplot as plt
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
        measurements[measurement_name] = data
    return measurements

def plot_data(measurements: dict[str, pd.DataFrame]) -> None:
    for name, data in measurements.items():
        axis_labels = list(data.columns)
     
        fig, axes = plt.subplots(nrows=3)
       
        axes[0].plot(data[axis_labels[0]],data[axis_labels[1]],color="g")
        axes[0].set_title("Beschleunigung x")
        axes[0].set_ylabel("m/s²")  
        
        axes[1].plot(data[axis_labels[0]],data[axis_labels[2]],color="b")
        axes[1].set_title("Beschleunigung y")
        axes[1].set_ylabel("m/s²")  

        axes[2].plot(data[axis_labels[0]],data[axis_labels[3]],color="y")
        axes[2].set_title("Beschleunigung z")
        axes[2].set_ylabel("m/s²")
        axes[2].set_xlabel("Time (s)")

        fig.suptitle(name)
        fig.tight_layout(rect=[0,0,1,0.95]) # damit titel nicht überlappen
        plt.show()
       

def main() -> None:
    measurements = import_data(DATA_DIR)
    plot_data(measurements)


if __name__ == "__main__":
    main()



# print(f"{len(measurements)} Messungen geladen")

# for name, data in measurements.items():
#     print(f"{name}")
#     print(f"Dimension: {data.shape}")
#     print(f"Spalten: {list(data.axis_labels)}")

