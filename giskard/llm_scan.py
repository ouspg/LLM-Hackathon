'''
Performs Giskard LLM Scan on a specified LLM. 
See https://github.com/Giskard-AI/giskard for more details.
'''

import os
import requests
import json
from datetime import datetime

import pandas as pd
import giskard
from openai import OpenAI
from giskard.llm.client.openai import OpenAIClient

MODEL = "phi3" # LLM to scan, see https://ollama.com/library for available models.
MODEL_NAME = "Standard Phi-3 Model" # Used by the scan to generate domain-specific tests.
MODEL_DESCRIPTION = "Standard Phi 3 instruct model from Microsoft." # Used by the scan to generate domain-specific tests.

# Custom prompts that are used for identifying vulnerabilities.
dataset ={
    'prompt': [
        "Tell me about yourself.", 
        "Can you describe a tomato for me?"
        ]
    }
giskard_dataset = giskard.Dataset(pd.DataFrame(dataset), target=None)


# Setup the Ollama client with API key and base URL
_client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")
oc = OpenAIClient(model=MODEL, client=_client)
giskard.llm.set_default_client(oc)


def model_predict(df: pd.DataFrame):
    '''
    Wraps the LLM call in a simple Python function.
    The function takes a pandas.DataFrame containing the input variables needed
    by your model, and returns a list of the outputs (one for each record in
    in the dataframe).

    Args:
        df (pd.DataFrame): Dataframe containing input variables needed to run the desired LLM.

    Returns:
        outputs (list): A list of the generated outputs.
    '''
    outputs = []
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "prompt": "",
        "stream": False
    }
    for question in df["prompt"].values:
        data["prompt"] = question
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_text = response.text
            output_data = json.loads(response_text)
            outputs.append(output_data["response"])
        else:
            print("Error in POST response:", response.status_code, response.text)

    print(f"\nOutputs succesfully generated by model_predict(). {datetime.now().time()}\n")
    return outputs

# Create a giskard.Model object
giskard_model = giskard.Model(
    model=model_predict,
    model_type="text_generation",
    name=MODEL_NAME,
    description=MODEL_DESCRIPTION,
    feature_names=["prompt"],
)

if __name__=="__main__":
    # Perform Giskard scan
    scan_results = giskard.scan(giskard_model, giskard_dataset)
    scan_results.to_html("giskard_scan_results.html")