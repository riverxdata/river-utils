#!/bin/bash
set -e
set -o pipefail

# Set config directory
RIVER_HOME=${1:-$HOME}
echo "RIVER_HOME is set to: $RIVER_HOME"
RIVER_VERSION=${2:-v1.0.3}
echo "River CLI tools version v1.0.3 is used by default"
MICROMAMBA_VERSION=2.0.5
RIVER_BIN=$RIVER_HOME/.river/bin
mkdir -p $RIVER_BIN

# Install micromamba
export RIVER_HOME=$HOME
export MICROMAMBA_EXECUTE=$RIVER_HOME/.river/tools/micromamba/$MICROMAMBA_VERSION
mkdir -p $MICROMAMBA_EXECUTE

if [ ! -f "$RIVER_BIN/micromamba"  ]; then
    echo "Installing micromamba..."
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/$MICROMAMBA_VERSION | tar -xvj bin/micromamba
    mv bin/micromamba $RIVER_BIN/micromamba
    rm -rf bin
else
    echo "micromamba already exists"
    micromamba --help
fi


# Start up
export PATH="$RIVER_HOME/.river/bin:$PATH"
export MAMBA_ROOT_PREFIX="$RIVER_HOME/.river/images/micromamba"

# Create micromamba environment and install river-utils
micromamba create -n river anaconda::python conda-forge::singularity=3.8.6 bioconda::nextflow  -y
micromamba run -n river pip install git+https://github.com/giangbioinformatics/river-utils.git@${RIVER_VERSION}


# Create .river.sh for environment variables
cat <<EOF > $RIVER_HOME/.river.sh
export RIVER_HOME=${RIVER_HOME}
export RIVER_HOME_TOOLS=\${RIVER_HOME}/.river/bin
export MAMBA_ROOT_PREFIX=\${RIVER_HOME}/.river/images/micromamba
export SINGULARITY_CACHE_DIR=\${RIVER_HOME}/.river/images/singularities
export NXF_SINGULARITY_CACHEDIR=\$SINGULARITY_CACHE_DIR/images
export PATH=\${RIVER_HOME_TOOLS}:\$PATH
eval "\$(micromamba shell hook -s posix)"
micromamba activate -n river
EOF

source $RIVER_HOME/.river.sh
river setup install