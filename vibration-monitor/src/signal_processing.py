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
        print(centered_data.iloc[:,1:4].mean(axis=0))
        centered_name = f"{name}_centered" # _centered an namen dranhängen
        centered_measurements[centered_name] = centered_data
    return centered_measurements

# def calc_fft(measurements: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]: