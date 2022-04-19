import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)
s3 = session.resource('s3', endpoint_url='https://s3mts.ru')
s3.meta.client.upload_file(Filename='call_history.csv', Bucket='test', Key='call_history.csv')
