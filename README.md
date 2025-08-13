# <p align="center">LLM Hackathon Environment</p>


## <p align="center">Table of Contents</p>

- [Introduction](#intro)
- [Quickstart](#quickstart)
  - [Prerequisites](#prereq)
      - [Required](#required)
      - [Optional](#optional)
  - [Setup](#setup)
  - [Usage](#usage)
      - [Garak](#garak)
      - [DependencyCheck](#odc)
      - [Giskard](#giskard)
- [Editing files inside a container](#editfile)
- [Using a LLM via REST API](#restllm)
- [Useful resources](#resource) 

# <p align="center">Introduction</p> <a name="intro"></a>
This repository contains a Docker environment for vulnerability testing Large Language Models (LLMs). The environment contains [Giskard](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html) and [Garak](https://docs.garak.ai/garak) tools for finding vulnerabilities by prompting a LLM, as well as [DependencyCheck](https://github.com/jeremylong/DependencyCheck/blob/main/README.md) for finding vulnerabilities in projects' dependencies. 

Following the **Quickstart** guide below will introduce you to each of the tools through examples. The guide contains three **OBJECTIVE**s and by completing all of them, you know you have learned how to utilize the tools for vulnerability testing LLMs. 

You can find a video series showcasing the **Quickstart** at [OUSPG's Youtube Channel](https://www.youtube.com/watch?v=YGzoOfFYayU&list=PL1fscFAejNoAz9gZlsubHdqGKfbswDSK2&index=2&ab_channel=OUSPG).

<br><br><br>

# <p align="center">Quickstart</p> <a name="quickstart"></a>

## <p align="center">Prerequisites</p> <a name="prereq"></a>

### Required <a name="required"></a>

- Install latest version of [Docker](https://docs.docker.com/engine/install/) and have it running.
- Make sure port **11434** is not in use by any program.
  - On **Linux** you can check ports that are in use with: `lsof -i -P -n | grep LISTEN`
  - On **Windows** you can check ports that are in use with: `netstat -bano`
  - On **MacOS** `lsof -i -P -n | grep LISTEN` or `netstat -pan` *may* work.
- ~20Gb of disk space.
-  5.6 GB of RAM for running containerized [Phi-3-Mini](https://ollama.com/library/phi3) for **giskard** tool.

### Optional <a name="optional"></a>
<!---
- For using **garak** with certain [Hugging Face](https://huggingface.co/) models (Phi-3-Mini for example), you need to create a Hugging Face account [here](https://huggingface.co/join). After you have an account, create and save a Hugging Face User Access Token with "Read" priviliges. You can create one [here](https://huggingface.co/settings/tokens) when you are logged in.
-->
- To save 15 minutes of time when using **DependencyCheck**, request a NVD API key [here](https://nvd.nist.gov/developers/request-an-api-key). The link for your personal NVD API key will be sent to your email - save it for later use.

<br><br><br>

## <p align="center">Setup</p> <a name="setup"></a>

Running a Large Language Model for inference can be computationally intensive. It is recommended to utilize the computation of your GPU for running the LLM, if you have a compatible GPU for GPU accelerated containers. Below there are several different collapsible Setup sections for different hardware. Follow the one that matches the hardware you are using. If none match, choose **Setup for CPU only**.

<details>
  <summary>Setup for NVIDIA GPU</summary>

### Step 1 

Install and configure [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for Docker to allow GPU accelerated container support. 

### Step 2

- Clone this repository to your local machine with: 
```console
  git clone https://github.com/ouspg/LLM-Hackathon.git
```
- Navigate to the repository with: 
```console
  cd LLM-Hackathon
```

- Open `compose.yaml` with your text editor and uncomment the `deploy` blocks (lines 7-13 & 22-28). The `compose.yaml` file should look as in the image below:

![compose.yaml for Nvidia GPU](/assets/img/nvidia-setup.PNG)

- Build the **llm_hackathon** and **ollama** Docker containers with: 
```console
  docker compose up -d
``` 


> *Note: Building the container environment may take up to 20 minutes* 



### Step 3

> *Note: If you have less than 5.6GB of RAM on your machine, skip this step* 

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

### Step 4

- Make sure the **llm_hackathon** container is running with: 
```console
  docker container start llm_hackathon
```
- Attach to the container's shell with: 
```console
  docker exec -ti llm_hackathon /bin/bash
```

- Type `ls` to see contents of current directory and if you see an output as in the image below - Congratulations! You have succesfully completed the setup part. 

![setup complete](/assets/img/llm_hackathon-container-contents.png "`ls` output") 
</details>

<br>

<details>
  <summary>Setup for AMD GPU</summary>

### Step 1

- Clone this repository to your local machine with: 
```console
  git clone https://github.com/ouspg/LLM-Hackathon.git
```
- Navigate to the repository with: 
```console
  cd LLM-Hackathon
```

- Open `compose.yaml` with your text editor and uncomment lines 35-55. Remove lines 1-28. The `compose.yaml` file should look as in the image below:

![compose.yaml for AMD GPU](/assets/img/amd-setup.PNG)

- Build the **llm_hackathon** and **ollama** Docker containers with: 
```console
  docker compose up -d
```

> *Note: Building the container environment may take up to 20 minutes*

*If you get an error response from daemon such as "Error response from daemon: error gathering device information while adding custom device "/dev/kfd": no such file or directory", remove the `- /dev/kfd` lines (lines 10 and 18)  from `compose.yaml` file.* 

### Step 2

> *Note: If you have less than 5.6GB of RAM on your machine, skip this step* 

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

- Make sure the **llm_hackathon** container is running with: 
```console
  docker container start llm_hackathon
```
- Attach to the container's shell with: 
```console
  docker exec -ti llm_hackathon /bin/bash
```

- Type `ls` to see contents of current directory and if you see an output as in the image below - Congratulations! You have succesfully completed the setup part. 

![setup complete](/assets/img/llm_hackathon-container-contents.png "`ls` output")
</details>

<br>

<details>
  <summary>Setup for macOS</summary>

### Step 1

- Clone this repository to your local machine with: 
```console
  git clone https://github.com/ouspg/LLM-Hackathon.git
```
- Navigate to the repository with: 
```console
  cd LLM-Hackathon
```

- Open `Dockerfile` with your text editor. Uncomment lines `RUN apt install cargo -y` and `RUN pip install maturin` in the `Dockerfile`, so it looks like in the image below:

![Dockerfile for macOS](/assets/img/mac-setup.PNG "Dockerfile for macOS")

- Build the **llm_hackathon** and **ollama** Docker containers with: 
```console
  docker compose up -d
```


> *Note: Building the container environment may take up to 20 minutes*

### Step 2

> *Note: If you have less than 5.6GB of RAM on your machine, skip this step* 

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

- Make sure the **llm_hackathon** container is running with: 
```console
  docker container start llm_hackathon
```
- Attach to the container's shell with: 
```console
  docker exec -ti llm_hackathon /bin/bash
```

- Type `ls` to see contents of current directory and if you see an output as in the image below - Congratulations! You have succesfully completed the setup part. 

![setup complete](/assets/img/llm_hackathon-container-contents.png "`ls` output")
</details>

<br>

<details>
  <summary>Setup for CPU only</summary>

### Step 1

- Clone this repository to your local machine with: 
```console
  git clone https://github.com/ouspg/LLM-Hackathon.git
```
- Navigate to the repository with: 
```console
  cd LLM-Hackathon
```

- Build the **llm_hackathon** and **ollama** Docker containers with: 
```console
  docker compose up -d
```

> *Note: Building the container environment may take up to 20 minutes*

### Step 2

> *Note: If you have less than 5.6GB of RAM on your machine, skip this step* 

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

- Make sure the **llm_hackathon** container is running with: 
```console
  docker container start llm_hackathon
```
- Attach to the container's shell with: 
```console
  docker exec -ti llm_hackathon /bin/bash
```

- Type `ls` to see contents of current directory and if you see an output as in the image below - Congratulations! You have succesfully completed the setup part. 

![setup complete](/assets/img/llm_hackathon-container-contents.png "`ls` output")
</details>



<br><br><br>

## <p align="center">Usage</p> <a name="usage"></a>

The **llm_hackathon** container includes [Garak](https://docs.garak.ai/garak) and [Giskard](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html) LLM vulnerability tools, as well as [DependencyCheck](https://github.com/jeremylong/DependencyCheck/blob/main/README.md).

<br><br>
### <ins>Garak</ins> <a name="garak"></a>

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

<!---You can run the probes on all available models in [Hugging Face Models](https://huggingface.co/models) (some require authentication and more computation power than others). 

Hugging Face API has rate limits, so in order to run garak probes on certain Hugging Face models, we need to set a personal User Access Token as an environment variable. If you don't already have a Hugging Face User Access Token, you can create one [here](https://huggingface.co/settings/tokens) after you have created an account and are logged in to the [Hugging Face](https://huggingface.co/) web platform. The User Accesss Token needs to have "Read" privileges (see image below).

![Hugging Face Token creation](/assets/img/hf_token_creation.PNG "Hugging Face Token creation")

Set your personal User Access Token as an environment variable with: 
```console
  export HF_INFERENCE_TOKEN=REPLACE_THIS_WITH_YOUR_TOKEN
```



Now we can, for example, run `malwaregen.Evasion` probe on Microsoft's `Phi-3-Mini` model with the command:
```console
  python3 -m garak --model_type huggingface.InferenceAPI --model_name microsoft/Phi-3-mini-4k-instruct --probes malwaregen.Evasion
```
-->

You can run the probes on all available [ollama models](https://ollama.com/library), as long as your hardware can run the model *(the model must be running inside the **ollama** container)*.

With Microsoft's `Phi-3-Mini` model running inside the **ollama** container, we can, for example, run `dan.DAN_Jailbreak` probe on the Phi-3-Mini model with the command:

```console
  python3 -m garak --config garak_misc/garak_config.yaml --model_type ollama --model_name phi3 --probes dan.DAN_Jailbreak
```

The command above first configures garak to probe an ollama model running at http://ollama:11434 with the garak_misc/garak_config.yaml file through the `--config` flag. The the command instructs garak, that the model is an ollama model with the `--model_type` flag, and that the model being probed is labeled phi3 with the `--model_name` flag. And finally, `--probes` flag let's us list all the probes that will be ran on the model. 

After garak has ran its probe(s), it will generate reports into `garak_runs` directory. 
You can copy the reports to your local host machine and explore the report files. The `html` file contains a summary of the results and the `json` files contain chat logs:
  - The directory currently needs root permissions to access, so let's change that with:
    ```console
    chmod -R a+rwX /root/.local/share/garak/garak_runs
    ```
  - Exit the container with command `exit` or by pressing `Ctrl + D`
  - Run the following command to copy the report files to your local machine into a directory labeled "garak_runs":
  ```console
  docker cp llm_hackathon:/root/.local/share/garak/garak_runs garak_runs
```
  - Explore the report files:

![garak report snippet](/assets/img/garak_report.PNG "garak report snippet")

<br> 

> [!IMPORTANT] 
> **OBJECTIVE:** Use different probes on the LLM and see what types of vulnerabilities you can find from it (all available probes might not work).

<br><br>
### <ins>DependencyCheck</ins> <a name="odc"></a>

If you aren't already attached to the **llm_hackathon** container's shell, do so with the command:
```console
  docker exec -ti llm_hackathon /bin/bash
```
*Make sure you are in the correct directory. Type `pwd` and if the output is `/home/ubuntu` - you are.*

You can use [DependencyCheck](https://jeremylong.github.io/DependencyCheck/) to scan any repository utilizing [languages](https://jeremylong.github.io/DependencyCheck/analyzers/index.html) supported by the DependencyCheck project. 

Let's analyze the tool we just used, [garak](https://github.com/leondz/garak), as an example.

Clone the repository with:
```console
  git clone https://github.com/NVIDIA/garak.git
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
  - Run the following command to copy the report to your local machine:
  ```console
  docker cp llm_hackathon:/home/ubuntu/dependency-check-report.html .
```
  - Explore the report file:

![DependencyCheck report snippet](/assets/img/dependency-check-report.PNG "DependencyCheck report snippet")

<br> 

> [!IMPORTANT] 
> **OBJECTIVE:** Find a Github repository of a software project containing [a supported file type](https://jeremylong.github.io/DependencyCheck/analyzers/index.html) by dependency-check, and see if you can find any vulnerable dependencies from the project.


<br><br>
### <ins>Giskard</ins> <a name="giskard"></a>

> [!NOTE]
> - *If you don´t have 5.6 GB of RAM on your machine and did not deploy a LLM locally with the **ollama** container, you can not use this tool. However, this repository contains an example evaluation report in the "giskard" directory labeled `giskard/giskard_scan_results.html` that was produced after running the Giskard LLM scan on Phi-3-Mini model using [Hackaprompt dataset](https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset). You can open this `html` file within your browser, and explore what kind of a report the tool would produce after running the complete scan.*
> - *Running the Giskard LLM Scan can take up to an hour or even several hours based on the computation power the LLM is being run on and the size of the dataset used to evaluate the LLM. You can try to start the Giskard LLM Scan and then abort the scan with `Ctrl + C`, if you do not wish to wait for the scan to complete. This repository contains an example evaluation report in the "giskard" directory labeled `giskard/giskard_scan_results.html` that was produced after running the Giskard LLM scan on Phi-3-Mini model using [Hackaprompt dataset](https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset). You can open this `html` file within your browser, and explore what kind of a report the tool would produce after running the complete scan.*

If you aren't already attached to the **llm_hackathon** container's shell, do so with the command `docker exec -ti llm_hackathon /bin/bash`. 

- Use command `ls` to make sure there is a directory labeled "giskard" in your current directory.
![setup complete](/assets/img/llm_hackathon-container-contents.png "`ls` output")

- If there is, you can check the contents of the "giskard" directory with `ls giskard`.
- The Python file `llm_scan.py` contains a Python script that runs a Giskard LLM scan on the LLM previously downloaded to the **ollama** container (Default: 'phi3'; You need to change `MODEL` parameter accordingly in `llm_scan.py` file if you selected a different model).
- You can define a custom dataset that will be used to evaluate the LLM by altering the `custom_dataset` parameter in the `llm_scan.py` file.
- You can start the Giskard LLM Scan with:
```console
  python3 giskard/llm_scan.py
```
- After the scan is complete, the Giskard tool will generate an evaluation report into the current directory labeled `giskard_scan_results.html`.
- You can copy the results file to your local host machine and explore the report in browser:
  - Exit the container with command `exit` or by pressing `Ctrl + D`
  - Run the following command to copy the report to your local machine:
```console
  docker cp llm_hackathon:/home/ubuntu/giskard_scan_results.html .
```
-
    - Open the `giskard_scan_results.html` in a browser and you should see a report such as in the image below.

![Giskard report](/assets/img/giskard_report.PNG "Giskard report")


<br> 

> [!IMPORTANT] 
>**OBJECTIVE:** Try to conduct the Giskard Scan on some other LLM available in the [Ollama library](https://ollama.com/library). You need to download & run the LLM inside the **ollama** container, and change the `MODEL` parameter in `giskard/llm_scan.py` file accordingly (the Giskard Scan might take quite a long time, so it is recommended to do this last).
>

<br><br>

# <p align="center">Editing files inside a container</p>  <a name="editfile"></a>

The **llm_hackathon** container includes [nano](https://www.nano-editor.org/dist/latest/cheatsheet.html) text editor. You can start editing `llm_scan.py` file while connected to the container's shell with the command: 
```console
  nano giskard/llm_scan.py
```

<br><br>
# <p align="center">Using a LLM via REST API</p>  <a name="restllm"></a>
After setting up the environment, you can also generate responses and chat with the model via REST API. The file `chat_api_template.py` contains a template for generating responses to custom prompts. 

For more information, please visit: https://github.com/ollama/ollama/blob/main/docs/api.md


<br><br><br><br><br>
# <p align="center">Useful resources</p> <a name="resources"></a>

[Ollama model library](https://ollama.com/library)

[Garak ReadMe](https://github.com/leondz/garak?tab=readme-ov-file)  
[Garak Documentation](https://docs.garak.ai/garak)  
  
[Giskard ReadMe](https://github.com/Giskard-AI/giskard)  
[Giskard Documentation](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html)  

[DependencyCheck ReadMe](https://github.com/jeremylong/DependencyCheck/blob/main/README.md)  
[DependencyCheck Documentation](https://jeremylong.github.io/DependencyCheck/)  
[DependencyCheck CLI Arguments](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/arguments.html)  
[DependencyCheck Supported File Types](https://jeremylong.github.io/DependencyCheck/analyzers/index.html)  
