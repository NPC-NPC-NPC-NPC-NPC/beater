import librosa
import numpy as np
import pretty_midi
import writema

# Load audio file
y, sr = librosa.load("drums.wav", sr=None)  # sr=None keeps original sample rate

# Detect tempo and beat frames
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Dxact drum hit transients
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

# Select bass or all
frames = beat_frames
#frames = onset_frames

# Samples and onset times
onset_samples = librosa.frames_to_samples(frames)
onset_times = librosa.frames_to_time(frames, sr=sr)

# Save as MIDI-file
drum_inst = pretty_midi.Instrument(program=1, is_drum=True, name="drums")
for i in range(len(onset_times)):

    # bass, pitch=35
    # snare, pitch=38
    # hihat, pitch=42
    
    note = pretty_midi.Note(velocity=100, pitch=35, start=onset_times[i]-0.02, end=onset_times[i] + 0.05)
    drum_inst.notes.append(note)

midi = pretty_midi.PrettyMIDI(initial_tempo=tempo[0])
midi.instruments.append(drum_inst)
midi.write("drums.mid")

# Save as MA time code
writema.create_grandma3_timecode(
    filename="timecode.xml",
    duration=onset_times[-1],
    event_times=onset_times,
    sequence_number=101
)
