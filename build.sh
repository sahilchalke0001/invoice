#!/bin/bash

# Install system-level dependencies
apt-get update && apt-get install -y libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0


# Install required Python packages
pip install -r requirements.txt
