import asyncio
import sys
import os
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.agents import ConcurrentOrchestration

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.technewsAgent import technewsagent
from agents.currentewsAgent import currentnewsagent

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

azure_endpoint = os.getenv("azure_endpoint")
api_version = os.getenv("api_version")
deployment_name = os.getenv("deployment_name")
source_websidte = os.getenv("source_websidte")    

async def main():
    

    tech_agent = await technewsagent.get_technewsagent()
    currentnews_agent = await currentnewsagent.get_currentnewsagent()
    
    agents = [tech_agent,currentnews_agent]
    # agents = [currentnews_agent]
    # 1. Create a concurrent orchestration with multiple agents
   
    concurrent_orchestration = ConcurrentOrchestration(members=agents)
   
    # 2. Create a runtime and start it
    runtime = InProcessRuntime()
    runtime.start()   

    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break
        # 3. Invoke the orchestration with a task and the runtime
        orchestration_result = await concurrent_orchestration.invoke(
            # task="What is latest technology news from techcrunch? What is latest current news from BBC?",
            task=userInput,
            runtime=runtime,
        ) 
    
        # 4. Wait for the results
        # Note: the order of the results is not guaranteed to be the same
        # as the order of the agents in the orchestration.
        value = await orchestration_result.get(timeout=600)
        for item in value:
            print(f"#Agent Response > {item.name}: {item.content}")

        
        
    # # Create a history of the conversation
    # history = ChatHistory()
    # history.add_message({"role": "user", "content": "Get the latest news from techcrunch"})
    # userInput = None
    # while True:
    #     # Collect user input
    #     userInput = input("User > ")
    #     # Add user input to the history
    #     history.add_user_message(userInput)

    #     # Terminate the loop if the user says "exit"
    #     if userInput == "exit":
    #         break
    #         # Get the response from the AI
    #     result = await chat_completion.get_chat_message_content(
    #         chat_history=history,
    #         settings=execution_settings,
    #         kernel=kernel,
    #     )
            
    #     # Print the results
    #     print("Assistant > " + str(result))

    # # Add the message from the agent to the chat history
    # history.add_message(result)           


   
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())    