FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractiv
#ENV SAGE_PKGS=/usr/share/sagemath/installed
WORKDIR "/home/cryptographic_estimators/"
RUN apt update && apt install -y python3-full python3-pip python3-toml
# Avoid the download and installation of dependencies on rebuild; 
# but without harcoding them
COPY ./pyproject.toml ./
COPY ./scripts/generate_requirements.py ./scripts/
RUN python3 scripts/generate_requirements.py
RUN pip install -r requirements.txt --break-system-packages && rm -r ./*
COPY . .
RUN pip install --no-deps --break-system-packages .
