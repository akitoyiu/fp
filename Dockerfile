# a pre-built Ubuntu server installed with Python version 3.
FROM python:3

# a setting below to instruct all the python output will be sent straight to the terminal
ENV PYTHONUNBUFFERED 1

# create a local folder in the virtual machine and set the active working dir
RUN mkdir /setup
WORKDIR /setup

# update and setup some basic tools for Ubuntu
# Because the pre-built Ubuntu server only contain the barebone kernel
RUN apt-get update && apt-get install -y net-tools nano software-properties-common

# Install the ffmpeg tools for video conversion.
RUN apt-get install -y ffmpeg

# a separate text files for all the required Python libraries.
# It will be installed using the pip commands
COPY requirements.txt /setup/

RUN pip install -r requirements.txt