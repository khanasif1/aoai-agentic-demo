import asyncio
from crawl4ai import AsyncWebCrawler

from .inferenceplugin import azure_openai_infer

from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator  import kernel_function



# from plugin.inferenceplugin import azure_openai_infer

class technewsplugin():
    def __init__(self, url):
        self._url = url
        print("Loading technewsplugin") 
             
    # name='techcrunch news crawler',
    @kernel_function(description='This function crawl the technology websidte to get latest news from techcrunch')   
    async def techcrunchNews(self):
        """This function crawl the technology websidte to get latest news from techcrunch"""
        print("********************************")
        print("******TECHCRUNCH CRAWLING STARTED*********")
        print("********************************") 
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=self._url,          
                selector="ul.wp-block-post-template.is-layout-flow.wp-block-post-template-is-layout-flow"
            )
            
            # print(result.markdown) 
            print("********************************")
            print("******TECHCRUNCH CRAWLING COMPLETE*********")
            print("********************************") 
            return result.markdown  
            # print("Call analyze_techcrunch_articles")
            # analyzed_articles = analyze_techcrunch_articles(result.markdown)
            # print(f"Analyzed articles: {analyzed_articles}")
            
    # @kernel_function        
    # def analyze_techcrunch_articles(articles):
    #     summaries = []
    #     print(f"Analyzing {len(articles)} articles...")

    #     prompt = f"""
    #     Html Content: {articles}
        
    #     Please provide a brief summary of what each article is about and why it might be interesting.
    #     Generate responde in json formate with attributes as title, summary and article image.
        
    #     """        

    #     summary = azure_openai_infer(prompt)
    #     print("Got summary from azure openai")

    #     print(f"Summary: {summary}")
        
    #     return summaries