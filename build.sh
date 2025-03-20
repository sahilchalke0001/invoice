#!/bin/bash
# Update package lists
apt-get update
# Install required dependencies for PyAudio and PortAudio
apt-get install -y libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
