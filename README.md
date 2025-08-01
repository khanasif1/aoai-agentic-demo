# autogen-agentic-demo
autogen-demo

## Run Solution

- python -m venv .venv
- .\.venv\Scripts\activate.ps1
- cd <path>\aoai-agentic-demo\_semantic 
- python .\agents\newsAgent.py

---

## Architecture Diagram

```mermaid
flowchart TD
    UserInput((User Input))
    AO[Agent Orchestrator\n(_semantic/agentOrchestrator.py)]
    TechAgent[Tech News Agent\n(_semantic/agents/technewsAgent.py)]
    CurrentNewsAgent[Current News Agent\n(_semantic/agents/currentewsAgent.py)]
    TechPlugin[Tech News Plugin\n(_semantic/plugin/technewsplugin.py)]
    CurrentPlugin[Current News Plugin\n(_semantic/plugin/currentnewsplugin.py)]
    InferencePlugin[Inference Plugin\n(_semantic/plugin/inferenceplugin.py)]
    AzureOpenAI[(Azure OpenAI Service)]
    WebCrawl[Async Web Crawler]

    UserInput-->|input|AO
    AO-->|orchestrates|TechAgent
    AO-->|orchestrates|CurrentNewsAgent
    TechAgent-->|uses|TechPlugin
    CurrentNewsAgent-->|uses|CurrentPlugin
    TechPlugin-->|calls|WebCrawl
    CurrentPlugin-->|calls|WebCrawl
    TechPlugin-->|calls|InferencePlugin
    CurrentPlugin-->|calls|InferencePlugin
    InferencePlugin-->|API call|AzureOpenAI
```

### Explanation
- **User Input**: The entry point where a user provides a prompt or query.
- **Agent Orchestrator**: Coordinates between multiple agents (tech and current news agents), manages runtime and orchestration.
- **Agents**: Each agent (Tech News, Current News) is responsible for a specific domain. They utilize plugins to fetch and process data.
- **Plugins**: Encapsulate the logic for crawling the web (using `AsyncWebCrawler`) and for accessing inference models (Azure OpenAI, Ollama, etc.).
- **Inference Plugin**: Handles calls to external inference services like Azure OpenAI for summarization or response generation.
- **External Services**: Azure OpenAI and web sources are accessed via plugins for data retrieval and AI-powered processing.

This modular architecture enables easy extension (e.g., adding new agents or plugins), robust orchestration, and clear separation of concerns.

---