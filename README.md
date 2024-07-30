# <p align="center">OUSPG LLM Hackathon Environment</p>

# <p align="center">Introduction</p>
This repository contains a Docker environment for vulnerability testing Large Language Models (LLMs). The environment contains [Giskard](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html) and [Garak](https://docs.garak.ai/garak) tools for finding vulnerabilities by prompting a LLM, as well as [DependencyCheck](https://github.com/jeremylong/DependencyCheck/blob/main/README.md) for finding vulnerabilities in projects' dependencies.

<br><br><br>

# <p align="center">Quickstart</p>

## <p align="center">Prerequisites</p>

### Required

- Install latest version of [Docker](https://docs.docker.com/engine/install/) and have it running.
- Make sure port **11434** is not in use by any program.
  - On **Linux** you can check ports that are in use with: `lsof -i -P -n | grep LISTEN`
  - On **Windows** you can check ports that are in use with: `netstat -bano`
  - On **MacOS** `lsof -i -P -n | grep LISTEN` or `netstat -pan` *may* work.
- ~20Gb of disk space.

### Optional
- Install and configure [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for Docker to allow GPU accelerated container support if you are using a Nvidia GPU.
- For using **garak** with certain [Hugging Face](https://huggingface.co/) models (Phi-3-Mini for example), you need to create a Hugging Face account [here](https://huggingface.co/join). After you have an account, create and save a Hugging Face User Access Token with "Read" priviliges. You can create one [here](https://huggingface.co/settings/tokens) when you are logged in.
- To save 15 minutes of time when using DependencyCheck, request a NVD API key [here](https://nvd.nist.gov/developers/request-an-api-key). The link for your personal NVD API key will be sent to your email - save it for later use.

<br><br><br>

## <p align="center">Setup</p>

### Step 1

- Clone this repository to your local machine with: 
```console
  git clone https://github.com/Zippo00/LLM_Hackathon.git
```
- Navigate to the repository with: 
```console
  cd LLM_Hackathon
```
*If you are using an **AMD GPU** and wish to utilize its computation in running LLMs, remove lines 1-28 from `compose.yaml` and uncomment lines 34 - 54.*
- Build the **llm-hackathon** and **ollama** Docker containers with: 
```console
  docker compose up
```
- You may automatically get stuck inside the **ollama** container. Exit it with: `Ctrl + C`

### Step 2

- Make sure the **ollama** container is running with: 
```console
  docker container start ollama
```
- Download & run [Microsoft's Phi-3-Mini](https://ollama.com/library/phi3) model inside the **ollama** container with: 
```console
  docker exec -it ollama ollama run phi3
```
*You can use any other LLM from [Ollama Library](https://ollama.com/library) as well. Just replace the `phi3` in the above command with the corresponding LLM tag.*
- After the download is complete you should be able to chat with the model. Type `/bye` to leave the interactive mode.

### Step 3

- Make sure the **llm-hackathon** container is running with: 
```console
  docker container start llm_hackathon
```
- Attach to the container's shell with: 
```console
  docker exec -ti llm_hackathon /bin/bash
```

- Type `ls` to see contents of current directory and if you see `giskard` as the output, as in the image below - Congratulations! You have succesfully completed the setup part. 

![setup complete](/assets/img/setup_done.png "`pwd` output")



<br><br><br>

## <p align="center">Usage</p>

The **llm-hackathon** container includes [Garak](https://docs.garak.ai/garak) and [Giskard](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html) LLM vulnerability tools, as well as [DependencyCheck](https://github.com/jeremylong/DependencyCheck/blob/main/README.md).

<br><br>
### <ins>Giskard</ins>
If you aren't already attached to the **llm_hackathon** container's shell, do so with the command `docker exec -ti llm_hackathon /bin/bash`. 

- Use command `ls` to make sure there is a directory labeled "giskard" in your current directory.
![setup complete](/assets/img/setup_done.png "`pwd` output")

- If there is, you can check the contents of the "giskard" directory with `ls giskard`.
- The Python file `llm_scan.py` contains a Python script that runs a Giskard LLM scan on the LLM previously downloaded to the **ollama** container (Default: 'phi3', you need to change `MODEL` parameter in `llm_scan.py` if you selected a different model).
- You can define a custom dataset that will be used to evaluate the LLM by altering the `custom_dataset` parameter in the `llm_scan.py` file.
- You can start the Giskard LLM Scan with:
```console
  python3 giskard/llm_scan.py
```
- After the scan is complete, the Giskard tool will generate an evaluation report into the current directory labeled `giskard_scan_results.html`.
- You can copy the results file to your local host machine and explore the report in browser:
  - Exit the container with command `exit` or by pressing `Ctrl + D`
  - Run command:
```console
  docker cp llm_hackathon:/home/ubuntu/giskard_scan_results.html .
```
-
    - Open the `giskard_scan_results.html` in a browser and you should see a report such as in the image below.

![Giskard report](/assets/img/giskard_report.PNG "Giskard report")

***Note:** Running the Giskard LLM Scan can take up to an hour or even several hours based on the computation power the LLM is being run on and the size of the dataset used to evaluate the LLM. This repository contains an example evaluation report in the giskard directory labeled `giskard/giskard_scan_results.html` that was produced after running the scan on Phi-3-Mini model using [Hackaprompt dataset](https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset). You can open this `html` file within your browser, and explore what kind of a report the tool would produce after running the complete scan.*
  
<br><br>
### <ins>Garak</ins>

If you aren't already attached to the **llm_hackathon** container's shell, do so with the command:
```console
  docker exec -ti llm_hackathon /bin/bash
```

You can now use [garak](https://docs.garak.ai/garak) via the shell. To list different available garak probes, type:   
```console
  python3 -m garak --list_probes
```
You should see an output such as in the image below:

![garak probes list](/assets/img/garak_probes.PNG "garak probes list")

You can run the probes on all available models in [Hugging Face Models](https://huggingface.co/models) (some require authentication and more computation power than others). 

Hugging Face API has rate limits, so in order to run garak probes on certain Hugging Face models, we need to set a personal User Access Token as an environment variable. If you don't already have a Hugging Face User Access Token, you can create one [here](https://huggingface.co/settings/tokens) after you have created an account and are logged in to the [Hugging Face](https://huggingface.co/) web platform.

Set your personal User Access Token as an environment variable with: 
```console
  export HF_INFERENCE_TOKEN=REPLACE_THIS_WITH_YOUR_TOKEN
```

Now we can, for example, run `malwaregen.Evasion` probe on Microsoft's `Phi-3-Mini` model with the command:
```console
  python3 -m garak --model_type huggingface.InferenceAPI --model_name microsoft/Phi-3-mini-4k-instruct --probes malwaregen.Evasion
```

After garak has ran it's probe(s), it will generate reports into `garak_runs` directory. 
You can copy the reports to your local host machine and explore the report files. The `html` file contains a summary of the results and the `json` files contain chat logs:
  - Exit the container with command `exit` or by pressing `Ctrl + D`
  - Run command:
  ```console
  docker cp llm_hackathon:/home/ubuntu/garak_runs/ garak_runs
```
  - Explore the report files.

![garak report snippet](/assets/img/garak_report.PNG "garak report snippet")

<br><br>
### <ins>DependencyCheck</ins>

If you aren't already attached to the **llm_hackathon** container's shell, do so with the command:
```console
  docker exec -ti llm_hackathon /bin/bash
```
*Make sure you are in the correct directory. Type `pwd` and if the output is `/home/ubuntu` - you are.*

You can use [DependencyCheck](https://jeremylong.github.io/DependencyCheck/) to scan any repository utilizing [languages](https://jeremylong.github.io/DependencyCheck/analyzers/index.html) supported by the DependencyCheck project. 

Let's analyze the tool we just used, [garak](https://github.com/leondz/garak), as an example.

Clone the repository with:
```console
  git clone https://github.com/leondz/garak.git
```
Garak is a Python project and it contains a `requirements.txt` file, which is a list of required dependencies to run the software.

*To save 15 minutes of your time when running the first analysis, you need a NVD API key. If you don't already have one, you can request one [here](https://nvd.nist.gov/developers/request-an-api-key) and a link to it will be sent to your email.*

To analyze the repository with DependencyCheck, scan the `requirements.txt` file with the command *(if you wish not to use a NVD API Key, remove the `--nvdApiKey REPLACE_THIS_WITH_YOUR_API_KEY` part)*:
```console
  /home/ubuntu/Dependency-Check/dependency-check/bin/dependency-check.sh \
--enableExperimental \
--out . \
--scan garak/requirements.txt \
--nvdApiKey REPLACE_THIS_WITH_YOUR_API_KEY
```

DependencyCheck will generate a `html` file of the analysis report, which you can copy from the container to your local machine.
  - Exit the container with the command `exit` or by pressing `Ctrl + D`.
  - Run command:
  ```console
  docker cp llm_hackathon:/home/ubuntu/dependency-check-report.html .
```
  - Explore the report file.

![DependencyCheck report snippet](/assets/img/dependency-check-report.PNG "DependencyCheck report snippet")

<br><br>
### <ins>Editing files inside a container</ins>

The **llm_hackathon** container includes [nano](https://www.nano-editor.org/dist/latest/cheatsheet.html) text editor. You can start editing `llm_scan.py` file while connected to the container's shell with the command: 
```console
  nano giskard/llm_scan.py
```

<br><br><br><br><br>
## Useful resources:

[Garak ReadMe](https://github.com/leondz/garak?tab=readme-ov-file)  
[Garak Documentation](https://docs.garak.ai/garak)  
  
[Giskard ReadMe](https://github.com/Giskard-AI/giskard)  
[Giskard Documentation](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html)  

[DependencyCheck ReadMe](https://github.com/jeremylong/DependencyCheck/blob/main/README.md)  
[DependencyCheck Documentation](https://jeremylong.github.io/DependencyCheck/)  
[DependencyCheck CLI Arguments](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/arguments.html)  
[DependencyCheck Supported File Types](https://jeremylong.github.io/DependencyCheck/analyzers/index.html)  
