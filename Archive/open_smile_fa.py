import opensmile
import numpy as np
import librosa
import pandas as pd

# Create a SMILE extractor object
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.GeMAPSv01b,
    feature_level=opensmile.FeatureLevel.Functionals,
)

# Load the audio file
audio_file = "/content/audio1.WAV"
signal, sr = librosa.load(audio_file, sr=None)

# Set the segment length in seconds
segment_length = 5

# Divide the audio into segments and extract features
features_list = []
for i, start in enumerate(range(0, len(signal), sr * segment_length)):
    end = min(start + sr * segment_length, len(signal))
    segment = signal[start:end]
    features = smile.process_signal(segment, sr)
    features_list.append(features.to_numpy().flatten())

# Convert the list of features to a pandas DataFrame
features_df = pd.DataFrame(features_list)
print(features_df.head())