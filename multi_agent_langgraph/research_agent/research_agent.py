from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from .research_tool import research_tool

load_dotenv()


def run_research_agent(agent_state):
    # Create the prompt template with the system message and agent_scratchpad
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Python research assistant. Your task is to search for simple Python problems or questions. When you find a problem, format it nicely and present it to the user. To search for information, use the search tool provided to you.",
            ),
            ("human", "Here is the query regarding the Python problem: {query}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

    # Create the tools list with our search tool
    tools = [research_tool]

    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Run the research agent with the given query
    response = agent_executor.invoke(
        {
            "query": agent_state["query"],
            "agent_scratchpad": [],
        }
    )
    return response["output"]


__all__ = [run_research_agent]
