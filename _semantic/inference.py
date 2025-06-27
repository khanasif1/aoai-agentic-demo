import requests
import json
import time
from datetime import datetime, timezone

def ollama_infer(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    prompt = f"{prompt}.\n Summarize the response in 150 words or less."
    print(f"Ollama prompt: {prompt}")
    payload = {"model": model, "prompt": prompt}
    # Print UTC time
    utc_start = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"Ollama start time (UTC): {utc_start}")
    response = requests.post(url, json=payload, stream=True)
    print(f"Ollama response status code: {response.content}")
    if response.ok:
        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    result += data.get("response", "")
                    # print(f"Ollama response: {result}")
                except Exception as e:
                    print(f"Ollama stream error: {e}")
        utc_end = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        print(f"Ollama end time (UTC): {utc_end}")
        return result if result else "No response from model."
    else:
        return f"Ollama error: {response.status_code}"