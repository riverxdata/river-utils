#!/bin/bash

# Function to display help message
usage() {
    echo "Usage: $0 <mount_point>"
    echo
    echo "  <mount_point>  Directory that is currently mounted and needs to be unmounted."
    exit 1
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    usage
fi

# Assign command-line arguments to variables
MOUNT_POINT="$1"

# Check if the mount point is currently mounted
if mountpoint -q "$MOUNT_POINT"; then
    echo "$MOUNT_POINT is mounted. Unmounting..."
    # Unmount the mount point
    umount "$MOUNT_POINT"
    
    # Check if the unmount was successful
    if [ $? -eq 0 ]; then
        echo "$MOUNT_POINT has been successfully unmounted."
    else
        echo "Error: Failed to unmount $MOUNT_POINT."
        exit 1
    fi
else
    echo "$MOUNT_POINT is not mounted."
fi
