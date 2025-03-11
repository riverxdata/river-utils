# River CLI Tool

nf-utils is a versatile Command-Line Interface (CLI) tool designed to streamline bioinformatics workflows, HPC job management, and cloud storage setup. This tool provides commands to manage cloud configurations, job scripts, and setup utilities.

## Installation

### Prerequisites
- Python 3.8 or higher
- AWS credentials configured locally (for cloud commands)
- Required system utilities: wget, curl

### Development Version
To install the development version, use the following commands for x64, for another CPU architect, follow [here](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html):
```bash
# adjust where you want to install micromamba
<<<<<<< HEAD


git clone https://github.com/riverxdata/river-utils.git -b dev
=======
git clone https://github.com/giangbioinformatics/river-utils.git -b dev
>>>>>>> 1c496bd (rm newline)
cd river-utils 
bash base.sh
make build
pip install -e .
```

### Latest Version
To install the latest stable version, use the following command, beside the python package, it offers a few cool softwares:
+ aws: the aws client to interact with AWS services or AWS compatible services
+ singularity: the container engine that is best suit for root-less environments
+ r-base (4.4.0): the R environment where you can play around with AWS
+ python (3.9.21): The Python environment
+ zsh: The shell with plugins help to boost your performace when work with unix

**Note**: It will install the micromamba, create environment call river, install the above software but not restrict the versions
```bash
version="add_awscli_zsh"
bash <(curl -Ls https://raw.githubusercontent.com/riverxdata/river-utils/${version}/install/setup.sh) $HOME $version
source ~/.river.sh
```

## Usage
Overview
The nf-utils CLI consists of three main subcommands:

+ `cloud`: Manage AWS S3 configurations and mount buckets using **Goofys**. The current aws cli does not support region
+ `job`: Manage and generate job scripts for HPC systems and River web server.
+ `setup`: Set up standard tools for bioinformatics analysis.

### 1.`cloud`
The cloud command is used to configure and manage S3 buckets with Goofys.

Subcommands:
+ s3-config: Add a new AWS profile to your local configuration.
```bash
cloud s3-config --profile-name PROFILE_NAME --region REGION --aws-access-key-id AWS_ACCESS_KEY_ID --aws-secret-access-key AWS_SECRET_ACCESS_KEY
```

### 2.`job`
The job command is used for managing HPC job scripts and information.

Subcommands:
+ create: Generate a job script based on provided Git repository and version.
+ info: Fetch and display information about jobs.
```bash
job create --job-id JOB_ID
job config --job-id JOB_ID
job info JOB_UUIDS
```

To load micromamba and river command line tool with these setup, run the below or add it to .bashrc 
```bash
source ~/.river.sh
```

### License
This project is licensed under the MIT License.