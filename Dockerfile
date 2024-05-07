# Use Amazon Linux 2 as the base image
FROM amazonlinux:2

# Labels for the Docker image
LABEL version="1.0"
LABEL description="Amazon Linux 2 with Python 3.11"

# Install system dependencies necessary for building Python
RUN yum update -y && \
    yum groupinstall -y "Development Tools" && \
    yum install -y \
        gcc openssl-devel bzip2-devel libffi-devel \
        zlib-devel xz-devel tk-devel readline-devel \
        gdbm-devel db4-devel libpcap-devel sqlite-devel

# Download Python 3.11
WORKDIR /usr/src
RUN curl -O https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz

# Extract and install Python 3.11
RUN tar xzf Python-3.11.7.tgz && \
    cd Python-3.11.7 && \
    ./configure --enable-optimizations --with-ensurepip=install && \
    make -j4 altinstall

# Remove the archive and source directory to save space
RUN rm /usr/src/Python-3.11.7.tgz && \
    rm -rf /usr/src/Python-3.11.7

# Set Python 3.11 as the default python and pip
RUN ln -fs /usr/local/bin/python3.11 /usr/bin/python3 && \
    ln -fs /usr/local/bin/pip3.11 /usr/bin/pip3