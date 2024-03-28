import pandas as pd
import wave
import numpy as np
from python_speech_features import fbank
from python_speech_features import mfcc




def extract_mfcc(wav_file,window):
    # Open the WAV file
    with wave.open(wav_file, 'rb') as wav:
        # Get the audio data
        frames = wav.readframes(-1)
        signal = np.frombuffer(frames, dtype='int16')

        # Get the sample rate
        sample_rate = wav.getframerate()

    # Extract MFCC features
    mfcc_features = mfcc(signal, sample_rate,nfft=1200,winlen=window,winstep=window)

    return mfcc_features

# Path to the WAV file
wav_file = '/home/hp/Documents/Speech-Analysis/Voxit_v2/Grandfather_passage_clean.wav'

# Extract MFCC features from the WAV file
mfcc_features = extract_mfcc(wav_file,20)
df = pd.DataFrame(mfcc_features)
# Print the extracted MFCC features
print(df)


def extract_filterbank_energies(wav_file, frame_size):
    # Open the WAV file
    with wave.open(wav_file, 'rb') as wav:
        # Get the audio data
        frames = wav.readframes(-1)
        signal = np.frombuffer(frames, dtype='int16')

        # Get the sample rate
        sample_rate = wav.getframerate()

    # Extract filterbank energies
    filterbank_features, _ = fbank(signal, samplerate=sample_rate, winlen=frame_size,winstep=frame_size)

    return filterbank_features

# Path to the WAV file


# Set the frame size in seconds (choose a valid frame size smaller than the audio duration)
frame_size = 20  # 20 milliseconds

# Extract filterbank energies from the WAV file with the specified frame size
filterbank_features = extract_filterbank_energies(wav_file, frame_size)

# Convert filterbank energies to DataFrame
df1 = pd.DataFrame(filterbank_features)

# Print the DataFrame
print(df1)



###############################################################################

from python_speech_features import ssc

def extract_ssc_features(wav_file, frame_size, frame_shift):
    # Open the WAV file
    with wave.open(wav_file, 'rb') as wav:
        # Get the audio data
        frames = wav.readframes(-1)
        signal = np.frombuffer(frames, dtype='int16')

        # Get the sample rate
        sample_rate = wav.getframerate()

    # Calculate frame length and frame shift in samples
    # frame_length = int(frame_size * sample_rate)
    # frame_shift = int(frame_shift * sample_rate)

    # Extract SSC features
    ssc_features = ssc(signal, samplerate=sample_rate, winlen=frame_size, winstep=frame_size)

    return ssc_features

# Path to the WAV file


# Set the frame size in seconds (e.g., 0.025 seconds or 25 milliseconds)
frame_size = 20

# Set the frame shift in seconds (e.g., 0.01 seconds or 10 milliseconds)
frame_shift = 20

# Extract SSC features from the WAV file with the specified frame size and frame shift
ssc_features = extract_ssc_features(wav_file, frame_size, frame_shift)

# Convert SSC features to DataFrame
df3 = pd.DataFrame(ssc_features)

# Print the DataFrame
print(df3)