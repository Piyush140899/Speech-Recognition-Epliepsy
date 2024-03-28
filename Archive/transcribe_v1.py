import boto3
import time
import json
import urllib

# Set up AWS credentials and regions

print("--------------AWS TRANSCRIBE------------------------------")

AWS_ACCESS_KEY_ID = '#######################'
AWS_SECRET_ACCESS_KEY = '###################################'
AWS_REGION_NAME = 'us-west-1'
s3_client = boto3.client('s3')
# Set up S3 client and resource
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)

# Set up Transcribe client
transcribe_client = boto3.client('transcribe', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)

# Upload the .wav file to S3 bucket
BUCKET_NAME = 'speech-ucdavis-psk'
OBJECT_NAME = 'audio1.WAV'
LOCAL_FILE_PATH = r'C:\Users\HP\Documents\Speech\audio1.WAV'

s3.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, OBJECT_NAME)

# Create Transcribe job
TRANSCRIBE_JOB_NAME = 'job1_temp'
LANGUAGE_CODE = 'en-US'
MEDIA_FORMAT = 'wav'

transcribe_client.start_transcription_job(
    TranscriptionJobName=TRANSCRIBE_JOB_NAME,
    LanguageCode=LANGUAGE_CODE,
    MediaFormat=MEDIA_FORMAT,
    Media={
        'MediaFileUri': f's3://{BUCKET_NAME}/{OBJECT_NAME}'
    }
)

max_tries = 60
job_name='job1_temp'
while max_tries > 0:
    max_tries -= 1
    job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    job_status = job['TranscriptionJob']['TranscriptionJobStatus']
    if job_status in ['COMPLETED', 'FAILED']:
        print(f"Job {job_name} is {job_status}.")
        if job_status == 'COMPLETED':
            response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
            data = json.loads(response.read())
            text = data['results']['transcripts'][0]['transcript']
            print("========== below is output of speech-to-text ========================")
            print(text)
            print("=====================================================================")
        break
    else:
        print(f"Waiting for {job_name}. Current status is {job_status}.")
    time.sleep(10)