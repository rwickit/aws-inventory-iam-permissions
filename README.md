# AWS IAM Role/Policy Inventory

The script provided in this repository is used to export a copy of every IAM Permissions Policy attached to every IAM role in a desired account.

## Script Configuration

The script [export-account-permissions.py](/export-account-permissions.py) can be run locally or from within an AWS Account.

1. Authenticate to the desired account with credentials locally via AWS IAM User or Identity Center and run the script locally.
2. Upload the script into AWS CloudShell and run the script from CloudShell using the console permissions you have.

### Advanced configuration

If desired, the script may updated and configured as a Lambda to run on a schedule to backup all policies to an S3 Bucket with Versioning enabled.

This will create a low-cost periodic backup of all permissions in your account for future reference.

## Output

The final output of the script is a directory structure where each Policy attached to an IAM Role is exported.

The directory structure is as follows:

- A directory in the `current working directory` is created using the current AWS Account ID as the folder name.
- Each role in the account gets a folder created in the account directory using the role name as the directory name.
- Each attached `managed` and `inline` policy documented are exported and saved in the respective role directory and prefixed with policy `type_`.

The final output provides a full copy of all permissions attached to each role within an account in a JSON policy document file.

## Script Creation

This script was complied by using ChatGPT 3.5

After about 20 minutes of testing prompts the process was to:

- Request a script to just create a folder from the account ID
- Update the script to add a sub-directory for each IAM Role
- Add the export of every managed and inline policy and save in JSON format to the respective role directory.

At this point the script worked except for the `inline` policies.
I have modified the logic to properly export inline policies as well as managed policies (AWS Managed and Customer Managed)

See the prompts here: [GPT Script Prompts](/artifacts/gpt-prompts.png)

See example output here: [Example Output](/artifacts/script-output.png)

See incrementally created scripts here: [Incremental Scripts](/python/)
