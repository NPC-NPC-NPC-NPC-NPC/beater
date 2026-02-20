import demucs.separate
import shlex
import os

def separate_drums(input_audio_path: str, model: str = "htdemucs_ft", out_dir: str = "separated"):
    # Build arguments
    args = [
        "-n", model,                 # Model choice (you can change to other models)
        "--two-stems", "drums",      # Separate drums and vocals or other stems
        "-o", out_dir,               # Output directory
        input_audio_path             # Input file path
    ]
    # Run separation
    demucs.separate.main(args)

    # Path to the isolated drum audio file (after separation)
    out_path = f"{out_dir}/{model}/input_audio/drums.wav"
    return out_path

# Separate the drums from the full mix
drum_audio_path = separate_drums("input_audio.wav")
os.rename(drum_audio_path, "./drums.wav")
