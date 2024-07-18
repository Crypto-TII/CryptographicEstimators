FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractiv
RUN apt update && apt install -y sagemath
RUN sage -python3 -m pip install prettytable scipy sphinx==5.3.0 furo pytest pytest-xdist pytest-cov python-flint
WORKDIR "/home/cryptographic_estimators/"
COPY . .
ENV SAGE_PKGS=/usr/share/sagemath/installed
RUN sage setup.py install
RUN sage -python3 -m pip install .
