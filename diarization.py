import json

# Specify the path to your JSON file
json_file_path = '/home/hp/Documents/Speech-Analysis/Voxit_v2/sample_aws_op.json'

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract the start and end times when the speaker label is 's0'
start_end_times = []
for label in data['results']['speaker_labels'][0]['segments']:
    
    if label['speaker_label'] == 'spk_1':
        start_time = float(label['start_time'])
        end_time = float(label['end_time'])
        start_end_times.append((start_time, end_time))

print(start_end_times)

######################################################################################
######################################################################################

from pydub import AudioSegment

# Function to clip and concatenate audio segments
def clip_and_concatenate_audio(audio_file, start_end_times, output_file):
    # Load the original audio file
    audio = AudioSegment.from_wav(audio_file)

    # Initialize an empty list to store the clipped segments
    clipped_segments = []

    # Iterate over the start and end times
    for start_time, end_time in start_end_times:
        # Clip the audio segment based on start and end times
        clipped_segment = audio[start_time * 1000:end_time * 1000]
        # Append the clipped segment to the list
        clipped_segments.append(clipped_segment)

    # Concatenate the clipped segments
    concatenated_audio = sum(clipped_segments)

    # Export the concatenated audio as a new WAV file
    concatenated_audio.export(output_file, format='wav')

# Example usage
audio_file = '/home/hp/Documents/Speech-Analysis/Voxit_v2/audio1_1.WAV'
  # List of start and end times in seconds
output_file = '/home/hp/Documents/Speech-Analysis/Voxit_v2/diarized.wav'

clip_and_concatenate_audio(audio_file, start_end_times, output_file)
