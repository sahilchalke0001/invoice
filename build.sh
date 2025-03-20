#!/bin/bash

# Update system packages and install PortAudio dependencies
apt-get update && apt-get install -y portaudio19-dev

# Install required Python packages
pip install -r requirements.txt
