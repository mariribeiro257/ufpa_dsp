import numpy as np
import soundfile as sf
import glob
import os
import matplotlib.pyplot as plt

def find_global_range(files):
    vmin, vmax = np.inf, -np.inf

    for file in files:
        data, _ = sf.read(file)
        if data.ndim > 1:
            data = data.mean(axis=1)
        vmin = min(vmin, data.min())
        vmax = max(vmax, data.max())
    return vmin, vmax
    

def extract_all_hist(files, bins):
    hist_total = np.zeros(len(bins) - 1)

    for file in files:
        data, _ = sf.read(file)
        if data.ndim > 1:
            data = data.mean(axis=1)
        hist, _ = np.histogram(data, bins)
        hist_total += hist
    
    return hist_total


if __name__ == '__main__':
    files_dir = "data/UrbanSound8k/fold1"

    files = glob.glob(os.path.join(files_dir, "*.wav"))

    vmin, vmax = find_global_range(files)

    n_intervals = 200
    
    # Creating a array of evenly spaced numbers over an interval:
    bins = np.linspace(vmin,vmax,n_intervals+1) # start: -1; stop: 1; intervals borders: 201 (creates 200 intervals) 

    hist_total = extract_all_hist(files, bins)


    # Plot
    plt.figure()
    plt.bar((bins[:-1] + bins[1:]) / 2, hist_total, width=(bins[1] - bins[0]))
    plt.xlabel("Amplitude")
    plt.ylabel("Count")
    plt.title("Global amplitude histogram")
    plt.savefig("global_hist2.png", dpi=150)
    plt.close()


