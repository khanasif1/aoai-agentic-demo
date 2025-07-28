import asyncio
import sys
import os
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import Agent, ChatCompletionAgent
from semantic_kernel import Kernel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugin.technewsplugin import technewsplugin


from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

azure_endpoint = os.getenv("azure_endpoint")
api_version = os.getenv("api_version")
deployment_name = os.getenv("deployment_name")
source_websidte = os.getenv("source_websidte")    

class technewsagent():
    def __init__(self, url):
        self._url = url
        print("Loading technewsagent") 

    async def get_technewsagent()-> list[Agent]:        
    # Initialize the kernel
        kernel = Kernel()
        print(f"Crawel Website: {source_websidte}") 
        # Entra ID authentication               
        
        try:  
                print("Get Credentials")   
                
                token_provider = get_bearer_token_provider(
                DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default"  # The scope for Azure OpenAI Service
                )
                print(f"env: {azure_endpoint} - {deployment_name}")
                # Add Azure OpenAI chat completion
                technews_chat_completion = AzureChatCompletion(
                    deployment_name=deployment_name,      
                    endpoint=azure_endpoint,
                    ad_token_provider=token_provider,
                    service_id="azure_open_ai",
                )
        except Exception as e:        
                print("Error in authentication: ", e)                
                exit()
        # Add a plugin 
        kernel.add_plugin(
            technewsplugin(source_websidte),
            plugin_name="TechNews_Plugin"
            )   
        technews_agent = ChatCompletionAgent(
                                        name="TechNew",
                                        instructions="You are an agent to extract technology new.",
                                        service= technews_chat_completion,
                                        kernel=kernel
                                    )
        return technews_agent
        
    