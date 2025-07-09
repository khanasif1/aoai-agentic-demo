import os
import json
import time
import requests
from datetime import datetime, timezone
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from dotenv import load_dotenv

load_dotenv()

def azure_openai_infer(prompt, model="gpt-4.1"):
    """
    Use Azure OpenAI GPT-4.1 model to process data with Entra ID authentication
    
    Args:
        prompt (str): The input prompt to send to the model
        model (str): The model name (default: gpt-4o for GPT-4.1)
        max_tokens (int): Maximum tokens for the response
    
    Returns:
        str: The model's response or error message
    """
    print("*********Start azure_openai_infer*********")
    # Azure OpenAI configuration
    azure_endpoint = os.getenv("azure_endpoint")
    api_version = os.getenv("api_version")
    
    if not azure_endpoint:
        return "Error: Azure OpenAI endpoint not found. Please set AZURE_OPENAI_ENDPOINT environment variable."

        
    try:
        # Initialize Azure credential for Entra ID authentication
        # Try different authentication methods in order of preference
        
        # Entra ID authentication               
        
        try:        
            _credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
            token = _credential.get_token("https://api.applicationinsights.io/.default").token
            # print(f"Using Entra ID authentication : {token}")
            client = ChatCompletionsClient(
                endpoint=azure_endpoint,
                credential=_credential,
                credential_scopes=["https://cognitiveservices.azure.com/.default"],
                api_version=api_version
            )
        except Exception as e:
            print("Error in authentication: ", e)                
            exit()
        
        # Prepare the prompt
        enhanced_prompt = f"{prompt}.\n Summarize the response in 150 words or less."
        print(f"Azure OpenAI prompt: {enhanced_prompt}")
        
        # Print UTC time
        utc_start = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        print(f"Azure OpenAI start time (UTC): {utc_start}")
        
        # Make the API call
        response = client.complete(
                messages=[
                    SystemMessage("You are a helpful assistant."),
                    UserMessage(prompt),
                ]
            )  
        
        # Extract the response
        result = response.choices[0].message.content if response.choices else "No response from model."
        
        utc_end = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        print(f"Azure OpenAI end time (UTC): {utc_end}")
        print(f"Azure OpenAI response: {result}")
        
        return result
        
    except Exception as e:
        error_msg = f"Azure OpenAI error: {str(e)}"
        print(error_msg)
        return error_msg

def ollama_infer(prompt, model="llama2"):
    """
    Legacy Ollama inference function - kept for backward compatibility
    """
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