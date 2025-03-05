FROM ubuntu:noble-20250127

WORKDIR /home/ubuntu/

RUN apt update
RUN apt-get install --no-install-recommends -y python3
RUN apt install python3.12-venv -y

# Create a virtual environment to install Python packages in
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt install nano
RUN apt install unzip -y
RUN apt install curl -y
RUN apt install git -y
RUN apt install default-jdk -y
    # apt install cargo -y && \
    # python3 -m pip install maturin && \

#RUN pip install garak
#RUN pip install giskard[llm]
#RUN pip install -U fsspec
#RUN pip install -U pyarrow 
#RUN pip install -U huggingface_hub
#RUN pip install transformers==4.45.0
WORKDIR /home/ubuntu/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY giskard/llm_scan.py giskard/llm_scan.py
COPY Dependency-Check/dependency-check-example-report.html Dependency-Check/dependency-check-example-report.html
WORKDIR /home/ubuntu/Dependency-Check
RUN VERSION=$(curl -s https://dependency-check.github.io/DependencyCheck/current.txt) && \
    curl -Ls "https://github.com/dependency-check/DependencyCheck/releases/download/v$VERSION/dependency-check-$VERSION-release.zip" --output dependency-check.zip && \
    unzip dependency-check.zip && \
    rm -rf dependency-check.zip
WORKDIR /home/ubuntu/

