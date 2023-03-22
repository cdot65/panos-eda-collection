"""Tasks to execute with Invoke."""

# ---------------------------------------------------------------------------
# standard library
# ---------------------------------------------------------------------------
import inspect
import os
import platform

# ---------------------------------------------------------------------------
# third party
# ---------------------------------------------------------------------------
import distro
from invoke import task


# ---------------------------------------------------------------------------
# Python3.11 hack for invoke
# ---------------------------------------------------------------------------
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


# ---------------------------------------------------------------------------
# Determine CPU architecture
# ---------------------------------------------------------------------------
def get_os_architecture():
    arch = platform.machine()

    if (
        "x86" in arch
        or "i386" in arch
        or "i686" in arch
        or "AMD64" in arch
        or "amd64" in arch
    ):
        return "x86"
    elif "arm" in arch or "aarch64" in arch:
        return "ARM"
    else:
        return "Unknown"


CPU_ARCHITECTURE = get_os_architecture()


# ---------------------------------------------------------------------------
# Determine Host operating system (to use Docker or Podman)
# ---------------------------------------------------------------------------
def get_container_runtime():
    dist = distro.id()

    if "rhel" in dist or "fedora" in dist or "centos" in dist:
        return "podman"
    else:
        return "docker"


CONTAINER_RUNTIME = get_container_runtime()

# ---------------------------------------------------------------------------
# CONTAINER PARAMETERS
# ---------------------------------------------------------------------------
CONTAINER_IMG = "ghcr.io/cdot65/panos-eda"

ARM_TAG = "arm"
X86_TAG = "x86"
VERSION = "0.1.0"

TCP_PORT = 5000

# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# CONTAINER CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task(optional=["arm"])
def build(context, arm=None):
    """Build our Container images."""
    if CPU_ARCHITECTURE == "ARM" or arm:
        context.run(
            f"{CONTAINER_RUNTIME} build -t {CONTAINER_IMG}:{ARM_TAG}-{VERSION} docker/arm",
        )
    else:
        context.run(
            f"{CONTAINER_RUNTIME} build -t {CONTAINER_IMG}:{X86_TAG}-{VERSION} .",
        )


# ---------------------------------------------------------------------------
# SHELL ACCESS
# ---------------------------------------------------------------------------
@task(optional=["arm"])
def shell(context, arm=None):
    """Get shell access to the container."""
    if CPU_ARCHITECTURE == "ARM" or arm:
        context.run(
            f"{CONTAINER_RUNTIME} run -it --rm -v {PWD}/eda:/code/eda:z -w /code/eda -p {TCP_PORT}:5000 {CONTAINER_IMG}:{ARM_TAG}-{VERSION} /bin/sh",
            pty=True,
        )
    else:
        context.run(
            f"{CONTAINER_RUNTIME} run -it --rm -v {PWD}/eda:/code/eda:z -w /code/eda -p {TCP_PORT}:5000 {CONTAINER_IMG}:{X86_TAG}-{VERSION} /bin/sh",
            pty=True,
        )


# ---------------------------------------------------------------------------
# Run rule book on localhost as container
# ---------------------------------------------------------------------------
@task(optional=["arm"])
def local(context, arm=None):
    """Run Ansible rule book."""
    if CPU_ARCHITECTURE == "ARM" or arm:
        context.run(
            f"{CONTAINER_RUNTIME} run -it --rm -v {PWD}/eda:/code/eda:z -w /code/eda -p {TCP_PORT}:5000 {CONTAINER_IMG}:{ARM_TAG}-{VERSION} ansible-rulebook --rulebook rulebooks/panos.yaml --inventory inventory/localhost.yaml --verbose",
            pty=True,
        )
    else:
        context.run(
            f"{CONTAINER_RUNTIME} run -it --rm -v {PWD}/eda:/code/eda:z -w /code/eda -p {TCP_PORT}:5000 {CONTAINER_IMG}:{X86_TAG}-{VERSION} ansible-rulebook --rulebook rulebooks/panos.yaml --inventory inventory/localhost.yaml --verbose",
            pty=True,
        )
