FROM ubuntu:24.10
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR "/home/cryptographic_estimators/"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# # Avoid the download and installation of dependencies on rebuild; 
# # but without harcoding them
RUN pip install toml
# COPY ./pyproject.toml ./
# COPY ./scripts/generate_requirements.py ./scripts/
# RUN python3 scripts/generate_requirements.py
# RUN pip install -r requirements.txt && rm -r ./*
COPY . .
RUN tree .
# RUN pip install --no-deps .
RUN pip install .

