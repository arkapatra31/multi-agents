from langchain_community.tools import TavilySearchResults
from langchain.tools import Tool

# Create a search tool using TavilySearchResults
search = TavilySearchResults(max_results=4)

# Create a LangChain Tool using the search
research_tool = Tool(
    name="Search",
    func=search.invoke,
    description="Search the internet for information about Python problems or concepts. Input should be a search query.",
)
