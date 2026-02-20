#!/usr/bin/env python3

from moviepy import VideoFileClip
import os
import sys
import matplotlib.pyplot as plt
import soundfile as sf

directory = '../media/Venezia'
filename = 'Rockefeller Street.mkv'

# Load the video file
video = VideoFileClip(os.path.join(directory, filename))

# Extract the audio from the video as a numpy array
sr = 48000
audio_array = video.audio.to_soundarray(fps=sr)
video.close()

# Write audio as wav file
sf.write("input_audio.wav", audio_array, sr)
