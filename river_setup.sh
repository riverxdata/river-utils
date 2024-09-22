#!/bin/bash

# Function to display help message
usage() {
    echo "Usage: $0 <RIVER_HOME> "
    echo "  <RIVER_HOME>  Directory where the river server tools will be installed."
    exit 1
}

# Check for the correct number of arguments
if [ "$#" -lt 1 ]; then
    usage
fi
RIVER_HOME="$1"
RIVER_HOME_TOOLS=${RIVER_HOME}/.river/tools
# tools version
openvscode_server_version="1.93.1"
goofys_version="0.24.0"
mkdir -p ${RIVER_HOME_TOOLS}
# install code-server
wget https://github.com/gitpod-io/openvscode-server/releases/download/openvscode-server-v${openvscode_server_version}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz \
    -O ${RIVER_HOME_TOOLS}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz

tar -xzf ${RIVER_HOME_TOOLS}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz -C ${RIVER_HOME}
rm ${RIVER_HOME_TOOLS}/openvscode-server-v${openvscode_server_version}-linux-x64.tar.gz

# install goofys
wget https://github.com/kahing/goofys/releases/download/v${goofys_version}/goofys -O ${RIVER_HOME_TOOLS}/goofys
chmod +x ${RIVER_HOME_TOOLS}/goofys

# install river utilities
cp -r ./utilities ${RIVER_HOME_TOOLS}/utilities
chmod 700 ${RIVER_HOME_TOOLS}/utilities/*

# add tools to PATH
echo "Create .river.sh for river utilities export"
cat <<EOF >> "$RIVER_HOME/.river.sh"
export SINGULARITY_CACHE_DIR=${RIVER_HOME}/.images/singularities
export PATH=\$PATH:${RIVER_HOME_TOOLS}/utilities:${RIVER_HOME_TOOLS}
export RIVER_HOME=${RIVER_HOME}
EOF

# add river to source .bashrc
echo "Adding river to .bashrc"
echo "source $RIVER_HOME/.river.sh" >> ~/.bashrc