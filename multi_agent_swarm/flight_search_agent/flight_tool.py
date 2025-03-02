from langchain.tools import tool
from langchain_community.tools import TavilySearchResults

@tool
def search_flights_tool(query: str) -> str:
    """Search for flights based on user query and return results.
    Searches flight information using Tavily search engine and returns relevant results.
    """
    search = TavilySearchResults(max_results= 10, verbose= True)
    results = search.run(tool_input=query)
    return results

__all__ = [search_flights_tool]