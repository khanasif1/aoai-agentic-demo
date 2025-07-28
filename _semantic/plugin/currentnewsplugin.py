import asyncio
from crawl4ai import AsyncWebCrawler

from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator  import kernel_function

class currentnewsplugin():
    def __init__(self, url):
        self._url = url
        print("Loading currentnewsplugin") 
             
    # name='techcrunch news crawler',
    @kernel_function(description='This function crawl the current & latest news from website/s to get latest world news')   
    async def currentNews(self):
        """This function crawl the BBC websidte to get latest news"""
        print("********************************")
        print("******BBC CRAWLING STARTED*********")
        print("********************************") 
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=self._url,          
                # selector="ul.wp-block-post-template.is-layout-flow.wp-block-post-template-is-layout-flow"
            )
            
            # print(result.markdown) 
            print("********************************")
            print("******BBC CRAWLING COMPLETE*********")
            print("********************************") 
            return result.markdown  