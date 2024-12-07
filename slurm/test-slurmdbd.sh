#!/bin/bash
/etc/init.d/munge start
service mysql start
/usr/sbin/sshd
service slurmdbd restart
service slurmctld restart
service slurmd restart
sleep 5
sacctmgr -i add cluster localcluster
sleep 5
sbatch --wrap="sleep 3"
sleep 5 

su river
# test river job info
source /home/river/.river.sh
sbatch --parsable /home/river/.river/jobs/uuid/job.sh > /home/river/.river/jobs/uuid/job.id
sleep 1

output=$(river job info uuid)

uuid_job_id=$(echo "$output" | jq -r '.uuid_job_id')
slurm_job_id=$(echo "$output" | jq -r '.slurm_job_id')
status=$(echo "$output" | jq -r '.status')
host=$(echo "$output" | jq -r '.host')
port=$(echo "$output" | jq -r '.port')
url=$(echo "$output" | jq -r '.url')
running_time=$(echo "$output" | jq -r '.running_time')

if [[ -z "$uuid_job_id" ]]; then
    echo "Test failed: Job ID is empty."
    exit 1
fi

if [[ -z "$slurm_job_id" ]]; then
    echo "Test failed: Slurm Job ID is empty."
    exit 1
fi

if [[ -z "$host" ]]; then
    echo "Test failed: Host is empty."
    exit 1
fi

if [[ -z "$status" || "$status" != "COMPLETED" ]]; then
    echo "Test failed: Job status is not COMPLETED. Actual status: $status"
    exit 1
fi

if [[ -z "$port" || ! "$port" =~ ^[0-9]+$ ]]; then
    echo "Test failed: Port is either empty or not a valid number. Actual port: $port"
    exit 1
fi

if [[ -z "$running_time" ]]; then
    echo "Test failed: Running time is empty."
    exit 1
fi

echo "Test passed: Output matches expected values."
