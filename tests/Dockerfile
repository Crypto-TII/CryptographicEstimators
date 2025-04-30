FROM sagemath/sagemath
WORKDIR "/home/cryptographic_estimators/"

# Sage base image is very restrictive without sudo
USER root

# Set Python path to include project root
ENV PYTHONPATH=/home/cryptographic_estimators

# Install the library in development mode
COPY . .
RUN sage -pip install -e .
