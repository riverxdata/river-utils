#!/bin/bash

# Start necessary services
/etc/init.d/munge start
service mysql start
/usr/sbin/sshd
service slurmdbd restart
service slurmctld restart
service slurmd restart

# Wait for services to stabilize
sleep 5

# Add a local cluster to SlurmDBD
sacctmgr -i add cluster localcluster

# Wait for the changes to take effect
sleep 5

# Submit a simple test job
sbatch --wrap="sleep 3"
sleep 5
lines=$(sacct --jobs=2 | wc -l)

# if [ "$lines" -eq 2 ]; then
#     echo "Fail slurmdbd"
#     exit 1
# fi

# echo "SlurmDBD is functioning correctly"
