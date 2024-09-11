# Use Ubuntu's current LTS
FROM ubuntu:jammy-20240530

RUN apt update && \
    apt install --no-install-recommends -y python3.10 && \
    apt install --no-install-recommends -y pip && \
    apt install nano && \
    apt install unzip -y && \
    apt install curl -y && \
    apt install git -y && \
    apt install default-jdk -y && \
    # apt install cargo -y && \
    # python3 -m pip install maturin && \
    python3 -m pip install -U garak==0.9.0.13 && \
    python3 -m pip install giskard[llm] && \
    python3 -m pip install -U fsspec && \
    python3 -m pip install -U pyarrow && \
    python3 -m pip install -U huggingface_hub

WORKDIR /home/ubuntu/
COPY giskard/llm_scan.py giskard/llm_scan.py
COPY Dependency-Check/dependency-check-example-report.html Dependency-Check/dependency-check-example-report.html
WORKDIR /home/ubuntu/Dependency-Check
RUN VERSION=$(curl -s https://jeremylong.github.io/DependencyCheck/current.txt) && \
    curl -Ls "https://github.com/jeremylong/DependencyCheck/releases/download/v$VERSION/dependency-check-$VERSION-release.zip" --output dependency-check.zip && \
    unzip dependency-check.zip && \
    rm -rf dependency-check.zip
WORKDIR /home/ubuntu/
