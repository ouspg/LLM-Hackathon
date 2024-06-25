# <p align="center">OUSPG LLM Hackathon Environment</p>

# <p align="center">Quickstart</p>

## <p align="center">Prerequisites</p>

- Install `Docker` and have it running.
- Make sure port **11434** is not in use by any program.
  - On **Linux** you can check ports that are in use with: `lsof -i -P -n | grep LISTEN`
  - On **Windows** you can check ports that are in use with: `netstat -bano`
  - On **MacOS** `lsof -i -P -n | grep LISTEN` or `netstat -pan` *may* work.
- ~20Gb of disk space.



## <p align="center">Setup</p>

### Step 1

- Clone this repository to your local machine with: `git clone https://github.com/Zippo00/LLM_Hackathon.git`
- Navigate to the repository with: `cd LLM_Hackathon`
- Build the Docker containers with: `docker compose up`
- You may automatically get stuck inside the **ollama** container. Exit it with: `Ctrl + C`

### Step 2

- Start the **ollama** container with: `docker container start ollama`
- Download & run Microsoft's Phi-3-Mini model inside the **ollama** container with ollama: `docker exec -it ollama ollama run phi3`
  - *You can use any other LLM from [Ollama Library](https://ollama.com/library) as well. Just replace the `phi3` in the above command with the corresponding LLM tag.*
- After downloading the model, you should be able to chat with the model [TODO: Add illustration here**]. Type `/bye` to leave the interactive mode.

### Step 3

- Start the **llm-hackathon** container with: `docker container start llm_hackathon`
- Connect to the container's shell with: `docker exec -ti llm_hackathon sh` 

If you see [TODO: Add illustration here] `root@2c77651e2bcf:/home/ubuntu#` in your terminal - Congratulations! You have succesfully completed the setup part.




## <p align="center">Usage</p>

The **llm-hackathon** container includes [Garak](https://docs.garak.ai/garak) and [Giskard](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html) LLM vulnerability tools.


### Giskard
If you aren't already connected to the **llm_hackathon** container's shell, do so with the command `docker exec -ti llm_hackathon sh`. 

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

**Note:** Running the Giskard LLM Scan can take up to an hour or several hours based on the computation power the LLM is being run on and the size on the dataset used to evaluate the LLM. This repository contains an example evaluation report in the giskard directory labeled `giskard/model_scan_results.html` that was produced after running the scan on Phi-3-Mini model using the default custom dataset found in `llm_scan.py`. You can open this `html` file within your browser, and explore what kind of a report the tool would produce after running the whole scan.
  

### Garak

If you aren't already connected to the **llm_hackathon** container's shell, do so with the command `docker exec -ti llm_hackathon sh`. 

You can now use [Garak](https://docs.garak.ai/garak) via the shell. To list different available Garak probes [Add illustration here**], type:   
```console
  python3 -m garak --list_probes
```

You can run the probes on all available models in [Hugging Face Models](https://huggingface.co/models) (some require authentication and more computation power than others). For example, to run `malwaregen.Evasion` probe on OpenAI's `GPT-2`, use the command:
```console
  python3 -m garak --model_type huggingface --model_name gpt2 --probes malwaregen.Evasion
```

After garak has ran it's probe(s), it will generate reports into `garak_runs` directory. 
You can copy the reports to your local host machine and explore the `html` report in browser:
  - Exit the container with command `exit` or by pressing `Ctrl + D`
  - Run command `docker cp llm_hackathon:/home/ubuntu/garak_runs/ .`
  - Explore the report files. [TODO: Add illustration here**] 




## <p align="center">TODO:</p>
- Giskard Scan takes 1hr+ (Phi3; No GPU). Is it possible to select only part scan?
   - A lot of the Giskard Scans failed due to "TypeError: list indices must be integers or slices, not str". Any known fixes?
- Write documentations on how to operate them (with examples).
- Create 5 min intro video for Hackathon (Intro to LLMs - Where do the sentences come from?)

  **Running a Garak probe in the container taking 10min+ with GPT-2, why?

### Useful resources:

[Garak ReadMe](https://github.com/leondz/garak?tab=readme-ov-file)  
[Garak Documentation](https://docs.garak.ai/garak)  
  
[Giskard ReadMe](https://github.com/Giskard-AI/giskard)  
[Giskard Documentation](https://docs.giskard.ai/en/stable/open_source/scan/scan_llm/index.html)  
