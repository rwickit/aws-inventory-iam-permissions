import os
import boto3

# Set up a Boto3 client for STS and IAM
sts_client = boto3.client('sts')
iam_client = boto3.client('iam')

# Get the AWS account ID for the current session
account_id = sts_client.get_caller_identity()['Account']

# Create a directory in the working directory named with the account ID
directory_name = account_id
if not os.path.exists(directory_name):
    os.makedirs(directory_name)
    print(f"Created directory {directory_name} in the current working directory.")
else:
    print(f"Directory {directory_name} already exists in the current working directory.")

# Retrieve a list of all IAM roles in the account
roles = iam_client.list_roles()['Roles']

# Create a subdirectory for each IAM role in the top-level directory
for role in roles:
    role_name = role['RoleName']
    subdirectory_name = os.path.join(directory_name, role_name)
    if not os.path.exists(subdirectory_name):
        os.makedirs(subdirectory_name)
        print(f"Created directory {subdirectory_name} in the current working directory.")
    else:
        print(f"Directory {subdirectory_name} already exists in the current working directory.")
