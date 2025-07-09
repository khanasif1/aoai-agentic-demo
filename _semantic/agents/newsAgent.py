import asyncio
import sys
import os
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugin.technewsplugin import technewsplugin


from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

azure_endpoint = os.getenv("azure_endpoint")
api_version = os.getenv("api_version")
deployment_name = os.getenv("deployment_name")
source_websidte = os.getenv("source_websidte")    

async def main():
   technews = technewsplugin(source_websidte)
   # Initialize the kernel
   kernel = Kernel()
   print(f"Crawel Website: {source_websidte}") 
    # Entra ID authentication               
    
   try:  
        print("Get Credentials")   
        _credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
       
        token = _credential.get_token("https://api.applicationinsights.io/.default")
        # print(f"Using Entra ID authentication : {token}")
        print(f"env: {azure_endpoint} - {deployment_name}")
        # Add Azure OpenAI chat completion
        chat_completion = AzureChatCompletion(
            deployment_name=deployment_name,      
            base_url=azure_endpoint,
            credential=_credential,
            # api_key=''        
            # ad_token=token
        )
   except Exception as e:
        print("Error in authentication: ", e)                
        exit()


   kernel.add_service(chat_completion)

   # Add a plugin 
   kernel.add_plugin(
      technewsplugin(source_websidte),
      plugin_name="TechNews_Plugin",
   )

   # Enable planning
   execution_settings = AzureChatPromptExecutionSettings()
   execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

   # Create a history of the conversation
   history = ChatHistory()
   history.add_message({"role": "user", "content": "Get the latest news from techcrunch"})
   userInput = None
   while True:
        # Collect user input
        userInput = input("User > ")
        # Add user input to the history
        history.add_user_message(userInput)

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break
           # Get the response from the AI
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )
        
        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)           


   
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())    