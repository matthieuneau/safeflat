# Start with the Amazon Linux 2 base image
FROM amazonlinux:2

# Labels for metadata
LABEL maintainer="your-email@example.com"
LABEL description="Amazon Linux 2 with Python 3.11"

# Update the system
RUN yum -y update

# Install development tools and libraries needed to compile Python
RUN yum -y groupinstall "Development Tools"
RUN yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel \
    readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel \
    libuuid-devel

# Specifically remove Python 2.x packages, avoiding wildcards that might unintentionally remove other packages
RUN yum -y remove python2 python2-pip || true

# Download and install Python 3.11
RUN curl -O https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz && \
    tar -xzf Python-3.11.7.tgz && \
    cd Python-3.11.7 && \
    ./configure --enable-optimizations --with-openssl=/usr/include/openssl && \
    make altinstall

# Clean up unnecessary files and cache to reduce image size
RUN rm -rf Python-3.11.7.tgz Python-3.11.7 /var/cache/yum

# Set the newly installed Python as the default python
RUN ln -sf /usr/local/bin/python3.11 /usr/bin/python3
RUN ln -sf /usr/local/bin/pip3.11 /usr/bin/pip3

# Set the default command for the container to check Python version
CMD ["python3", "--version"]