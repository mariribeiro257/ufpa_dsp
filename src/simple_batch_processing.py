import librosa
import soundfile as sf
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

def processing_file(file, N=100):
    y, sr = librosa.load(file, sr=None, mono=True)
    Ts = 1/sr # sampling period
    t = np.arange(len(y)) * Ts # creating a time vector for the signal 
    S = int(np.floor(len(y)/N)) # number of segments 
    e_segments = [] # array to store energy of segments of the signal
    t_segments = (np.arange(S) + 0.5) * N/sr # creating time vector for segments (the +0.5 is for shifting to the center of segments)
    for i in range(S):
        seg = y[i*N:(i*N + N)] # slicing a segment from the signal
        e_i = np.sum(seg * seg) # calculating the energy of the segment
        e_segments.append(e_i) # adding the value to the array
    print(f"Processed {os.path.basename(file)} → {len(e_segments)} segments") # printing the total of segments per file 
    return y, t, e_segments, t_segments

def plot_wave_and_energy(y, t, e_segments, t_segments, filename):
    plt.figure(figsize=(10,6)) # creating a "canvas" for the plots
    plt.suptitle(f"{filename}", fontsize=10)

    plt.subplot(211) # dividing figure into a grid; (211) is a short for (nrows=2, ncols=1, index=1)
    plt.plot(t, y) # plotting signal amplitude y versus time t
    plt.title("Waveform") # adds title to current subplot
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.autoscale(tight=False)
    plt.grid(True)

    plt.subplot(212) # selecting index=2
    plt.plot(t_segments, e_segments) # plotting energy per segment
    plt.title("Energy per segment") # adds title
    plt.xlabel("Time(s)")
    plt.ylabel("Energy")
    plt.autoscale(tight=False)
    plt.grid(True)

    plt.tight_layout() # adjusts automatically spacing between subplots
    
    os.makedirs("figures", exist_ok = True)
    plt.savefig(f"figures/{filename}.png", dpi=150) # saving picture of plots
    plt.close()



if __name__ == '__main__':
    DATASET_PATH = "./data/UrbanSound8k/fold1/"
    files = glob.glob(os.path.join(DATASET_PATH,"*.wav"))

    N = 100 # number of samples

    for file in tqdm(files, desc="Processing files"):
        filename = os.path.splitext(os.path.split(file)[1])[0]
        y, t, e_segments, t_segments = processing_file(file, N)
        plot_wave_and_energy(y,t,e_segments, t_segments, filename)
