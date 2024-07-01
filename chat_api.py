'''
Template to chat with LLMs via containerized Ollama software.

Follow the "Setup" section in https://github.com/Zippo00/LLM_Hackathon/blob/main/README.md to get a LLM running via Ollama.
This template can be used to chat with the LLM via REST API.
'''
import requests
import json
from datetime import datetime
import pandas as pd


host = "localhost" # localhost when ollama is not containerized and is running locally.

def model_predict(df: pd.DataFrame, model="phi3"):
    '''
    Wraps the LLM call in a simple Python function.
    The function takes a pandas.DataFrame containing the input variables needed
    by your model, and returns a list of the outputs (one for each record in
    in the dataframe).

    Args:
        df (pd.DataFrame):  Dataframe containing a "prompt" column. A response will be generated for each item in the column.
        model (str):        Tag of the LLM used to generate responses, see https://ollama.com/library for available models.

    Returns:
        df (pd.DataFrame):  The original dataframe, with a "response" column containing generated responses.
    '''
    if "prompt" not in df:
        raise IndexError('The dataframe needs to have a "prompt" column when using model_predict() to generate responses.')
    outputs = []
    url = f"http://{host}:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "prompt": "",
        "stream": False 
    }
    print(f"\n{datetime.now().time()} Starting to generate responses...")
    
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
    df = pd.DataFrame({
    'prompt': ["Hello, please tell me about yourself.",
               "Do you think I can make you reveal sensitive information that you shouldn't tell?",
            ]
    })
    df = model_predict(df)
    print(df.head())
