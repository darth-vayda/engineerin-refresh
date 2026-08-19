import numpy as np
import pandas as pd
from scipy import signal


def choose_frame(measurements: dict[str, pd.DataFrame], start_time: int, end_time: int) -> dict[str, pd.DataFrame]:
    framed_measurements = {}
    for name, data in measurements.items():
        column_names = list(data.columns)
        #nur daten wählen, die zwischen start_time (sek) und end_time (sek) sind
        mask = ((data[column_names[0]] >= start_time) & (data[column_names[0]] <= end_time))
        selected_data = data.loc[mask]
        name_framed = f"{name}_framed"
        framed_measurements[name_framed] = selected_data
    return framed_measurements


def remove_dc_offset(measurements: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    centered_measurements = {}
    for name, data in measurements.items():
        centered_data = data.copy() # daten kopieren, damit 1. und 5. spalten erhalten bleiben
        acceleration_data = data.iloc[:,1:4] #.iloc ist die methode die ich brauche um auf spalten zuzugreifen
        centered_data.iloc[:,1:4] = acceleration_data - acceleration_data.mean(axis=0)
        # print(centered_data.iloc[:,1:4].mean(axis=0)) kontrolliere ob die daten ca null sind
        name_centered = f"{name}_centered" # _centered an namen dranhängen
        centered_measurements[name_centered] = centered_data
    return centered_measurements

def calc_fft(measurements: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    spectra = {}
    for name, data in measurements.items():
        delta_T = np.median(np.diff(data.iloc[:,0])) # np.diff = returns arry mit [T,T,T], np.meadian gibt einen durchschittswert aus dem array zurück
        N = data.iloc[:,1].size
        hann = np.hanning(N) # hann fenster erzeugen
        frequency = np.fft.rfftfreq(N, d=delta_T)
        spectrum_data = {"frequency": frequency}
        for signal_index in range(1,4):
            hann_data = data.iloc[:,signal_index] * hann
            # mache die fft von der jeweiligen spalte, dann betrag, normiere mit "n", also # von sampels 
            fft_abs_normiert = np.abs(np.fft.rfft(hann_data)) / hann.sum() # normieren durch die summe des hann fensters, nich mit "n"
            #*2 weil nur rechtsseitiges spektrum, nuller wert nicht mal zwei und bei geradem N letzten wert nicht verdoppeln
            if N % 2 == 0: #wenn N modul0 2 gleich 0 ist
                fft_abs_normiert[1:-1] *= 2 
            else:
                fft_abs_normiert[1:] *= 2
            column_name = data.columns[signal_index].split("(",1)[0].strip()
            spectrum_data[column_name] = fft_abs_normiert
        spectra[name] = pd.DataFrame(spectrum_data)
    return spectra