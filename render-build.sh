#!/bin/bash

# Install system dependencies required for PyAudio
apt-get update && apt-get install -y portaudio19-dev

# Install project dependencies
pip install -r requirements.txt
