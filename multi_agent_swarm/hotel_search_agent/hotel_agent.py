from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from .hotel_tool import search_hotels_tool
from langchain.agents import create_tool_calling_agent
from langgraph_swarm import create_handoff_tool
from .output_parser import hotel_output_parser

load_dotenv()


def run_hotel_agent(user_query: str):
    system_prompt = SystemMessagePromptTemplate.from_template(
        template="""
                    You are a travel agent. Your task is to search for the best hotel options based on the user's query.
                    You have access to a hotel search tool 'search_hotel_tool' that can help you find the best options.
                    USAGE: Execute the tool once and return the results. Do not execute the tool multiple times.
        """
    )

    human_prompt = HumanMessagePromptTemplate.from_template(
        template="""
                        I would like you to find {user_query}.
                        Once you have the results, please return them in the following format:
                        {hotel_output_parser}
        """
    )

    prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

    tools = [
        search_hotels_tool,
        create_handoff_tool(
            agent_name="hotel_agent",
            description="A travel agent that can search for hotels.",
        ),
    ]

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt_template,
        message_formatter=hotel_output_parser.get_format_instructions(),
    )

    return agent


__all__ = [run_hotel_agent]
