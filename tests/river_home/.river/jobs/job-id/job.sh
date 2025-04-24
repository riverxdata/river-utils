#!/bin/bash
#SBATCH --job-name=job-id
#SBATCH --time=1:00:00
#SBATCH --output=./tests/river_home/.river/jobs/job-id/job.log
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
source ~/.river.sh

# Working directory
cd ./tests/river_home/.river/jobs/job-id

# Loading config to be exported bash variable
while IFS== read key value; do
    printf -v "$key" "$value"
done < <(jq -r 'to_entries|map("\(.key)=\(.value|tostring)")|.[]' config.json)

# Repo
repo_name=$(basename -s .git "$git")
owner=$(basename "$(dirname "$git")")
local_dir="$RIVER_HOME/.river/tools/$owner/$repo_name/$tag"

# Clone
# nf-core
if [ $owner = "nf-core" ]; then
    echo "The tool is nf-core owner, handle clone by nextlow"
# non nf-core
else
    if [ ! -d "$local_dir" ]; then
        echo "Starting to clone $git to $local_dir"
        git clone --branch "$tag" --single-branch "$git" "$local_dir"
    else
        echo "Tool already exists"
    fi
    # Symlink analysis
    ln -sf $local_dir $RIVER_HOME/.river/jobs/$uuid_job_id/analysis
fi

# Cloud storage
trap 'umount $mount_point || "S3 bucket is not mounted"' EXIT
set -euo pipefail

# Mount using goofys
mount_point=$RIVER_HOME/.river/jobs/$uuid_job_id/workspace
mkdir -p $mount_point
goofys --profile $bucket_name --file-mode=0700 --dir-mode=0700 --endpoint=$endpoint $bucket_name $mount_point

# Main
if [ $owner = "nf-core" ]; then
    river job config --job-id $uuid_job_id
    local_outdir=river_result
    nextflow run $owner/$repo_name -r $tag -c river.config -profile singularity --outdir $local_outdir
    # tarball folder and upload
    tar -czvf ${local_outdir}.tar.gz $local_outdir
    mkdir -p $outdir
    cp ${local_outdir}.tar.gz $outdir
else
    bash analysis/river/main.sh
fi