#!/bin/bash

# Function to display help message
# 
usage() {
    echo "Usage: $0 <profile> <endpoint> <mount_point> <bucket>"
    echo
    echo "  <profile>        AWS profile name to use for authentication."
    echo "  <endpoint>       S3 endpoint URL."
    echo "  <mount_point>    Directory where the S3 bucket will be mounted."
    echo "  <bucket>         S3 bucket name."
    exit 1
}

# Check for the correct number of arguments
if [ "$#" -lt 4 ]; then
    usage
fi

# Assign command-line arguments to variables
PROFILE="$1"
ENDPOINT="$2"
MOUNT_POINT="$3"
BUCKET="$4"

# Ensure the mount point directory exists
if [ ! -d "$MOUNT_POINT" ]; then
    echo "Creating mount point directory $MOUNT_POINT..."
    mkdir -p "$MOUNT_POINT"
fi

# Check if goofys is installed
if command -v goofys >/dev/null 2>&1; then
    echo "goofys is already installed."
else
    echo "ERROR: goofys is not installed. Please install goofys before running this script."
    exit 1
fi

# Check if the mount point is already mounted
if mountpoint -q "$MOUNT_POINT"; then
    echo "$MOUNT_POINT is already mounted."
else
    echo "$MOUNT_POINT is not mounted. Mounting with goofys..."
    goofys -f --profile "$PROFILE" --file-mode=0700 --dir-mode=0700 --endpoint="$ENDPOINT" "$BUCKET" "$MOUNT_POINT"   
fi
