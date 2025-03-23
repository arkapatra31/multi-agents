import os
import uuid
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from IPython.display import Image, display

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)


def add(agent_state):
    prompt = PromptTemplate.from_template(
        template="""Return the sum of {num1} and {num2}"""
    )
    chain = prompt | llm
    response = chain.invoke(
        {"num1": agent_state["num1"], "num2": agent_state["num2"]}
    ).content
    return {"addition": str(response)}


def review(agent_state):
    approval = interrupt(
        {
            "question": "Do you approve the addition result?",
            "addition": agent_state["addition"],
        }
    )
    if approval == "yes":
        return {"next": "finalize"}
    else:
        return {"next": "add"}


def finalize(agent_state):
    response = agent_state["addition"]
    return {"final_result": response}


def orchestrate():
    class AgentState(TypedDict):
        num1: int
        num2: int
        addition: str  # Change to str since it stores text
        final_result: str

    graph = StateGraph(AgentState)

    graph.add_node("add", add)
    graph.add_node("reviewal", review)
    graph.add_node("finalize", finalize)

    graph.set_entry_point("add")
    graph.add_edge("add", "reviewal")
    graph.add_conditional_edges(
        "reviewal", lambda x: x["next"], {"finalize": "finalize", "add": "add"}
    )
    graph.set_finish_point("finalize")

    checkpointer = InMemorySaver()

    return graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    app = orchestrate()
    display(Image(app.get_graph().draw_mermaid_png()))
    u_id = str(uuid.uuid4())
    thread_config = {"configurable": {"thread_id": u_id}}
    result = app.invoke(input={"num1": 5, "num2": 3}, config=thread_config)

    print(result["addition"])
    state = app.get_state(thread_config)
    print("################## State ##################")
    print(state)
    print("################## State Tasks ##################")
    print(state.tasks)
    print("################## Task Interrupts ##################")
    print(state.tasks[0].interrupts)

    print("\n\n\n\n\n")
    print("################## Resume Graph ##################")
    response = app.invoke(
        Command(
            resume=input(
                "Human Input Validation - Do you approve the addition result? (yes/no) \t"
            )
        ),
        config=thread_config,
    )
    print(response)

    print("################## State ##################")
    state = app.get_state(thread_config)
    print(state)
    print("################## State Tasks ##################")
    print(state.tasks)
    print("################## Task Interrupts ##################")
    print(state.tasks[0].interrupts if state.tasks else "No interrupts")
