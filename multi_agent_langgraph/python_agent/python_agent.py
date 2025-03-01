from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import create_tool_calling_agent, AgentExecutor
from .python_tool import python_tool


load_dotenv()


def run_python_agent(question: str):
    # Create the prompt template with system message, human message, and agent_scratchpad
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Python code generator. Your task is to generate a Python code to solve the problem.",
            ),
            ("human", "Here is the problem: {question}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

    tools = [python_tool]

    agent = create_tool_calling_agent(llm, tools, prompt_template)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response = agent_executor.invoke(
        {
            "question": question,
            "agent_scratchpad": [],
        }
    )

    return response["output"]


__all__ = [run_python_agent]
