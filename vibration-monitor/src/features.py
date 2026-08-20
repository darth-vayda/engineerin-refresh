import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal

def extract_prominent_peaks(spectra: dict[str, pd.DataFrame])-> pd.DataFrame:
    strongest_peaks = []
    for name, spectrum in spectra.items():
        for column in spectrum.columns[1:4]:
            fft = spectrum[column]

            peak_indices, properties = find_peaks(fft,prominence = 0.35 *fft.max(), width=(1,None))
            peak_frequencies = spectrum.loc[peak_indices, "frequency"]
            peak_amplitudes = fft.loc[peak_indices]

            for counter, peak_index in enumerate(peak_indices):
                peak_frequency = peak_frequencies[peak_index]
                peak_amplitude = peak_amplitudes[peak_index]

                strongest_peak = {"measurement": name, 
                                "axis": column, 
                                "frequency": peak_frequency, 
                                "amplitude": peak_amplitude,
                                "index": peak_index}
                strongest_peaks.append(strongest_peak)
    strongest_peaks = pd.DataFrame(strongest_peaks)
    return strongest_peaks

def calc_rel_frequ_band_energy(spectra: dict[str, pd.DataFrame])-> pd.DataFrame:
    rel_energies = []
    for name, spectrum in spectra.items():
        column_names = spectrum.columns
        frequency = spectrum[column_names[0]]
        fft_x = spectrum[column_names[1]]
        fft_y = spectrum[column_names[2]]
        fft_z = spectrum[column_names[3]]

        power_spectrum = fft_x ** 2 + fft_y ** 2 + fft_z ** 2
        mask_band1 = ((frequency >= 0.2) & (frequency < 5))
        mask_band2 = ((frequency >= 5) & (frequency < 15))
        mask_band3 = ((frequency >= 15) & (frequency < 30))
        mask_band4 = ((frequency >= 30) & (frequency <= 50))

        energy_band1 = np.sum(power_spectrum[mask_band1])
        energy_band2 = np.sum(power_spectrum[mask_band2])
        energy_band3 = np.sum(power_spectrum[mask_band3])
        energy_band4 = np.sum(power_spectrum[mask_band4])
        energy = energy_band1 + energy_band2 + energy_band3 + energy_band4

        rel_energy_band1 = energy_band1 / energy
        rel_energy_band2 = energy_band2 / energy
        rel_energy_band3 = energy_band3 / energy
        rel_energy_band4 = energy_band4 / energy

        rel_energy = {"measurement": name,
                      "rel_energy_0_5": rel_energy_band1,
                      "rel_energy_5_15": rel_energy_band1,
                      "rel_energy_15_30": rel_energy_band1,
                      "rel_energy_30_50": rel_energy_band1,}
        rel_energies.append(rel_energy)
    return pd.DataFrame(rel_energies)

# Codex version of calc_rel_frequ_band_energy
# def calc_relative_frequency_band_energy(
#     spectra: dict[str, pd.DataFrame],
# ) -> pd.DataFrame:

#     frequency_bands = {
#         "0_5": (0.2, 5.0),
#         "5_15": (5.0, 15.0),
#         "15_30": (15.0, 30.0),
#         "30_50": (30.0, 50.0),
#     }

#     feature_rows = []

#     for measurement_name, spectrum in spectra.items():
#         frequencies = spectrum["frequency"]

#         acceleration_spectra = spectrum.iloc[:, 1:4]
#         power_spectrum = acceleration_spectra.pow(2).sum(axis=1)

#         analysis_mask = (
#             (frequencies >= 0.2)
#             & (frequencies <= 50.0)
#         )

#         total_energy = power_spectrum.loc[analysis_mask].sum()

#         if total_energy <= 0:
#             raise ValueError(
#                 f"Keine positive spektrale Energie in "
#                 f"'{measurement_name}' gefunden."
#             )

#         feature_row = {
#             "measurement": measurement_name,
#         }

#         number_of_bands = len(frequency_bands)

#         for band_index, (band_name,(lower_frequency, upper_frequency),) in enumerate(frequency_bands.items()):

#             is_last_band = band_index == number_of_bands - 1

#             if is_last_band:
#                 band_mask = (
#                     (frequencies >= lower_frequency)
#                     & (frequencies <= upper_frequency)
#                 )
#             else:
#                 band_mask = (
#                     (frequencies >= lower_frequency)
#                     & (frequencies < upper_frequency)
#                 )

#             band_energy = power_spectrum.loc[band_mask].sum()
#             relative_energy = band_energy / total_energy

#             feature_row[f"rel_energy_{band_name}"] = relative_energy

#         feature_rows.append(feature_row)

#     return pd.DataFrame(feature_rows)

        



def calc_RMS(centered_measurements: dict[str, pd.DataFrame])-> pd.DataFrame:
    rms_values = []
    for name, measurement in centered_measurements.items():
        column_names = measurement.columns
        acc_x = measurement[column_names[1]]
        acc_y = measurement[column_names[2]]
        acc_z = measurement[column_names[3]]

        acc_xyz_squared = acc_x ** 2 + acc_y **2 + acc_z ** 2
        rms = np.sqrt(np.mean(acc_xyz_squared))
        level = int(name.split("_")[1].split("l")[-1])
        rms_value = {"measurement": name,
                     "level": level,
                     "rms": rms}
        rms_values.append(rms_value)
    return pd.DataFrame(rms_values)




    



# x-, y- und z-Spalten auswählen
# → quadrieren
# → pro Zeitpunkt addieren
# → Mittelwert über alle Zeitpunkte
# → Quadratwurzel

def extract_strongest_peaks(spectra: dict[str, pd.DataFrame])-> pd.DataFrame:
    strongest_peaks = []
    for name, spectrum in spectra.items():
        for column in spectrum.columns[1:4]:
            fft = spectrum[column]

            peak_index = fft.idxmax()
            peak_frequency = spectrum.loc[peak_index, "frequency"]
            peak_amplitude = fft.loc[peak_index]
            
            strongest_peak = {"measurement": name, 
                            "axis": column, 
                            "frequency": peak_frequency, 
                            "amplitude": peak_amplitude}
            strongest_peaks.append(strongest_peak)
    strongest_peaks = pd.DataFrame(strongest_peaks)
    return strongest_peaks

def extract_strongest_x_peaks(spectra: dict[str, pd.DataFrame])-> pd.DataFrame:
    strongest_peaks = []
    
    for name, spectrum in spectra.items():
        axis_name = spectrum.columns[1]
        x_fft = spectrum[axis_name]

        peak_index = x_fft.idxmax()
        peak_frequency = spectrum.loc[peak_index, "frequency"]
        peak_amplitude = x_fft.loc[peak_index]
        
        strongest_peak = {"measurement": name, 
                          "axis": axis_name, 
                          "frequency": peak_frequency, 
                          "amplitude": peak_amplitude}
        strongest_peaks.append(strongest_peak)
    strongest_peaks = pd.DataFrame(strongest_peaks)
    return strongest_peaks