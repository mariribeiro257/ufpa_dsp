import librosa
import soundfile as sf
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
from tqdm import tqdm


def processing_file(file, N=100):
    """Read `file` and compute energy per window of N samples.

    Returns:
        y: waveform array (mono)
        t: time vector for waveform
        e_segments: list of energy values per segment
        t_segments: center times for each segment
    """
    y, sr = librosa.load(file, sr=None, mono=True)
    Ts = 1 / sr
    t = np.arange(len(y)) * Ts
    S = int(np.floor(len(y) / N))
    e_segments = []
    t_segments = (np.arange(S) + 0.5) * N / sr
    for i in range(S):
        seg = y[i * N:(i * N + N)]
        e_i = np.sum(seg * seg)
        e_segments.append(e_i)
    print(f"Processed {os.path.basename(file)} → {len(e_segments)} segments")
    return y, t, e_segments, t_segments


def plot_wave_and_energy(y, t, e_segments, t_segments, filename, outdir="figures"):
    """Plot waveform and per-segment energy and save figure to `outdir`.

    Parameters:
        y, t, e_segments, t_segments: outputs from `processing_file`
        filename: base filename (no extension) to use when saving
        outdir: directory where the figure will be saved
    """
    plt.figure(figsize=(10, 6))
    plt.suptitle(f"{filename}", fontsize=10)

    plt.subplot(211)
    plt.plot(t, y)
    plt.title("Waveform")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.autoscale(tight=False)
    plt.grid(True)

    plt.subplot(212)
    plt.plot(t_segments, e_segments)
    plt.title("Energy per segment")
    plt.xlabel("Time(s)")
    plt.ylabel("Energy")
    plt.autoscale(tight=False)
    plt.grid(True)

    plt.tight_layout()

    os.makedirs(outdir, exist_ok=True)
    plt.savefig(os.path.join(outdir, f"{filename}.png"), dpi=150)
    plt.close()


def process_folder(inputdir, N=100, limit=None, outdir="figures"):
    """Recursively process audio files under `inputdir`.

    Parameters:
        inputdir: root folder to search for .wav files
        N: window size in samples
        limit: optional maximum number of files to process
        outdir: directory where figures will be saved
    """
    files = glob.glob(os.path.join(inputdir, "**", "*.wav"), recursive=True)
    if limit:
        files = files[:limit]
    for file in tqdm(files, desc="Processing files"):
        filename = os.path.splitext(os.path.split(file)[1])[0]
        y, t, e_segments, t_segments = processing_file(file, N)
        plot_wave_and_energy(y, t, e_segments, t_segments, filename, outdir=outdir)


if __name__ == "__main__":
    DATASET_PATH = "./data/UrbanSound8k/fold1/"
    N = 100
    process_folder(DATASET_PATH, N=N)
