FROM fedora:39

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
LABEL name="ghcr.io/cdot65/panos-eda:x86"
LABEL maintainer="cremsburg.dev@gmail.com"
LABEL description="Docker container for PAN-OS EDA collection"
LABEL license="Apache 2.0"
LABEL url="https://github.com/cdot65/panos-eda-collection"
LABEL build-date="20230321"

# ---------------------------------------------------------------------------
# Copy project to build context
# ---------------------------------------------------------------------------
COPY . /var/tmp
WORKDIR /var/tmp

# ---------------------------------------------------------------------------
# Install Python dependencies and packages
# ---------------------------------------------------------------------------
RUN dnf install -y python3-devel python3-pip gcc
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# ---------------------------------------------------------------------------
# Install OpenJDK 17
# ---------------------------------------------------------------------------
RUN dnf install -y java-17-openjdk-devel

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk

# ---------------------------------------------------------------------------
# Copy local directory into container build and install Ansible collections
# ---------------------------------------------------------------------------
RUN ansible-galaxy install -r requirements.yaml

# ---------------------------------------------------------------------------
# Cleanup and remove build dependencies
# ---------------------------------------------------------------------------
RUN rm -rf /var/tmp/*
RUN dnf remove -y gcc python3-devel
