import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from audiocomplib import AudioCompressor

# Load audio file
y, sr = librosa.load('drums.wav')

# Display the original waveform
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Original Audio')

# Detect non-silent regions using librosa
non_silent_intervals = librosa.effects.split(y, top_db=18)

print(f"Detected {len(non_silent_intervals)} non-silent regions.")

for start, end in non_silent_intervals:
    # Calculate segment duration (ms)
    segment_ms = (end - start) / sr * 1000

    print(segment_ms)

# Minimum segment length [s]
min_segment_len = 0.09

# Create loudness meter
meter = pyln.Meter(sr, block_size=min_segment_len)

# Process each region separately
target_loudness = -18.0  # target LUFS
y_processed = np.zeros_like(y)

# Create compressor with your chosen parameters
compressor = AudioCompressor(
    threshold=-3.0,   # in dBFS
    ratio=6.0,
    attack_time_ms=5.0,
    release_time_ms=90.0,
    knee_width=3.0,
    makeup_gain=0.0
)

for start, end in non_silent_intervals:
    segment = y[start:end]
    
    segment_len = (end - start) / sr
    if segment_len < min_segment_len:
        continue

    # audiocomplib expects shape (channels, samples) as float32
    # since mono: reshape to (1, N)
    sig = segment.astype(np.float32)[None, :]

    # Process (compress) the signal
    compressed_sig = compressor.process(sig, sample_rate=sr)
    
    # Back to mono 1D array
    compressed_np = compressed_sig[0, :]

    # Measure loudness
    loudness = meter.integrated_loudness(compressed_np)

    # Normalize to target loudness
    segment_normalized = pyln.normalize.loudness(compressed_np, loudness, target_loudness)

    # Replace the original segment
    y_processed[start:end] = segment_normalized

# Write output file
sf.write("normalized_sections.wav", y_processed, sr)
        
# Display the trimmed waveform
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y_processed, sr=sr)
plt.title('Trimmed Audio')
plt.show()
