import soundfile as sf
import os, errno, sys
import matplotlib.pyplot as plt
import glob

def make_hist_file(file, outputdir):
    """
    Generate the amplitude histogram for a waveform file (.wav extension) 

    Parameters:
    file -> the path for a .wav file
    outputdir -> the path for the desired output directory 

    Returns:
    None
    """

    data, _ = sf.read(file) # Reading the .wav file

    if data.ndim > 1: # Checking if the audio is stereo or mono
        data = data.mean(axis=1) # Convert stereo to mono

    plt.hist(data, bins=100, color='steelblue', alpha=0.7) # Creating the wave amplitude histogram 
    plt.xlabel("Amplitude") # Label for x axis
    plt.ylabel("Count") # Label for y axis
    plt.grid(True) # Adds a grid for better visualization
    
    # Creating the path for saving the histogram png
    output_path = os.path.join(
        outputdir,
        f"{os.path.splitext(os.path.basename(file))[0]}_hist.png"
    )

    plt.savefig(output_path, dpi=150) 
    
    plt.close() # the figure must be deregistered explicitly to free memory

def process_folder(inputdir, outputdir):
    # Checking if outputdir already exists (important for avoiding overwriting existing files):
    try:
        os.makedirs(outputdir, exist_ok=False)
        print(f"Diretório '{outputdir}' criado.")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print(f"Erro: diretório '{outputdir}' já existe.")
            sys.exit(1)
        else:
            print(f"Erro inesperado na criação do diretório {outputdir}.")
            sys.exit(1)

    # Creating a list with all .wav files in the inputdir and its subdirectories:
    files = glob.glob(os.path.join(inputdir,"**", "*.wav"), recursive=True) 

    if not files: # Make sure that there are any .wav files in that folder
        print(f"There are no .wav files in folder '{inputdir}'.")
        sys.exit(1)
    
    for file in files:
        # Extracting the relative path for recreating the same inputdir structure on outputfolder:
        rel_path = os.path.relpath(file, inputdir) 
        
        sub_dir = os.path.join(
            outputdir,
            os.path.dirname(rel_path)
        )

        os.makedirs(sub_dir, exist_ok=True)

        make_hist_file(file, sub_dir) # Creating the hist for file



if __name__ == '__main__':
    if len(sys.argv) != 3: # Checking if user provided the inputfolder and outputfolder
        print("Usage: python create_pngs.py <inputfolder> <outputfolder>")
        sys.exit(1)
    
    inputfolder = sys.argv[1]
    outputfolder = sys.argv[2]

    process_folder(inputfolder, outputfolder)