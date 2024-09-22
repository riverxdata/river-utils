#!/bin/bash
RIVER_HOME="$HOME"
if [-f "$RIVER_HOME/.river.sh"]; then
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