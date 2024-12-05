#!/bin/bash
#SBATCH --job-name=uuid
#SBATCH --time=1:00:00
#SBATCH --output=./.river/jobs/uuid/job.log
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
source ~/.river.sh
# Symlink analysis
ln -sf ./.river/tools/code_server ./.river/jobs/uuid/code_server

# Boostrap
# No boostrap script


# Access job
echo $(python3 -c "import socket; s=socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()") > ./.river/jobs/uuid/job.port
echo $(hostname) > ./.river/jobs/uuid/job.host

# Cloud storage
trap 'umount $MOUNT_POINT || "S3 bucket is not mounted' EXIT
set -euo pipefail

# Mount using goofys
MOUNT_POINT=./.river/jobs/uuid/workspace 
goofys --profile bucket_name --file-mode=0700 --dir-mode=0700 bucket_name $MOUNT_POINT

# Main
openvscode-server --host 0.0.0.0 --port $PORT --server-base-path <<uuid_job_id>> --without-connection-token
