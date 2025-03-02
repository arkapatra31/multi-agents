from langchain.tools import tool
from langchain_community.tools import TavilySearchResults


@tool
def search_hotels_tool(query: str) -> str:
    """
    Search for hotels based on user query which includes location, date, time.
    Searches hotel information using Tavily search engine and returns relevant results.
    """
    search = TavilySearchResults(max_results=10, verbose=True)
    results = search.run(tool_input=query)
    return results


__all__ = [search_hotels_tool]
