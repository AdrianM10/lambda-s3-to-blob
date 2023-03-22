import boto3
import botocore
import os
import tempfile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

s3 = boto3.resource('s3')

# Credentials for accessing Azure Blob Storage
storage_account_key = os.environ.get('storage_account_key')
storage_account_name = os.environ.get('storage_account_name')
connection_string = os.environ.get('connection_string')
container_name = os.environ.get('container_name')


def lambda_handler(event, context):
    # Get temp file location when running
    temFilePath = tempfile.gettempdir()

    # Change directory to /tmp folder
    os.chdir(temFilePath)

    for record in event['Records']:
        # Get bucket and key from s3 trigger event
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Get file name from key, join /tmp folder path and file name
        file_name = key
        upload_file_path = os.path.join(temFilePath, file_name)

        try:
            # Download the file from s3
            s3.meta.client.download_file(bucket, key, file_name)

            def upload_to_blob_storage(file_path, file_name):
                """Upload file to Azure storage as blob from /tmp folder"""
                blob_service_client = BlobServiceClient.from_connection_string(
                    connection_string)
                blob_client = blob_service_client.get_blob_client(
                    container=container_name, blob=file_name)

                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                    print(f" {file_name} uploaded to Azure Blob !")

            upload_to_blob_storage(upload_file_path, file_name)

        except FileNotFoundError:
            print(f"The file {key} does not exist")
        except botocore.exceptions.ClientError as error:
            print(
                f"Error : {error.response['Error']['Code']}, '{upload_file_path}' not found.")
