FROM ubuntu:jammy-20240911.1
RUN useradd -m -N -u 1000 ubuntu && \
    echo 'APT::Install-Recommends "false";' > /etc/apt/apt.conf.d/99disable-install-recommends #
RUN apt-get update && apt-get install -y \
    python3.10 \
    pip \
    nano \
    unzip \
    curl \
    git \
    default-jdk-headless
USER ubuntu
WORKDIR /home/ubuntu/
ENV PATH=/home/ubuntu/.local/bin:$PATH

COPY --chown=ubuntu requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

COPY --chown=ubuntu giskard/llm_scan.py giskard/llm_scan.py
COPY --chown=ubuntu Dependency-Check/dependency-check-example-report.html Dependency-Check/dependency-check-example-report.html
WORKDIR /home/ubuntu/Dependency-Check
RUN VERSION=$(curl -s https://jeremylong.github.io/DependencyCheck/current.txt) && \
    curl -Ls "https://github.com/jeremylong/DependencyCheck/releases/download/v$VERSION/dependency-check-$VERSION-release.zip" --output dependency-check.zip && \
    unzip dependency-check.zip && \
    rm -rf dependency-check.zip
WORKDIR /home/ubuntu/
