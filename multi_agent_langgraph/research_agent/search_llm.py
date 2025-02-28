import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

prompt_template = ChatPromptTemplate.from_template(
    template= """ Search some a simple problem in Python and return the question only"""
)

llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0,
    verbose= True
)

chain = prompt_template | llm

response = chain.invoke(
    {
        "input": "Search some a simple problem in Python"
    }
)

print(response.content)

