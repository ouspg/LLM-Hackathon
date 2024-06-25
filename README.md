# LLM_Hackathon
Repository for OUSPG LLM Hackathon.

## Quickstart

### Prerequisites

- Install Docker and have it running.
- Make sure port 11434 is not in use by your local machine.
  On Linux you can check ports that are in use with: `sudo lsof -i -P -n | grep LISTEN`
- ~20Gb of disk space

### Step 1

- Clone this repository to your local machine with `git clone `

## TODO: 
- Giskard Scan takes 1hr+ (Phi3; No GPU). Is it possible to select only part scan?
   - A lot of the Giskard Scans failed due to "TypeError: list indices must be integers or slices, not str". Any known fixes?
- Write documentations on how to operate them (with examples).
- Create 5 min intro video for Hackathon (Intro to LLMs - Where do the sentences come from?)

  **Running a Garak probe in the container taking 10min+ with GPT-2, why?

## Notes

### Docker Commands:

- Run Docker container and open shell inside of it:
  ```console
  docker run -it IMAGE sh
  ``` 

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
- [Giskard ReadMe](https://github.com/Giskard-AI/giskard)
