import librosa
import numpy as np
import pandas as pd
import os

def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=10)  # Load audio file, limited to 30 seconds

    # Feature extraction
    features = {
        'filename': os.path.basename(file_path),
        'length': librosa.get_duration(y=y, sr=sr),
        'chroma_stft_mean': np.mean(librosa.feature.chroma_stft(y=y, sr=sr)),
        'chroma_stft_var': np.var(librosa.feature.chroma_stft(y=y, sr=sr)),
        'rms_mean': np.mean(librosa.feature.rms(y=y)),
        'rms_var': np.var(librosa.feature.rms(y=y)),
        'spectral_centroid_mean': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
        'spectral_centroid_var': np.var(librosa.feature.spectral_centroid(y=y, sr=sr)),
        'spectral_bandwidth_mean': np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
        'spectral_bandwidth_var': np.var(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
        'rolloff_mean': np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
        'rolloff_var': np.var(librosa.feature.spectral_rolloff(y=y, sr=sr)),
        'zero_crossing_rate_mean': np.mean(librosa.feature.zero_crossing_rate(y=y)),
        'zero_crossing_rate_var': np.var(librosa.feature.zero_crossing_rate(y=y)),
        'harmony_mean': np.mean(librosa.effects.harmonic(y=y)),
        'harmony_var': np.var(librosa.effects.harmonic(y=y)),
        'perceptr_mean': np.mean(librosa.effects.percussive(y=y)),
        'perceptr_var': np.var(librosa.effects.percussive(y=y)),
        'tempo': librosa.feature.rhythm.tempo(y=y, sr=sr)[0]
    }

    # MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    for i in range(1, 21):
        features[f'mfcc{i}_mean'] = np.mean(mfccs[i-1])
        features[f'mfcc{i}_var'] = np.var(mfccs[i-1])
    print(features)
    return features

# Load all files in a directory
def process_directory(directory_path):
    data = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            features = extract_features(file_path)
            data.append(features)
    return pd.DataFrame(data)

# Example usage
# Assuming your audio files are in the "genres_original/blues" directory
# df = process_directory("genres_original/blues")
# print(df.head())


extract_features("sunflower-street-drumloop-85bpm-163900.mp3")
