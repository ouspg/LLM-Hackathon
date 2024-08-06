'''
Template to chat with LLMs via containerized Ollama software.

Follow the "Setup" section in https://github.com/Zippo00/LLM_Hackathon/blob/main/README.md to get a LLM running via Ollama.
This template can be used to generate responses from the LLM via REST API.
'''
import requests
import json
from datetime import datetime
import pandas as pd


def model_predict(df: pd.DataFrame, model="phi3", ctx_size=2048, url="http://localhost:11434/api/generate"):
    '''
    Wraps the LLM call in a simple Python function.
    The function takes a pandas.DataFrame containing the input variables needed
    by your model, and returns a list of the outputs (one for each record in
    in the dataframe).

    Args:
        df (pd.DataFrame):  Dataframe containing a "prompt" column. A response will be generated for each item in the column.
        
    Kwargs:
        model (str):        Tag of the LLM used to generate responses, see https://ollama.com/library for available models.
        ctx_size (int):     LLM context window size in tokens.
        url (string):       POST requests are sent to this URL.

    Returns:
        df (pd.DataFrame):  The original dataframe, with a "response" column containing generated responses.
    '''
    if "prompt" not in df:
        raise IndexError('The dataframe needs to have a "prompt" column when using model_predict() to generate responses.')
    outputs = []
    url = url
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "prompt": "",
        "options": {
            "num_ctx": ctx_size
        },
        "stream": False 
    }
    print(f"\n{datetime.now().time().replace(microsecond=0)} - Starting to generate responses...")
    
    for question in df["prompt"].values:
        data["prompt"] = question
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_text = response.text
            output_data = json.loads(response_text)
            outputs.append(output_data["response"])
        else:
            print("Error in POST response:", response.status_code, response.text)
    df["response"] = outputs

    return df


if __name__=="__main__":
    # Example of usage:
    df = pd.DataFrame({
    'prompt': ["Hello, please tell me about yourself.",
               "Do you think I can make you reveal sensitive information that you shouldn't tell?",
            ]
    })
    df = model_predict(df)
    print(df.head())
