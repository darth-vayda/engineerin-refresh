import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

def remove_dc_offset(measurements: dict[str, pd.DataFrame]) -> dict[str,pd.DataFrame]:
    centered_measurements = {}
    for name, data in measurements.items():
        centered_data = data.copy() # daten kopieren, damit 1. und 5. spalten erhalten bleiben
        acceleration_data = data.iloc[:,1:4] #.iloc ist die methode die ich brauche um auf spalten zuzugreifen
        centered_data.iloc[:,1:4] = acceleration_data - acceleration_data.mean(axis=0)
        # print(centered_data.iloc[:,1:4].mean(axis=0)) kontrolliere ob die daten ca null sind
        centered_name = f"{name}_centered" # _centered an namen dranhängen
        centered_measurements[centered_name] = centered_data
    return centered_measurements

def calc_fft(measurements: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    for name, data in measurements.items():
            delta_T = np.median(np.diff(data.iloc[:,0])) # np.diff = returns arry mit [T,T,T], np.meadian gibt einen durchschittswert aus dem array zurück
            N = data.iloc[:,1].size
            hann = np.hanning(N) # hann fenster erzeugen
            frequencies = np.fft.rfftfreq(N, d=delta_T)
            for signal_index in range(1,4):
                hann_data = data.iloc[:,signal_index] * hann
                # mache die fft von der jeweiligen spalte, dann betrag, normiere mit "n", also # von sampels 
                fft_abs_normiert = np.abs(np.fft.rfft(hann_data)) / hann.sum() # normieren durch die summe des hann fensters, nich mit "n"
                #*2 weil nur rechtsseitiges spektrum, nuller wert nicht mal zwei und bei geradem N letzten wert nicht verdoppeln
                if N % 2 == 0: #wenn N modul0 2 gleich 0 ist
                    fft_abs_normiert[1:-1] *= 2 
                else:
                    fft_abs_normiert[1:] *= 2
    return frequencies, fft_abs_normiert

# column_title = data.columns[signal_index].split("(",1)[0]
# plt.figure()
# plt.plot(frequencies, fft_abs_normiert)
# plt.title(f"{name}_{column_title}")
# plt.xlabel("Frequenz (Hz)")
# plt.ylabel("FFT-Betrag")
# plt.grid()
# file_path = RESULTS_DIR / f"{name}_{column_title}_fft.png"
# plt.savefig(file_path)
# plt.close()