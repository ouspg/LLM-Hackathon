# Use Ubuntu's current LTS
FROM ubuntu:jammy-20240530

RUN apt update && \
    apt install --no-install-recommends -y python3.10 && \
    apt install --no-install-recommends -y pip

WORKDIR /garak
RUN python3 -m pip install -U garak

