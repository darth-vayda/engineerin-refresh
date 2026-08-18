import matplotlib.pyplot as plt
import pandas as pd

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