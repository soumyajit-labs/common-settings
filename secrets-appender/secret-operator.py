import boto3
import os
import sys
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

region = os.environ['AWS_REGION']
repository = sys.argv[1]

def fetch(key):
    session = boto3.session.Session()
    client = session.client( service_name='secretsmanager', region_name=region )
    try:
        get_secret_value_response = client.get_secret_value( SecretId=key )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return 401
        else:
            return 400

    secret = get_secret_value_response['SecretString']
    return secret

secret = fetch(repository)

def create_file(env, secret):
    file_path = 'src/main/resources/{0}-secured-properties.yaml'.format(env)
    with open(file_path, 'w') as file:
            file.write(secret)

create_file(secret)
