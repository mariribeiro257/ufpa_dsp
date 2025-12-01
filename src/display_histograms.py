import soundfile as sf
import os
import numpy as np
import matplotlib.pyplot as plt
import glob


def process_stats_file(file, outdir="histograms", bins=100):
    """Compute basic statistics of `file` and save an amplitude histogram to `outdir`.

    Prints: filename, duration, min, max, mean(abs)
    """
    data, sr = sf.read(file)
    if data.ndim > 1:
        data = data.mean(axis=1)

    duration = len(data) / sr
    min_amp = np.min(data)
    max_amp = np.max(data)
    mean_amp = np.mean(np.abs(data))

    print(f"{os.path.basename(file)} | dur: {duration:.2f}s | amp(min,max,mean)=({min_amp:.3f},{max_amp:.3f},{mean_amp:.3f})")

    plt.hist(data, bins=bins, color="steelblue", alpha=0.7)
    plt.title(f"Amplitude histogram - {os.path.basename(file)}")
    plt.xlabel("Amplitude")
    plt.ylabel("Count")
    plt.grid(True)
    os.makedirs(outdir, exist_ok=True)
    plt.savefig(os.path.join(outdir, f"{os.path.splitext(os.path.basename(file))[0]}_hist.png"), dpi=150)
    plt.close()


def process_folder(inputdir, outdir="histograms", bins=100, limit=None):
    """Process all .wav files under `inputdir`, compute stats and save histograms."""
    files = glob.glob(os.path.join(inputdir, "**", "*.wav"), recursive=True)
    if limit:
        files = files[:limit]
    for file in files:
        process_stats_file(file, outdir=outdir, bins=bins)


if __name__ == "__main__":
    DATASET_PATH = "./data/for_hist_tests/"
    process_folder(DATASET_PATH)