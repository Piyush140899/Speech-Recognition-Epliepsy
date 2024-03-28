import math
import os
import wave
import librosa
import soundfile as sf
import numpy as np
import noisereduce as nr
from scipy.signal import resample
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.generators import WhiteNoise
import denoiser
import torch
import torchaudio
from denoiser import pretrained
from denoiser.dsp import convert_audio
import moviepy.editor as mp
import subprocess


"""

Toprani Lab Script

Voice-Speech Analysis

"""


def denoise_wav_librosa(input_file, output_file):
    """
    Denoise .wav files using librosa

    :param input_file: individual .wav file to denoise
    :param output_file: name of new file
    :return: denoised file
    """

    # check if input file is a valid WAV file
    # input_file, output_file = check_wav_file(input_file, output_file)

    # load the audio file
    signal, sample_rate = librosa.load(input_file, sr=44100)

    # use spectral subtraction to denoise the audio signal
    stft = librosa.stft(signal, n_fft=2048, hop_length=512)
    magnitude = np.abs(stft)
    power = magnitude ** 2
    noise_threshold = power.mean() * 0.5
    mask = power > noise_threshold
    stft_denoised = stft * mask
    signal_denoised = librosa.istft(stft_denoised, hop_length=512)

    # create a new wave file and write the denoised audio signal to it
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, len(signal_denoised), 'NONE', 'not compressed'))
        wav_file.writeframes(signal_denoised.tobytes())

    return output_file


def denoiser_fb(audio_file):
    """
    Denoise .wav files using fb denoiser

    :param audio_file: individual .wav file to denoise
    :return: denoised file _FBdenoised.wav extension, same path as input .wav file
    """

    # Check if the file extension is valid
    valid_extensions = ['.wav', '.WAV']
    file_extension = os.path.splitext(audio_file)[1]
    if file_extension not in valid_extensions:
        raise ValueError("Invalid file extension. Only WAV files are supported.")
    # Convert .WAV to .wav if necessary
    if file_extension.lower() == '.wav':
        audio_file = os.path.splitext(audio_file)[0] + '.wav'

    # loading model
    model = pretrained.master64()
    print("MODEL SAMPLE RATE", model.sample_rate)

    # loading audio file
    wav, sr = torchaudio.load(audio_file)
    # converting audio
    wav = convert_audio(wav, sr, model.sample_rate, model.chin)

    # denoising
    with torch.no_grad():
        denoised = model(wav[None])[0]

    # create a new wave file and write the denoised audio signal to it
    denoised_audio = audio_file.replace(".wav", "_FBdenoised.WAV")
    torchaudio.save(denoised_audio, denoised.data.cpu(), model.sample_rate)
    print(f"Successfully wrote denoised audio to {denoised_audio}")


def denoise_wav_noisereduce(input_file, output_file):
    """
    Denoise .wav files using noisereduce

    :param input_file: individual .wav file to denoise
    :param output_file: name of new file (.wav)
    :return: denoised file
    """

    # check if input file is a valid WAV file
    # input_file, output_file = check_wav_file(input_file, output_file)

    # load the audio file
    # with wave.open(input_file, 'rb') as wav_file:
    #     signal = np.frombuffer(wav_file.readframes(-1), dtype='int16')
    #     sample_rate = wav_file.getframerate()

    rate, signal = wavfile.read(input_file)
    orig_shape = signal.shape
    signal = np.reshape(signal, (2, -1))
    print(rate)

    # use noisereduce to denoise the audio signal
    signal_denoised = nr.reduce_noise(y=signal, sr=rate, stationary=True)

    # create a new wave file and write the denoised audio signal to it
    # wavfile.write(output_file, rate, signal_denoised.reshape(orig_shape))

    # try:
    #     with sf.SoundFile(output_file, 'w', samplerate=rate, channels=1, subtype='PCM_16') as file:
    #         file.write(signal_denoised)
    # except Exception as e:
    #     print(f"Failed to write audio to {output_file}: {e}")
    #     raise
    print(f"Successfully wrote denoised audio to {output_file}")

    return output_file


def add_noise_to_wav(original_file, SNR):
    # SNR in dB

    # Load the original audio file
    signal, sr = librosa.load(original_file)

    # RMS value of signal
    RMS_signal = math.sqrt(np.mean(signal**2))
    RMS_noise = math.sqrt(RMS_signal**2/(pow(10, SNR/10)))

    # generate noise from Gaussian distribution with mean = 0 and SD = RMS
    noise = np.random.normal(0, RMS_noise, signal.shape[0])

    # overlay
    signal_noise = signal + noise

    # Output the noisy audio to the same directory as the original file
    noisy_file = original_file.replace(".wav", "_noisy.wav")
    print(signal_noise)
    print("Length", np.array(signal_noise).shape)
    # sf.write(noisy_file, signal_noise, sr, 'PCM_24')


def mp4_to_wav(infile, outfile):
    input_file = AudioSegment.from_file(infile, format="mp4")
    input_file.export(outfile, format="wav")


def split_wav_file(input_file, segment_length):
    """
    Splits a WAV file into segments of specified length.

    :param input_file: (str) : Path the the input WAV file
    :param segment_length: (float): Length of each segment in seconds.
    :return: List[str]: List of paths to the output WAV files

    """

    # Load the input file
    with wave.open(input_file, 'rb') as wav:
        framerate = wav.getframerate()
        n_channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        n_frames = wav.getnframes()
        duration = n_frames / framerate

        # Calculate the number of segments needed
        n_segments = int(duration // segment_length) + 1

        # Create a directory to store the output files
        output_dir = os.path.splitext(input_file)[0] + '_segments'
        os.makedirs(output_dir, exist_ok=True)

        # Split the input file into segments
        output_files = []
        for i in range(n_segments):
            start_time = i * segment_length
            end_time = min((i + 1) * segment_length, duration)
            start_frame = int(start_time * framerate)
            end_frame = int(end_time * framerate)
            segment_frames = wav.readframes(end_frame - start_frame)

            # Create a new output file for this segment
            output_path = os.path.join(output_dir, f'{i}.wav')
            with wave.open(output_path, 'wb') as segment:
                segment.setframerate(framerate)
                segment.setnchannels(n_channels)
                segment.setsampwidth(sample_width)
                segment.writeframes(segment_frames)
            output_files.append(output_path)
        print('File split successfully')

    return output_files


def check_wav_file(input_file):
    """
    Check if input/output file is a valid WAV file

    :param input_file: path to .wav file

    # Must:
    #   - Input/Output contains '.wav' extension and exist
    #   - Have frame rate of < 41kHz

    """

    # input
    if not os.path.isfile(input_file):
        raise ValueError(f"Input file {input_file} does not exist!")
    signal, sample_rate = sf.read(input_file)
    if sample_rate != 48000:
        print(f"Warning: Input WAV file has a sample rate of {sample_rate} Hz...")
        if sample_rate >= 41000:
            raise ValueError("Sample rate is too low to continue")
