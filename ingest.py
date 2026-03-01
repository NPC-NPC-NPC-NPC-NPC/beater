#!/usr/bin/env python3

import argparse
from moviepy import VideoFileClip
import os
import sys
import matplotlib.pyplot as plt
import soundfile as sf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_video")

    args = parser.parse_args()

    # Load the video file
    video = VideoFileClip(args.input_video)

    # Extract the audio from the video as a numpy array
    sr = 48000
    audio_array = video.audio.to_soundarray(fps=sr)
    video.close()

    # Write audio as wav file
    sf.write("input_audio.wav", audio_array, sr)

if __name__ == "__main__":
    main()
    
