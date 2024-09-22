#!/bin/bash

# Function to display help message
usage() {
    echo "Usage: $0 <profile_name> <region> <aws_access_key_id> <aws_secret_access_key>"
    echo
    echo "  <profile_name>         AWS profile name to be added."
    echo "  <region>               AWS region (e.g., us-west-2)."
    echo "  <aws_access_key_id>    Your AWS access key ID."
    echo "  <aws_secret_access_key> Your AWS secret access key."
    exit 1
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    usage
fi

# Assign command-line arguments to variables
PROFILE_NAME="$1"
REGION="$2"
ACCESS_KEY_ID="$3"
SECRET_ACCESS_KEY="$4"

AWS_CONFIG_FILE="$HOME/.aws/config"

# Ensure the AWS config directory exists
mkdir -p "$HOME/.aws"

# Check if the profile already exists in the config file
if grep -q "\[$PROFILE_NAME\]" "$AWS_CONFIG_FILE"; then
    echo "Profile '$PROFILE_NAME' already exists in $AWS_CONFIG_FILE."
    exit 0
else
    echo "Adding profile '$PROFILE_NAME' to AWS config..."
    # Append the profile configuration to the config file
    cat <<EOF >> "$AWS_CONFIG_FILE"
[$PROFILE_NAME]
region = $REGION
aws_access_key_id = $ACCESS_KEY_ID
aws_secret_access_key = $SECRET_ACCESS_KEY
EOF
    echo "Profile '$PROFILE_NAME' successfully added to $AWS_CONFIG_FILE."
fi
