# LLM_Hackathon
Repository for OUSPG LLM Hackathon.
## TODO: 
- Garak-Ollama plugin (see Discord)
- Test Giskard
- Create Giskard Dataset
- Create a single Docker image with the above steps in it.
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
 python3 -m garak --model_type huggingface --model_name gpt2 --probes        
malwaregen.Evasion
  ```

### Useful resources:

- [Garak ReadMe](https://github.com/leondz/garak?tab=readme-ov-file)
- [Giskard ReadMe](https://github.com/Giskard-AI/giskard)
