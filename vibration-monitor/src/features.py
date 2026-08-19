import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def extract_prominent_peaks(spectra: dict[str, pd.DataFrame])-> pd.DataFrame:
    strongest_peaks = []
    for name, spectrum in spectra.items():
        for column in spectrum.columns[1:4]:
            fft = spectrum[column]

            peak_indices, properties = find_peaks(fft,prominence = 0.20 *fft.max(), width=(2,3.5))
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