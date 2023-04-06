import os
import boto3

# Set up a Boto3 client for STS
sts_client = boto3.client('sts')

# Get the AWS account ID for the current session
account_id = sts_client.get_caller_identity()['Account']

# Create a directory in the working directory named with the account ID
directory_name = account_id
if not os.path.exists(directory_name):
    os.makedirs(directory_name)
    print(f"Created directory {directory_name} in the current working directory.")
else:
    print(f"Directory {directory_name} already exists in the current working directory.")
