FROM sagemath/sagemath
ENV SAGE_PKGS=/usr/share/sagemath/installed

USER root
WORKDIR "/home/sage/cryptographic_estimators/"
RUN chown -R sage:sage /home/sage/cryptographic_estimators
RUN apt update && apt install -y python3 pip

# Avoid the download and installation of dependencies on rebuild; 
# but without hardcoding them
RUN pip install toml
COPY --chown=sage:sage ./pyproject.toml ./
COPY --chown=sage:sage ./scripts/generate_requirements.py ./scripts/
RUN python3 scripts/generate_requirements.py
RUN sage -python3 -m pip install -r requirements.txt && rm -r ./*
COPY --chown=sage:sage . .

RUN sage -python3 -m pip install --no-deps .

WORKDIR "/home/sage/cryptographic_estimators/cryptographic_estimators""

