# 🎙️ Text-to-Speech Converter with Amazon Polly & Lambda

This project is a serverless Text-to-Speech (TTS) system built using **AWS Lambda**, **Amazon Polly**, and **Amazon S3**. It takes a block of input text, converts it into speech using Polly, and stores the resulting MP3 in an S3 bucket. The MP3 file URL is then returned as output.

---

## 🚀 Features

- Converts any text to high-quality speech using Amazon Polly
- Saves MP3 output to Amazon S3
- Returns a sharable audio URL
- Supports custom voice selection
- Easily extensible via API Gateway for HTTP access

---

## 🧰 AWS Services Used

- **Lambda** – Serverless function to process text
- **Amazon Polly** – Converts text to speech
- **Amazon S3** – Stores resulting MP3 files
- **IAM** – Controls access permissions
- *(Optional)* **API Gateway** – Exposes function via HTTP

---

## 🛠️ Setup Instructions

### 1. Create an S3 Bucket

- Go to the [S3 Console](https://console.aws.amazon.com/s3/)
- Create a bucket named (e.g., `polly-audio-output`)
- Optional: Disable public access if security is required

---

### 2. Create a Lambda Function

- Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
- Create a function named `TextToSpeechLambda` using **Python 3.9**

Paste the following code into `lambda_function.py`:

```python
import boto3
import uuid
import os

polly = boto3.client('polly')
s3 = boto3.client('s3')
S3_BUCKET = os.environ['S3_BUCKET']  # Set this as an environment variable

def lambda_handler(event, context):
    text = event['text']
    voice_id = event.get('voice_id', 'Joanna')

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

