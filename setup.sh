#!/bin/bash
RIVER_HOME="$HOME"
if [ -f "$RIVER_HOME/.river.sh" ]; then
    source "$RIVER_HOME/.river.sh"
    echo "River utilities already installed."
fi

RIVER_HOME_TOOLS=${RIVER_HOME}/.river/tools
# tools version
openvscode_server_version="1.93.1"
goofys_version="0.24.0"
mkdir -p ${RIVER_HOME_TOOLS}
# install code-server
wget https://github.com/gitpod-io/openvscode-server/releases/download/openvscode-server-v${openvscode_server_version}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz \
    -O ${RIVER_HOME_TOOLS}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz

tar -xzf ${RIVER_HOME_TOOLS}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz -C ${RIVER_HOME_TOOLS}
rm ${RIVER_HOME_TOOLS}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz

# install goofys
wget https://github.com/kahing/goofys/releases/download/v${goofys_version}/goofys -O ./utilities/goofys

# install micromamba
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C $RIVER_HOME_TOOLS bin/micromamba
mv $RIVER_HOME_TOOLS/bin $RIVER_HOME_TOOLS/micromamba

# install singularity by micromamba and nextflow
$RIVER_HOME_TOOLS/micromamba/micromamba create -p ${RIVER_HOME}/images/micromamba/river conda-forge::singularity bioconda::nextflow -y

# install river utilities
cp -r ./utilities ${RIVER_HOME_TOOLS}/utilities
chmod 700 ${RIVER_HOME_TOOLS}/utilities/*

# add tools to PATH
echo "Create .river.sh for river utilities export"
cat <<EOF >> "$RIVER_HOME/.river.sh"
export RIVER_HOME=${RIVER_HOME}
export RIVER_HOME_TOOLS=\${RIVER_HOME}/.river/tools
export MAMBA_ROOT_PREFIX=\${RIVER_HOME}/.images/micromamba
export SINGULARITY_CACHE_DIR=\${RIVER_HOME}/.images/singularities
export PATH=\${RIVER_HOME_TOOLS}/utilities:\${RIVER_HOME_TOOLS}:\${RIVER_HOME_TOOLS}/openvscode-server-v${openvscode_server_version}-linux-x64/bin:\${RIVER_HOME_TOOLS}/micromamba:\$PATH
eval "\$(micromamba shell hook -s posix)"
micromamba activate -p ${RIVER_HOME}/images/micromamba/river
EOF