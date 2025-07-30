# Start with Ubuntu Linux as the base
FROM ubuntu:22.04

# Prevent interactive prompts during install (e.g., tzdata)
ENV DEBIAN_FRONTEND=noninteractive

# Install required tools: gcc for C, gdb for debugging, python3 for scripts
RUN apt update && apt install -y \
    gcc \
    gdb \
    python3 \
    python3-pip

# Set the working directory inside the container
WORKDIR /app

# Copy all files from your local folder into the container
COPY . .

# Tell Docker to start in an interactive shell when the container runs
CMD ["/bin/bash"]
