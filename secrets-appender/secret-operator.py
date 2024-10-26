import boto3
import os
import sys
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

region = sys.argv[1]
repository = sys.argv[2]
env = sys.argv[3]

print('Region is set to {0} and the environment is set to {1}...'.format(region, env))

def fetch(key):
    print('Trying to fetch the credentials for {0} repository...'.format(repository))
    session = boto3.session.Session()
    client = session.client( service_name='secretsmanager', region_name=region )
    try:
        get_secret_value_response = client.get_secret_value( SecretId=key )
    except ClientError as e:
        print('Something went wrong while fetching the credentials for {0} repository...'.format(repository))
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return 401
        else:
            return 400

    print('Fetched the credentials for {0} repository successfully!'.format(repository))
    return get_secret_value_response['SecretString']

def create_file(secret):
    file_path = 'src/main/resources/{0}-secured-properties.yaml'.format(env)
    try:
        with open(file_path, 'w') as file:
            file.write(secret)
            print('File written successfully!')
    except:
        print('Oh no! Something snapped!')

create_file(fetch(repository))
