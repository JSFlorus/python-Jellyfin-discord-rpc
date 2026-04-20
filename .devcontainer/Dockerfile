FROM mcr.microsoft.com/devcontainers/base:noble

#Update
RUN apt-get update && apt-get install -y \
#For gcc, g++, make, and libc among other tools that python needs for its libraries
    build-essential \
    python3 \
    python3-pip 