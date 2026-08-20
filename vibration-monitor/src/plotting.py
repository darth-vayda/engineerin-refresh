import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

def plot_all_data(measurements: dict[str, pd.DataFrame], results_dir: Path) -> None:
    for name, data in measurements.items():
        axis_labels = list(data.columns)
     
        fig, axes = plt.subplots(nrows=3, figsize=(14,9), dpi = 120, sharex=True)
       
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
        # existiert der ordner?, falls ja (exist_ok=True) mache weiter, sonst erstelle ihn samt parents
        results_dir.mkdir(parents=True, exist_ok=True) 
        file_path = results_dir / f"{name}.png"
        fig.savefig(file_path)
        plt.close(fig)

def plot_all_ffts_inkl_peaks(spectra: dict[str, pd.DataFrame], results_dir: Path, all_peaks: pd.DataFrame) -> None:
    frequencies = all_peaks["frequency"]
    for name, spectrum in spectra.items():
        frequencies = all_peaks["frequency"]
        amplitudes = all_peaks["amplitude"]
        axis_labels = list(spectrum.columns)

        fig, axes = plt.subplots(nrows=3, figsize=(14,9), dpi = 120, sharex=True)
        
        axes[0].plot(spectrum[axis_labels[0]],spectrum[axis_labels[1]],color="g")
        axes[0].set_title("Beschleunigung x")
        axes[0].set_ylabel("FFT-Betrag")
        axes[0].set_ylim(0, 0.03)    
        
        axes[1].plot(spectrum[axis_labels[0]],spectrum[axis_labels[2]],color="b")
        axes[1].set_title("Beschleunigung y")
        axes[1].set_ylabel("FFT-Betrag")
        axes[1].set_ylim(0, 0.03)      

        axes[2].plot(spectrum[axis_labels[0]],spectrum[axis_labels[3]],color="y")
        axes[2].set_title("Beschleunigung z")
        axes[2].set_ylabel("FFT-Betrag")
        axes[2].set_ylim(0, 0.03)

        axes[2].set_xlabel("Frequenz (Hz)")
# plot all selected peaks in right subplot
        
        mask1 = all_peaks["measurement"] == name
        filtered_frequencies_name = frequencies[mask1]
        filtered_amplitudes_name = amplitudes[mask1]
        
        mask2 = all_peaks["axis"] == axis_labels[1]
        filtered_frequencies_axis = filtered_frequencies_name[mask2]
        filtered_amplitudes_axis = filtered_amplitudes_name[mask2]
        axes[0].scatter(filtered_frequencies_axis, filtered_amplitudes_axis, color="red", marker="x")

        mask2 = all_peaks["axis"] == axis_labels[2]
        filtered_frequencies_axis = filtered_frequencies_name[mask2]
        filtered_amplitudes_axis = filtered_amplitudes_name[mask2]
        axes[1].scatter(filtered_frequencies_axis, filtered_amplitudes_axis, color="red", marker="x")

        mask2 = all_peaks["axis"] == axis_labels[3]
        filtered_frequencies_axis = filtered_frequencies_name[mask2]
        filtered_amplitudes_axis = filtered_amplitudes_name[mask2]
        axes[2].scatter(filtered_frequencies_axis, filtered_amplitudes_axis, color="red", marker="x")

        fig_name = f"{name}_fft"
        fig.suptitle(fig_name)
        fig.tight_layout(rect=[0,0,1,0.95]) # damit titel nicht überlappen
        # existiert der ordner?, falls ja (exist_ok=True) mache weiter, sonst erstelle ihn samt parents
        results_dir.mkdir(parents=True, exist_ok=True) 
        file_path = results_dir / f"{name}_fft_w_peaks.png"
        fig.savefig(file_path)
        plt.close(fig)

def plot_all_ffts(spectra: dict[str, pd.DataFrame], results_dir: Path) -> None:
    for name, spectrum in spectra.items():
        axis_labels = list(spectrum.columns)

        fig, axes = plt.subplots(nrows=3, figsize=(14,9), dpi = 120, sharex=True)

        axes[0].plot(spectrum[axis_labels[0]],spectrum[axis_labels[1]],color="g")
        axes[0].set_title("Beschleunigung x")
        axes[0].set_ylabel("FFT-Betrag")  
        
        axes[1].plot(spectrum[axis_labels[0]],spectrum[axis_labels[2]],color="b")
        axes[1].set_title("Beschleunigung y")
        axes[1].set_ylabel("FFT-Betrag")  

        axes[2].plot(spectrum[axis_labels[0]],spectrum[axis_labels[3]],color="y")
        axes[2].set_title("Beschleunigung z")
        axes[2].set_ylabel("FFT-Betrag")
        axes[2].set_xlabel("Frequenz (Hz)")

        fig_name = f"{name}_fft"
        fig.suptitle(fig_name)
        fig.tight_layout(rect=[0,0,1,0.95]) # damit titel nicht überlappen
        # existiert der ordner?, falls ja (exist_ok=True) mache weiter, sonst erstelle ihn samt parents
        results_dir.mkdir(parents=True, exist_ok=True) 
        file_path = results_dir / f"{name}_fft.png"
        fig.savefig(file_path)
        plt.close(fig)

def plot_one_measurement(name: str, data: pd.DataFrame) -> None:
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
    return fig, axes


def plot_rms_values(rms_values: pd.DataFrame, results_dir: Path)-> None:
    # code from codex start
    fig, ax = plt.subplots(figsize=(9,6))
    rms_values.boxplot(
    column="rms",
    by="level",
    ax=ax,
    )

    for level, group in rms_values.groupby("level"):
        x_positions = np.linspace(
            level + 1 - 0.12,
            level + 1 + 0.12,
            len(group),
        )

        ax.scatter(
            x_positions,
            group["rms"],
            color="red",
            zorder=3,
        )

    ax.set_xlabel("Ventilatorstufe")
    ax.set_ylabel("Gesamt-RMS (m/s²)")
    ax.set_title("RMS-Werte nach Ventilatorstufe")
    fig.suptitle("")
    fig.tight_layout()
    # code from codex end
    results_dir.mkdir(parents=True, exist_ok=True) 
    file_path = results_dir / "rms_boxplot.png"
    fig.savefig(file_path)
    plt.close(fig)
    return fig, ax