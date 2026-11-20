from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print


#tavily tools
tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """Search the web for recent and relible information on a topic . Returns Titles,URLS AND snippets"""

    results=tavily.search(query=query,max_results=5)
    out=[]

    for r in results['results']:
        out.append(
        f"Title: {r['title']}\n"
        f"URL: {r['url']}\n"
        f"Snippet: {r['content'][:300]}"
    )
    return "\n-----\n".join(out)

# print(web_search.invoke("what is the recent news of war"))

    # return result
    # print(web_s earch.invoke("what are the recent news of war?"))
    
@tool
def scrape_url(url: str) -> str:
    """Scrape content from a given URL using BeautifulSoup. Returns the page text content."""
    try:
        response = requests.get(url, timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        # response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for tag in soup(["script", "style","nav,","footer"]):
            tag.decompose()

            return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Error scraping URL: {str(e)}"


# print(scrape_url.invoke("https://timesofindia.indiatimes.com/sports/cricket/news/when-ms-dhoni-stepped-away-virat-kohli-ravi-shastri-toughened-up-indian-cricket-ajinkya-rahane/articleshow/132913800.cms"))   
        
       






