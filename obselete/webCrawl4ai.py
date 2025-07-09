import asyncio
from crawl4ai import AsyncWebCrawler
import requests
from inference import azure_openai_infer


def ollama_infer(prompt, model="mistral"):

   try:
       print(f"Ollama prompt: {prompt}")
    #    url = "http://20.70.144.241:11434/api/generate"
       url = "http://localhost:11434/api/generate"
       data = {
        "model": model,
        "prompt": prompt,
        "stream": False
        }
       
       response = requests.post(url, json=data)
       if response.status_code == 200:
            return response.json()["response"]
       else:
            return f"Error: {response.status_code} - {response.text}"
   except Exception as e:
        return f"Error: {str(e)}"


        
def analyze_techcrunch_articles(articles):
    summaries = []
    print(f"Analyzing {len(articles)} articles...")

    prompt = f"""
    Html Content: {articles}
       
    Please provide a brief summary of what each article is about and why it might be interesting.
    Generate responde in json formate with attributes as title, summary and article image.
    
    """
    
    # summary = ollama_infer(prompt)
    summary = azure_openai_infer(prompt)
    print("Got summary from azure openai")

    print(f"Summary: {summary}")
    
    return summaries

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://techcrunch.com/",
            #  selector=".river--homepage .post-block__title a"
             selector="ul.wp-block-post-template.is-layout-flow.wp-block-post-template-is-layout-flow"
        )

        print(result.markdown)    
        print("Call analyze_techcrunch_articles")
        analyzed_articles = analyze_techcrunch_articles(result.markdown)
        print(f"Analyzed articles: {analyzed_articles}")

if __name__ == "__main__":
    print("*********Start*********")
    asyncio.run(main())
    print("*********End*********")
    # summary = azure_openai_infer("Tell me about world?")
    # print(f"Summary: {summary}")