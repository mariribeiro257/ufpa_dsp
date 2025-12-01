import soundfile as sf
import os
import numpy as np
import matplotlib.pyplot as plt
import glob

file = "data/for_hist_tests/7383-3-1-0.wav"

def process_stats_file(file):
    # Reading the waveform file:
    data, sr = sf.read(file)

    if data.ndim > 1: # Convert stereo to mono
        data = data.mean(axis=1)
    
    duration = len(data) / sr # Calculating the duration of wave file

    min_amp = np.min(data) # Extracting the minimum amplitude
    max_amp = np.max(data) # Extracting the maximum amplitude
    mean_amp = np.mean(np.abs(data)) # Extracting the amplitude mean

    print(f"{os.path.basename(file)} | dur: {duration:.2f}s | amp(min,max,mean)=({min_amp:.3f},{max_amp:.3f},{mean_amp:.3f})")

    plt.hist(data, bins=100, color='steelblue', alpha=0.7)
    plt.title(f"Amplitude histogram - {os.path.basename(file)}")
    plt.xlabel("Amplitude")
    plt.ylabel("Count")
    plt.grid(True)
    os.makedirs("histograms", exist_ok=True)
    plt.savefig(f"histograms/{os.path.splitext(os.path.basename(file))[0]}_hist.png", dpi=150)
    plt.close()

if __name__ == '__main__':
    DATASET_PATH = "./data/for_hist_tests/"
    files = glob.glob(os.path.join(DATASET_PATH,"*.wav"))

    for file in files:
        process_stats_file(file)