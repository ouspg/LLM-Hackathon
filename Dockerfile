# Use Ubuntu's current LTS
FROM ubuntu:jammy-20240530

RUN apt update && \
    apt install --no-install-recommends -y python3.10 && \
    apt install --no-install-recommends -y pip && \
    apt install nano && \
    python3 -m pip install -U garak && \
    python3 -m pip install giskard[llm] && \
    python3 -m pip install -U fsspec && \
    python3 -m pip install -U pyarrow && \
    python3 -m pip install -U huggingface_hub

WORKDIR /home/ubuntu/
COPY giskard/llm_scan.py giskard/llm_scan.py