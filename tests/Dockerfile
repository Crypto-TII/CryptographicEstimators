FROM sagemath/sagemath
WORKDIR "/home/cryptographic_estimators/"

# Sage base image is very restrictive without sudo
USER root

# Install the library in development mode
COPY . .
RUN sage -pip install -e .

# Restore normal user
USER sage

