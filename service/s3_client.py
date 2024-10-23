import boto3

from config import settings

BUCKET = settings['SELECTEL']['BUCKET']

s3_client = boto3.client(service_name=settings['SELECTEL']['SERVICE_NAME'],
                         endpoint_url=settings['SELECTEL']['ENDPOINT_URL'],
                         # signature_version='s3v4',
                         verify=False
                         )
