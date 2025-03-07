from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from .flight_tool import search_flights_tool
from langchain.agents import create_tool_calling_agent
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool
from .output_parser import flight_output_parser

load_dotenv()


def run_flight_agent():
    system_prompt = SystemMessagePromptTemplate.from_template(
        template="""
                    You are a travel agent. Your task is to search for the best flight options based on the user's query.
                    You have access to a flight search tool 'search_flight_tool' that can help you find the best options.
                    USAGE: Execute the tool once and return the results. Do not execute the tool multiple times.
        """
    )

    human_prompt = HumanMessagePromptTemplate.from_template(
        template="""
                        I would like you to find flight from Kolkata
                        Once you have the results, please return them in JSON format
                        Write down your thought process and reasoning behind the results in the {agent_scratchpad}
        """
    )

    prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

    agent = create_react_agent(
        llm,
        [
            search_flights_tool,
            create_handoff_tool(
                agent_name="hotel_agent",
                description="Transfer to hotel_agent, it can help with hotel search",
            ),
        ],
        prompt="""
                         I would like you to find {user_query}.
                        Once you have the results, please return them in the following format
        """,
        name="flight_agent",
    )

    return agent


__all__ = [run_flight_agent]
