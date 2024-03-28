def generate_transcript_file(json_file_path,op_filename):
    import json

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    transcription = data['results']['transcripts'][0]['transcript']

    print(transcription)


generate_transcript_file('/home/hp/Documents/Speech-Analysis/Voxit_v2/sample_aws_op.json',"aa")