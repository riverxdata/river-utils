#!/bin/bash
#SBATCH --job-name=uuid
#SBATCH --time=1:00:00
#SBATCH --output=./src/tests/river_home/.river/jobs/uuid/job.log
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
source ~/.river.sh

# Boostrap
echo uuid > ./src/tests/river_home/.river/jobs/uuid/job.url

# Symlink analysis
ln -sf ./src/tests/river_home/.river/tools/<<analysis>> ./src/tests/river_home/.river/jobs/uuid/<<analysis>>

# Access job
echo $(python3 -c "import socket; s=socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()") > ./src/tests/river_home/.river/jobs/uuid/job.port
echo $(hostname) > ./src/tests/river_home/.river/jobs/uuid/job.host


# Cloud storage
trap 'umount $MOUNT_POINT || "S3 bucket is not mounted"' EXIT
set -euo pipefail

# Mount using goofys
MOUNT_POINT=./src/tests/river_home/.river/jobs/uuid/workspace 
mkdir -p $MOUNT_POINT
goofys --profile bucket_name --file-mode=0700 --dir-mode=0700 --endpoint=endpoint bucket_name $MOUNT_POINT

# Main
openvscode-server --host 0.0.0.0 --port $PORT --server-base-path <<uuid_job_id>> --without-connection-token
