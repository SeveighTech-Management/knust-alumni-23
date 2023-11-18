from boto3 import resource, client
from botocore.client import Config
from boto3.session import Session
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME=os.environ.get('AWS_BUCKET')

s3 = client('s3', aws_access_key_id=os.environ.get('BUCKET_ACCESS_KEY_ID'),
                    aws_secret_access_key= os.environ.get('BUCKET_SECRET_ACCESS_KEY')
                     )

my_config = Config(
    region_name = os.environ.get('AWS_BUCKET_REGION_NAME'),
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

def s3_client():
    session = Session()
    client = session.client('s3', aws_access_key_id=os.environ.get('BUCKET_ACCESS_KEY_ID'), aws_secret_access_key= os.environ.get('BUCKET_SECRET_ACCESS_KEY'), config=my_config)
    return client

def send_files(filename, file_key, file_type):
    client = s3_client()
    upload_file_response = client.put_object(Body=filename,
                                             Bucket=BUCKET_NAME,
                                             Key=file_key,
                                             ContentType=file_type)
    return upload_file_response

def get_files(folder):
    client = s3_client()
    s3 = resource('s3', aws_access_key_id=os.environ.get('BUCKET_ACCESS_KEY_ID'), aws_secret_access_key= os.environ.get('BUCKET_SECRET_ACCESS_KEY'))
    my_bucket = s3.Bucket(BUCKET_NAME)
    url = ""
    try:
        for item in my_bucket.objects.filter(Delimiter='/', Prefix=folder):
            presigned_url = client.generate_presigned_url('get_object', Params = {'Bucket': BUCKET_NAME, 'Key': item.key}, ExpiresIn = 3600)
            url = presigned_url
    except Exception as e:
        return e

    return url



