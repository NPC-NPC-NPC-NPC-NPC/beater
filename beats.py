#!/usr/bin/env python3

import argparse
import csv
import librosa
import numpy as np
import pretty_midi
import writema

def save_midi(onset_times, tempo, filename="drums.mid"):
    # Save as MIDI-file
    drum_inst = pretty_midi.Instrument(program=1, is_drum=True, name="drums")
    for i in range(len(onset_times)):

        # bass, pitch=35
        # snare, pitch=38
        # hihat, pitch=42
    
        note = pretty_midi.Note(velocity=100, pitch=35, start=onset_times[i]-0.02, end=onset_times[i] + 0.05)
        drum_inst.notes.append(note)

    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    midi.instruments.append(drum_inst)
    midi.write(filename)

def save_ma(onset_times, filename="timecode.xml"):
    # Save as MA time code
    writema.create_grandma3_timecode(
        filename=filename,
        duration=onset_times[-1],
        event_times=onset_times,
        sequence_number=101
    )

def save_csv(onset_times, filename="beats.csv"):
    with open(filename, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(onset_times)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--ma", action="store_true")
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--midi", action="store_true")
    parser.add_argument("--mode", type=str, default="onset")

    args = parser.parse_args()

    # Load audio file
    y, sr = librosa.load("drums.wav", sr=None)  # sr=None keeps original sample rate
    y = librosa.to_mono(y)
    
    # Detect tempo and beat frames
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo = tempo[0]
    
    # Dxact drum hit transients
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

    # Select bass or all
    if args.mode == "onset":
        frames = onset_frames
    else:
        frames = beat_frames

    # Loudness filtering
    onset_samples = librosa.frames_to_samples(frames)
    if args.mode == "onset":
        power = np.array([])
        for i in range(len(onset_samples)-1):
            max_time = 0.1 # Max integration time
            if (onset_samples[i+1] - onset_samples[i])/sr > max_time:
                end_sample = int(onset_samples[i] + max_time*sr)
            else:
                end_sample = onset_samples[i+1]

            s = y[onset_samples[i]:end_sample]
            power = np.append(power, np.dot(s,s)/len(s))

        #print(power)
        [n,edges] = np.histogram(power, bins = int(tempo/2 * len(y)/sr/60))
        
        # Only keep loud beats
        filtered_frames = []
        threshold = edges[1]
        for i in range(len(onset_samples)-1):
            if power[i] > threshold or (onset_samples[i+1] - onset_samples[i])/sr > 3.0:
                filtered_frames.append(frames[i])
            
    else:
        filtered_frames = frames
    
    # Samples and onset times
    onset_times = librosa.frames_to_time(filtered_frames, sr=sr)
    
    if args.ma:
        save_ma(onset_times)

    if args.csv:
        save_csv(onset_times)
    
    if args.midi:
        save_midi(onset_times, tempo)


if __name__ == "__main__":
    main()
