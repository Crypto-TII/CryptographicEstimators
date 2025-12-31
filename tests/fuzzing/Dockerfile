FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR "/home/cryptographic_estimators/"

# NOTE: the version is 3.10 is on purpose. DO NOT CHANGE. atheris only supports this
# Thats the reason we use such a old ubuntu
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    clang llvm \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv .venv
ENV PATH=".venv/bin:$PATH"

RUN pip install toml atheris
COPY ./pyproject.toml ./
COPY ./scripts/generate_requirements.py ./scripts/
RUN python3 scripts/generate_requirements.py
RUN pip install -r requirements.txt && rm -r ./*
COPY . .
RUN pip install --no-deps .
