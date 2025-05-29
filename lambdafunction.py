import boto3
import uuid

polly = boto3.client('polly')
s3 = boto3.client('s3')

S3_BUCKET = 'awspollys3bybadarqa'  # Change if your bucket is named differently

def lambda_handler(event, context):
    text = event['text']
    voice_id = event.get('voice_id', 'Joanna')  # Optional voice selection

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id
    )

    audio_key = f"{uuid.uuid4()}.mp3"
    s3.put_object(Bucket=S3_BUCKET, Key=audio_key, Body=response['AudioStream'].read())

    return {
        'statusCode': 200,
        'audio_url': f"https://{S3_BUCKET}.s3.amazonaws.com/{audio_key}"
    }

