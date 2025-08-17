FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    gcc \
    gdb \
    python3 \
    python3-pip

WORKDIR /app

COPY . .

CMD ["/bin/bash"]
