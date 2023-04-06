import os
import json
import boto3

def main():
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

    # Process each role
    for role in roles:
        role_name = role['RoleName']
        subdirectory_name = os.path.join(directory_name, role_name)
        if not os.path.exists(subdirectory_name):
            os.makedirs(subdirectory_name)
            print(f"Created directory {subdirectory_name} in the current working directory.")
        else:
            print(f"Directory {subdirectory_name} already exists in the current working directory.")

        # Process each inline policy attached to the role
        inline_policy_names = iam_client.list_role_policies(RoleName=role_name)['PolicyNames']
        for inline_policy_name in inline_policy_names:
            inline_policy_document = iam_client.get_role_policy(RoleName=role_name, PolicyName=inline_policy_name)['PolicyDocument']
            policy_type = "inline"
            policy_filename = f"{policy_type}_{inline_policy_name}.json"
            with open(os.path.join(subdirectory_name, policy_filename), 'w') as f:
                json.dump(inline_policy_document, f, indent=4)
            print(f"Created {policy_filename} in directory {subdirectory_name}.")

        # Process each managed policy attached to the role
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        for policy in attached_policies:
            policy_arn = policy['PolicyArn']
            policy_name = policy_arn.split('/')[-1]
            policy_type = "managed"
            policy_filename = f"{policy_type}_{policy_name}.json"
            policy_version = iam_client.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
            policy_doc = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document']
            with open(os.path.join(subdirectory_name, policy_filename), 'w') as f:
                json.dump(policy_doc, f, indent=4)
            print(f"Created {policy_filename} in directory {subdirectory_name}.")

if __name__ == '__main__':
    main()
