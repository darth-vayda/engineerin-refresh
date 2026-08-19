import numpy as np
import pandas as pd
from src.signal_processing import calc_fft

def test_fft_frequency_and_amplitude():
    generated_sinus = {}

    # generate time axis
    f_s = 100
    T = 1/f_s
    duration = 25
    time = np.arange(0,duration,T)

    # generate sinus
    signal_frequency = 15
    amplitude = 1.0
    sinus_x = amplitude *np.sin(2 * np.pi * signal_frequency * time)
    zeros_y = np.zeros_like(time)
    zeros_z = zeros_y

    sinus_data = pd.DataFrame({"Time (s)": time,
                               "Acceleration x": sinus_x,
                               "Acceleration y": zeros_y,
                               "Acceleration z": zeros_z,})
    generated_sinus["sinus_15_Hz"] = sinus_data

    #call calc fft
    sinus_fft = calc_fft(generated_sinus)

    sinus_data = sinus_fft["sinus_15_Hz"]
    fft_values = sinus_data["Acceleration x"]
    peak_index = np.argmax(fft_values)

    peak_frequency = sinus_data["frequency"].iloc[peak_index]
    peak_amplitude = fft_values.iloc[peak_index]
    print(peak_frequency)
    print(peak_amplitude)
    assert np.isclose(peak_frequency, signal_frequency,atol=1/duration)
    assert np.isclose(peak_amplitude, amplitude, rtol=0.01)
