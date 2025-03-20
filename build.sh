#!/bin/bash

# Update package lists
apt-get update 

# Install system-level dependencies for PyAudio
apt-get install -y \
  libasound2-dev \
  portaudio19-dev \
  libportaudio2 \
  libportaudiocpp0 \
  python3-dev \
  python3-pyaudio

# Install Python dependencies
pip install -r requirements.txt
