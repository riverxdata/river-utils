FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
# Install necessary packages
RUN apt-get update && apt-get install -y \
    munge \
    slurm-wlm \
    slurm-wlm-basic-plugins \
    slurmdbd \
    mariadb-server \
    mariadb-client \
    build-essential \
    vim \
    curl \
    wget \
    git \
    openssh-server \
    fuse \
    net-tools \
    python3 python3-dev python3-pip python3-venv \
    && apt-get clean

# Create user for the cluster
RUN useradd -m -s /bin/bash river && echo "river:password" | chpasswd
COPY .ssh/id_rsa.pub /home/river/.ssh/authorized_keys
RUN chown -R river:river /home/river/.ssh
RUN chmod 700 /home/river/.ssh/authorized_keys

USER root
# Setup SSH server
RUN mkdir -p /run/sshd

# Setup SLURM
RUN mkdir -p /etc/munge /var/log/munge /var/lib/munge /etc/slurm /var/spool/slurmd
RUN chown -R munge:munge /etc/munge /var/log/munge /var/lib/munge \
    && chmod 0700 /etc/munge /var/log/munge /var/lib/munge
RUN /usr/sbin/create-munge-key

# Copy configuration files
COPY slurm.conf /etc/slurm-llnl/slurm.conf
COPY slurmdbd.conf /etc/slurm-llnl/slurmdbd.conf
RUN mkdir -p /var/log/slurm

# Setup MySQL
RUN mkdir -p /var/run/mysqld && \
    chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

# Start MariaDB and initialize the SLURM database
RUN service mysql start && \
    mysql -e "CREATE DATABASE slurm_acct_db;" && \
    mysql -e "CREATE USER 'slurm'@'localhost' IDENTIFIED BY 'slurm';" && \
    mysql -e "GRANT ALL PRIVILEGES ON slurm_acct_db.* TO 'slurm'@'localhost';" && \
    mysql -e "FLUSH PRIVILEGES;"

# Expose necessary ports
EXPOSE 22 6817 6818 3306

# Copy MySQL configuration
COPY my.cnf /etc/mysql/my.cnf

USER root
RUN usermod -s /bin/bash slurm

# Install and configure river-utils
USER river
WORKDIR /home/river
COPY ./river-1.0.0-py3-none-any.whl .
RUN pip install river-1.0.0-py3-none-any.whl
ENV PATH=$PATH:/home/river/.local/bin
RUN river setup install
RUN mkdir -p /home/river/.river/jobs/uuid/
COPY ./job.sh /home/river/.river/jobs/uuid/job.sh
COPY ./test-slurmdbd.sh .

USER root
RUN chmod u+x /home/river/test-slurmdbd.sh
# RUN bash -c "/home/river/test-slurmdbd.sh"

# CMD ["bash", "-c", "/etc/init.d/munge start && \
#     service mysql start && \
#     /usr/sbin/sshd && \
#     slurmdbd && \
#     slurmctld && \
#     slurmd -D"]