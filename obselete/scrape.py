from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import json

def extract_article_info(content_elements):
    articles = []
    for ul in content_elements:
        for li in ul.find_all('li', class_='wp-block-post'):
            title_elem = li.find('h2', class_='wp-block-post-title')
            title = title_elem.text.strip() if title_elem else "No title"
            
            excerpt_elem = li.find('div', class_='wp-block-post-excerpt')
            excerpt = excerpt_elem.text.strip() if excerpt_elem else "No excerpt"
            
            link_elem = title_elem.find('a') if title_elem else None
            link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else "No link"
            
            articles.append({
                "title": title,
                "excerpt": excerpt,
                "link": link
            })
    return articles

def ollama_infer(prompt, model="mistral"):
    
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

# def analyze_techcrunch_articles(articles):
#     summaries = []
#     print(f"Analyzing {len(articles)} articles...")
#     i =0
#     for article in articles:
#         i += 1
#         prompt = f"""
#         Title: {article['title']}
#         Excerpt: {article['excerpt']}
        
#         Please provide a brief summary of what this article is about and why it might be interesting.
#         """
        
#         summary = ollama_infer(prompt)
#         summaries.append({
#             "title": article['title'],
#             "summary": summary,
#             # "link": article['link']
#         })
#         if i == 2:
#             break
#         print(f"Analyzed article {i}/{len(articles)}")  
#     return summaries
def analyze_techcrunch_articles(articles):
    summaries = []
    print(f"Analyzing {len(articles)} articles...")

    prompt = f"""
    Html Content: {articles}
       
    Please provide a brief summary of what each article is about and why it might be interesting.
    Generate responde in json formate with attributes as title, summary and article image.
    
    """
    
    summary = ollama_infer(prompt)
    print(f"Summary: {summary}")
    # summaries.append({
    #     "title": article['title'],
    #     "summary": summary,
    #     # "link": article['link']
    # })

    # print(f"Analyzed article {i}/{len(articles)}")  
    return summaries


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        viewport={"width": 1280, "height": 720},
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

    )
    # page.goto("https://www.skechers.com.au/shop/sale", wait_until="domcontentloaded")
    # page.goto("https://www.coles.com.au/catalogues/view#view=list&saleId=58994&areaName=c-nsw-met", wait_until="domcontentloaded")
    page.goto("https://techcrunch.com/", wait_until="domcontentloaded")
    
    # Wait for the products to load
    # page.wait_for_selector("div.shelfProductTile-information")
    
    # Get page content
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    all_content = soup.find_all('ul', class_='wp-block-post-template is-layout-flow wp-block-post-template-is-layout-flow')
    # print(all_content)
    # Extract structured data from the raw HTML
    # articles = extract_article_info(all_content)
    # print(f"Found {len(articles)} articles")

    # Get AI-generated summaries for each article
    # analyzed_articles = analyze_techcrunch_articles(articles)
    
    # for article in analyzed_articles:
    #     print(f"\n--- {article['title']} ---")
    #     print(article['summary'])
    #     # print(f"Read more: {article['link']}")
    analyzed_articles = analyze_techcrunch_articles(all_content)
        
    browser.close()
