# Dockerfile for ARM

## Overview

This Dockerfile differs from the x86 version in two ways:

1. It uses an ARM architecture base image for Fedora
2. It is not concerned with building of the Ansible Collection, favoring to download from Galaxy.

While the first point is obvious, this second point is by design. The ARM architecture is not as popular as x86, and the build process for the collection is quite long. This Dockerfile is intended to be used for testing purposes, and not for production. As such, it is not concerned with building the collection, but rather downloading it from Galaxy.

This results in a flow where I'll build the collection on an x86 machine, publish to Galaxy, and then download it on an ARM machine. This is not ideal, but it is the best I can do for now.
