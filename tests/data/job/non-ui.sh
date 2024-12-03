#!/bin/bash
#SBATCH --job-name=uuid
#SBATCH --time=1:00:00
#SBATCH --output=./.river/jobs/uuid/job.log
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
source ~/.river.sh
# Symlink analysis
ln -sf ./.river/tools/code_server ./.river/jobs/uuid/code_server
# Boostrap:


# Cloud storage
cleanup() {
    s3_umount.sh ./.river/jobs/uuid/workspace
}
error_handler() {
    local exit_code=$?
    cleanup
    exit $exit_code
}

trap 'error_handler' EXIT
set -euo pipefail
s3_cloud.sh bucket_name endpoint ./.river/jobs/uuid/workspace bucket_name
openvscode-server --host 0.0.0.0 --port $PORT --server-base-path uuid --without-connection-token
