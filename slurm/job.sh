#!/bin/bash
#SBATCH --job-name=uuid
#SBATCH --time=1:00:00
#SBATCH --output=/home/river/.river/jobs/uuid/job.log
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
source /home/river/.river.sh

# host and port
echo $(python3 -c "import socket; s=socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()") > /home/river/.river/jobs/uuid/job.port
echo $(hostname) > /home/river/.river/jobs/uuid/job.host

# keep running for 10 seconds
sleep 1