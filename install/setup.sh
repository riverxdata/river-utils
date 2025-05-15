#!/bin/bash
set -e
set -o pipefail

# Set config directory
RIVER_HOME=${1:-$HOME}
RIVER_VERSION=${2:-dev}
echo "RIVER_HOME is set to: $RIVER_HOME"
echo "River software dependencies setup"
MICROMAMBA_VERSION=2.0.5
GOOFYS_VERSION=0.24.0
RIVER_BIN=$RIVER_HOME/.river/bin
mkdir -p $RIVER_BIN

# Base softwares
# micromamba
export RIVER_HOME=$HOME
export MICROMAMBA_EXECUTE=$RIVER_HOME/.river/bin
export PATH=$RIVER_HOME/.river/bin:$PATH
mkdir -p $MICROMAMBA_EXECUTE


if [ ! -f "$RIVER_BIN/micromamba"  ]; then
    echo "Installing micromamba..."
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/$MICROMAMBA_VERSION | tar -xvj bin/micromamba
    mv bin/micromamba $RIVER_BIN/micromamba
    rm -rf bin
else
    echo "micromamba already exists at: $RIVER_HOME/.river/bin"
fi

# goofys
if [ ! -f "$RIVER_BIN/goofys"  ]; then
    echo "Installing goofys..."
    curl -L https://github.com/kahing/goofys/releases/download/v${GOOFYS_VERSION}/goofys -o $RIVER_BIN/goofys
    chmod +x $RIVER_BIN/goofys
else
    echo "Goofys already exists at: $RIVER_HOME/.river/bin"
    goofys --help 2> /dev/null
fi



# Start up
export PATH="$RIVER_HOME/.river/bin:$PATH"
export MAMBA_ROOT_PREFIX="$RIVER_HOME/.river/images/micromamba"

# Create micromamba environment and install river-utils
micromamba create -n river \
    anaconda::python \
    conda-forge::r-base \
    conda-forge::singularity=3.8.6 \
    bioconda::nextflow \
    conda-forge::zsh \
    conda-forge::awscli \
    -y

eval "$(micromamba shell hook --shell bash)"
micromamba activate river

pip install git+https://github.com/riverxdata/river-utils.git@${RIVER_VERSION}

# zsh setup
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# plugins
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Update .zshrc
echo "Updating .zshrc..."
sed -i "s|plugins=(git)|plugins=(\n    git\n    docker\n    docker-compose\n    history\n    rsync\n    safe-paste\n    zsh-autosuggestions\n    zsh-syntax-highlighting\n)\n|" ~/.zshrc

# Create the singularity dir
mkdir -p $RIVER_HOME/.river/images/singularities/images

# Create .river.sh for environment variables
cat <<EOF > $RIVER_HOME/.river.sh
export RIVER_HOME=${RIVER_HOME}
export RIVER_HOME_TOOLS=\${RIVER_HOME}/.river/bin
export MAMBA_ROOT_PREFIX=\${RIVER_HOME}/.river/images/micromamba
export SINGULARITY_CACHE_DIR=\${RIVER_HOME}/.river/images/singularities
export NXF_SINGULARITY_CACHEDIR=\$SINGULARITY_CACHE_DIR/images
export NXF_WORK=\${RIVER_HOME}/.river/nextflow/work
export PATH=\${RIVER_HOME_TOOLS}:\$PATH
eval "\$(micromamba shell hook -s posix)"
micromamba activate -n river
zsh 
source ~/.zshrc
EOF