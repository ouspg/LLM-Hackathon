# OUSPG LLM Hackathon

# Quickstart

## Prerequisites

- Install `Docker` and have it running.
- Make sure port **11434** is not in use by your local machine.
  - On **Linux** you can check ports that are in use with: `lsof -i -P -n | grep LISTEN`
- ~20Gb of disk space

## Setup

### Step 1

- Clone this repository to your local machine with `git clone https://github.com/Zippo00/LLM_Hackathon.git`
- Build the Docker containers with `docker compose up`
- Exit the ollama container with `Ctrl + C`

### Step 2

- Start the ollama container with `docker container start ollama`
- Download & run a desired LLM with ollama *(replace `phi3` with the desired LLM tag; available models can be found from https://ollama.com/library)*: `docker exec -it ollama ollama run phi3`
- After downloading the model, you should be [TODO: Add illustration here**] able to chat with the model. Type `/bye` to leave the interactive mode.

### Step 3

- Start the llm-hackathon container with: `docker container start llm_hackathon`
- Connect to the container's shell with: `docker exec -ti llm_hackathon sh` 

If you see [TODO: Add illustration here] `root@2c77651e2bcf:/home/ubuntu#` in your terminal - Congratulations! You have succesfully completed the setup part.

## Usage

The llm-hackathon container includes [Garak](https://docs.garak.ai/garak) and [Giskard](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html) LLM vulnerability tools.

### Giskard

- Use command `ls` to make sure there is a directory labeled "giskard" in your current directory.[TODO: Add illustration here**]
- If there is, you can check the contents of the "giskard" directory with `ls giskard`.
- The Python file `llm_scan.py` contains a Python script that runs a Giskard LLM scan on the LLM previously downloaded to the "ollama" container (Default: phi3, you need to change `MODEL` parameter in `llm_scan.py` if you selected a different model).
- You can define a custom dataset that will be used to evaluate the LLM by altering the `custom dataset` parameter in the `llm_scan.py` file.
- You can start the Giskard LLM Scan with `python3 giskard/llm_scan.py`
- After the scan is complete, the Giskard tool will generate an evaluation report into the current directory labeled `giskard_scan_results.html`.
- You can copy the results file to your local host machine and explore the report in browser:
  - Exit the container with command `exit` or by pressing `Ctrl + D`
  - Run command `docker cp llm_hackathon:/home/ubuntu/giskard_scan_results.html .`
  - Open the `giskard_scan_results.html` in a browser. [TODO: Add illustration here**] 

**Note:** Running the Giskard LLM Scan can take up to an hour or several hours based on the computation power the LLM is being run on and the size on the dataset used to evaluate the LLM. This repository contains an example evaluation report in the giskard directory labeled `model_scan_results.html` that was produced after running the scan on Phi-3-Mini model using the default custom dataset found in `llm_scan.py`. You can open this `html` file within your browser, and explore what kind of a report the tool would produce after running the whole scan.
  

### Garak

If you aren't already connected to the **llm_hackathon** container's shell, do so with the command `docker exec -ti llm_hackathon sh`. 

You can now use [Garak](https://docs.garak.ai/garak) via the shell. To list different available Garak probes [Add illustration here**], type:   
```console
  python3 -m garak --list_probes
```
You can run the probes on all available models in [Hugging Face Models](https://huggingface.co/models) (some require authentication and more computation power than others). For example, to run `malware.Evasion` probe on OpenAI's `GPT-2`, use the command:
```console
  python3 -m garak --model_type huggingface --model_name gpt2 --probes malwaregen.Evasion
```


## TODO: 
- Giskard Scan takes 1hr+ (Phi3; No GPU). Is it possible to select only part scan?
   - A lot of the Giskard Scans failed due to "TypeError: list indices must be integers or slices, not str". Any known fixes?
- Write documentations on how to operate them (with examples).
- Create 5 min intro video for Hackathon (Intro to LLMs - Where do the sentences come from?)

  **Running a Garak probe in the container taking 10min+ with GPT-2, why?

## Notes

### Garak Commands: 

- List available probes:
  ```console
  python3 -m garak --list_probes
  ```

- Run malware.Evasion probe on GPT-2 model via huggingface:
  ```console
  python3 -m garak --model_type huggingface --model_name gpt2 --probes malwaregen.Evasion
  ```  

### Useful resources:

- [Garak ReadMe](https://github.com/leondz/garak?tab=readme-ov-file)
- [Garak Documentation](https://docs.garak.ai/garak)
  
- [Giskard ReadMe](https://github.com/Giskard-AI/giskard)
- [Giskard Documentation](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html)
