from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import  ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from .python_tool import python_tool


load_dotenv()


def run_python_agent(question: str):

    system_prompt = SystemMessagePromptTemplate.from_template(
        template= """
                        You are a Python code generator. Your task is to generate a Python code to solve the problem.
                        Sometimes you might be provided with data which needs to be represented visually using graphs or charts
                        """
    )

    human_prompt = HumanMessagePromptTemplate.from_template(
        template= """
                        Here is the problem: {question}.
                        Return the Python code to solve the problem and visualize the data if needed.
                        Once you are done, please return the final output.
                        Write down your thoughts and reasoning in the {agent_scratchpad}.
                        """
    )

    # Create the prompt template with system message, human message, and agent_scratchpad
    prompt_template = ChatPromptTemplate.from_messages(
        [
            system_prompt,
            human_prompt
        ]
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

    tools = [python_tool]

    agent = create_tool_calling_agent(llm, tools, prompt_template)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response = agent_executor.invoke(
        {
            "question": question,
            "agent_scratchpad": []
        }
    )

    return response["output"]


__all__ = [run_python_agent]
