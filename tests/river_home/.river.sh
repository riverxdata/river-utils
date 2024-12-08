
export RIVER_HOME="./tests/river_home"
export RIVER_HOME_TOOLS=${RIVER_HOME}/.river/tools
export MAMBA_ROOT_PREFIX=${RIVER_HOME}/.river/.images/micromamba
export SINGULARITY_CACHE_DIR=${RIVER_HOME}/.river/.images/singularities
export NXF_SINGULARITY_CACHEDIR=$SINGULARITY_CACHE_DIR
export PATH=${RIVER_HOME_TOOLS}:${RIVER_HOME_TOOLS}/openvscode-server-v1.93.1-linux-x64/bin:$/home/giangnguyen/Documents/dev/river-utils/env/bin:$PATH
eval "$(micromamba shell hook -s posix)"
micromamba activate -n river
