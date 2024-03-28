# Voxit_v2

Welcome to Speech Analysis , the pipline aim to achieve a feature extraction on a given wav file and outputs a dataframe containing features extracted from various packages. Here is overview of all the modules and pipelines

1. **process_wav_files.py** - This facebook denoiser first denoises the input .wav file and downsamples the audio to 16 KHz

2. **transcribe_v1.py** - This code first uploads the denoised wav file to s3 bucket. You need AWS credntials to do so. Please create a username , password or get one from Dr Miller or Dr Stavisky. After that you will need a AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION_NAME and an s3 bucket location. It then creates a aws transcribe job for you and outputs and saves .json file which basically is the transcription , the word timings, the speaker labels for each word.

3. **diarization.py** - This code uses the json and identifies when the speaker of interest spoke and clips the audio accordingly and creates a clipped audio.

4. **generate_transcript.py** - This code generates a .text file that is required for the MFA

5. **MFA** - Not a code but after we have the clipped audio and clipped transcript we will feed that to the Montreal Forced Aligner . Please look at MFA.text for more information on how to run mfa align command so as to get the output .textgrid file that we will use for further analysis and feature extraction.

6. **pyvoxit.py** - We use the .textgrid file as input and find the 16 voxit feature which internally calculate pitch using the pyworld.harvest() method and uses the word timings of .textgrid file.

7. **opensmile_v1.py** - We run opensmile.py on the updated .wav file to find the 85 features 

8. **speech features.py** - We run speechfeatures.py to find additional 64 features ( MFCC's, filterbank energies,Spectral Subband Centroids) .

9. **sentiment.py** - This code contains functions that calculate sentiments every 1 minute and applies the same data for all the 3 rows that signify 20 second window. The sentiments are calculates using the NRC Word-Emotion Association Lexicon . Following are the sentiments/emotions captured= ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']

