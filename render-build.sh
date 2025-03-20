#!/bin/bash
set -e

# Update package list and install portaudio dependencies
apt-get update && apt-get install -y portaudio19-dev python3-dev python3-pip gcc

# Install required packages
pip install -r requirements.txt

