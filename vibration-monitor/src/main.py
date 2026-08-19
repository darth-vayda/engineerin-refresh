from src.io_clem import import_data
from src.io_clem import select_measurement
from src.plotting import plot_one_measurement
from src.plotting import plot_all_data
from src.plotting import plot_all_ffts
from src.plotting import plot_all_ffts_inkl_peaks
from src.signal_processing import choose_frame
from src.signal_processing import remove_dc_offset
from src.signal_processing import calc_fft
from src.features import extract_strongest_peaks
from src.features import extract_prominent_peaks
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# set folder and file to look for
ROOT_DIR = Path(__file__).absolute().parent.parent
DATA_DIR = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results"

def main() -> None:
    measurements = import_data(DATA_DIR)
    framed_measurements = choose_frame(measurements, 5,30)
    centered_measurements = remove_dc_offset(framed_measurements)
    # plot_all_data(centered_measurements, RESULTS_DIR) # activate/deactivate if you need to plot/replot data

    spectra = calc_fft(centered_measurements)

    # plot_all_ffts(spectra, RESULTS_DIR)

    strongest_peaks = extract_prominent_peaks(spectra)

    plot_all_ffts_inkl_peaks(spectra, RESULTS_DIR, strongest_peaks)
   
    print(type(spectra))


    # plot data
    # name, data = select_measurement(measurements,"fan",1,1)
    # plot_one_measurement(name, data)
    # c_name, c_data = select_measurement(c_measurements,"fan",1,1)
    # plot_one_measurement(c_name, c_data)
    # plt.show()




if __name__ == "__main__":
    main()

# print(f"{len(measurements)} Messungen geladen")

# for name, data in measurements.items():
#     print(f"{name}")
#     print(f"Dimension: {data.shape}")
#     print(f"Spalten: {list(data.axis_labels)}")
