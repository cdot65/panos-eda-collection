FROM docker.io/arm64v8/fedora:39

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
LABEL name="ghcr.io/cdot65/panos-eda:arm"
LABEL maintainer="cremsburg.dev@gmail.com"
LABEL description="Docker container for PAN-OS EDA collection"
LABEL license="Apache 2.0"
LABEL url="https://github.com/cdot65/panos-eda-collection"
LABEL build-date="20230321"

# ---------------------------------------------------------------------------
# Install Python dependencies and packages
# ---------------------------------------------------------------------------
RUN dnf install -y python3-devel python3-pip java-17-openjdk-devel
ADD requirements.txt /var/tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /var/tmp/requirements.txt

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-17
