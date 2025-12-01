import numpy as np
import soundfile as sf
import glob
import os
import matplotlib.pyplot as plt


def find_global_range(files):
    """Return (vmin, vmax) across all files provided."""
    vmin, vmax = np.inf, -np.inf
    for file in files:
        data, _ = sf.read(file)
        if data.ndim > 1:
            data = data.mean(axis=1)
        vmin = min(vmin, data.min())
        vmax = max(vmax, data.max())
    return vmin, vmax


def extract_all_hist(files, bins):
    """Accumulate histogram counts for all files using given `bins`."""
    hist_total = np.zeros(len(bins) - 1)
    for file in files:
        data, _ = sf.read(file)
        if data.ndim > 1:
            data = data.mean(axis=1)
        hist, _ = np.histogram(data, bins)
        hist_total += hist
    return hist_total


def compute_global_histogram(input_dir, n_intervals=200, outpath="global_hist.png", limit=None):
    """Compute and save a global amplitude histogram for all .wav files under `input_dir`."""
    files = glob.glob(os.path.join(input_dir, "**", "*.wav"), recursive=True)
    if limit:
        files = files[:limit]
    if not files:
        raise ValueError(f"No .wav files found in {input_dir}")
    vmin, vmax = find_global_range(files)
    bins = np.linspace(vmin, vmax, n_intervals + 1)
    hist_total = extract_all_hist(files, bins)

    plt.figure()
    plt.bar((bins[:-1] + bins[1:]) / 2, hist_total, width=(bins[1] - bins[0]))
    plt.xlabel("Amplitude")
    plt.ylabel("Count")
    plt.title("Global amplitude histogram")
    plt.savefig(outpath, dpi=150)
    plt.close()


if __name__ == "__main__":
    files_dir = "data/UrbanSound8k/fold1"
    compute_global_histogram(files_dir, n_intervals=200)


