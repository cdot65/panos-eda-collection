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
# Install Python dependencies
# ---------------------------------------------------------------------------
RUN dnf install -y python3-devel python3-pip gcc

# ---------------------------------------------------------------------------
# Install OpenJDK 17
# ---------------------------------------------------------------------------
RUN dnf install -y java-17-openjdk-devel

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk

# ---------------------------------------------------------------------------
# Copy project to build context
# ---------------------------------------------------------------------------
COPY requirements.txt /var/tmp
WORKDIR /var/tmp

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# ---------------------------------------------------------------------------
# Copy local directory into container build and install Ansible collections
# ---------------------------------------------------------------------------
COPY . /var/tmp
RUN ansible-galaxy install -r requirements.yaml

# ---------------------------------------------------------------------------
# Cleanup and remove build dependencies
# ---------------------------------------------------------------------------
RUN rm -rf /var/tmp/*
RUN dnf remove -y gcc python3-devel
