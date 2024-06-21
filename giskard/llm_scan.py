import os
import requests
import json

import pandas as pd
#from openai import OpenAI
import giskard
#from giskard.llm.client.openai import OpenAIClient


# Setup the Ollama client with API key and base URL


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
        "model": "phi3",
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
            print("Error:", response.status_code, response.text)

    print(f"outputs:\n\n{outputs}\n\n")
    return outputs

# Create a giskard.Model object. Don’t forget to fill the `name` and `description`
# parameters: they will be used by our scan to generate domain-specific tests.
giskard_model = giskard.Model(
    model=model_predict,  # our model function
    model_type="text_generation",
    name="Phi 3",
    description="Standard Phi 3 model from Microsoft.",
    feature_names=["prompt"],  # input variables needed by your model
)
data ={'prompt': ["Tell me about yourself.", "Can you describe a tomato for me?"]}
df = pd.DataFrame(data)
print(f"df:\n\n{df}\n\n")

test = model_predict(df)
scan = 0 #TODO: FIGURE OUT THE UP-TO-DATE syntax for generating scan from own dataset
scan_results = giskard.scan(giskard_model)
scan_results.to_html("model_scan_results.html")