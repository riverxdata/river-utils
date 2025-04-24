# River CLI Tool

`river-utils` is a powerful Command-Line Interface (CLI) tool designed to simplify bioinformatics workflows, manage HPC jobs, and configure cloud storage. It provides commands for handling cloud configurations, job scripts, and setup utilities.

## Installation

### Prerequisites
- Python 3.8 or higher
- AWS credentials configured locally (for cloud-related commands)
- System utilities: `wget`, `curl`

### Development Version
To install the development version, follow these steps (for non-x64 architectures, refer to [micromamba installation guide](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)):

```bash
# Specify your desired installation directory for micromamba
git clone https://github.com/riverxdata/river-utils.git -b dev
cd river-utils
bash base.sh
make build
pip install -e .
```

### Latest Stable Version
To install the latest stable version, use the following command. This version includes additional software:

- **AWS CLI**: Interact with AWS or AWS-compatible services.
- **Singularity**: A container engine suitable for rootless environments.
- **R (4.4.0)**: An R environment for data analysis and AWS integration.
- **Python (3.9.21)**: A Python environment.
- **Zsh**: A shell with productivity-enhancing plugins.

**Note**: This setup installs micromamba, creates an environment named `river`, and installs the above tools without version restrictions.

```bash
version="v1.2.0"
bash <(curl -Ls https://raw.githubusercontent.com/riverxdata/river-utils/${version}/install/setup.sh) $HOME $version
source ~/.river.sh
```

## Usage

The `river-utils` CLI consists of three main subcommands:

### 1. `cloud`
Manage AWS S3 configurations and mount buckets using **Goofys**. Unlike the default AWS CLI, this tool supports specifying regions.

```bash
river cloud s3-config --profile-name PROFILE_NAME --region REGION --aws-access-key-id AWS_ACCESS_KEY_ID --aws-secret-access-key AWS_SECRET_ACCESS_KEY
```

### 2. `job`
Manage and generate job scripts for HPC systems and the River web server.

Subcommands:
- `create`: Generate a job script with an `sbatch` header for Slurm. The script is based on a cloned repository.
- `info`: Fetch and display job information for platform updates.

```bash
river job create --job-id JOB_ID
river job config --job-id JOB_ID
river job info JOB_UUIDS
```

### Environment Setup
To load micromamba and the `river` CLI tool, run the following command or add it to your `.bashrc`:

```bash
source ~/.river.sh
```

## License
This project is licensed under the MIT License.