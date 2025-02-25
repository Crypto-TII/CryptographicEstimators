FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractiv
ENV SAGE_PKGS=/usr/share/sagemath/installed
WORKDIR "/home/cryptographic_estimators/"
RUN apt update && apt upgrade -y
RUN apt install -y sagemath python3-full && pip install toml
# Avoid the download and installation of dependencies on rebuild; 
# but without harcoding them
COPY ./pyproject.toml ./
COPY ./scripts/generate_requirements.py ./scripts/
RUN python3 scripts/generate_requirements.py
RUN sage -python3 -m pip install -r requirements.txt && rm -r ./*
RUN sage -python3 -m pip install setuptools --upgrade
COPY . .
RUN sage -python3 -m pip install --no-deps .
