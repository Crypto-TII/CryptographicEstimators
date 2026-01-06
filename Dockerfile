FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home/cryptographic_estimators/

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

RUN pip install toml
COPY ./pyproject.toml ./
COPY ./scripts/generate_requirements.py ./scripts/
RUN python3 scripts/generate_requirements.py
RUN pip install -r requirements.txt && rm -r ./*
COPY . .
RUN pip install --no-deps .
