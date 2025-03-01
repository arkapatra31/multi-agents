from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

prompt_template = ChatPromptTemplate.from_template(
    template="""
                    You will be provided a Python question. Return only the code to solve the problem. Here is the question: {question}
                    """
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

chain = prompt_template | llm

response = chain.invoke(
    {
        "question": "**Question:** Write a Python function that takes a list of numbers and returns the sum of all the even numbers in the list."
    }
)

print(response.content)
