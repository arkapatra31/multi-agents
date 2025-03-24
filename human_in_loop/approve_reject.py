import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from IPython.display import Image, display

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def add(agent_state):
    prompt = PromptTemplate.from_template(
        template="""Calculate and return only the numeric sum of {num1} and {num2} as a plain number, without any text."""
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
    response = f"Approved result: {agent_state['addition']}"
    return {"final_result": response}


def orchestrate():
    class AgentState(TypedDict):
        num1: int
        num2: int
        addition: str
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

    checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    app = orchestrate()
    display(Image(app.get_graph().draw_mermaid_png()))
    config = {"configurable": {"thread_id": "556467783abc"}}

    # Initialize input
    state_input = {"num1": 7, "num2": 4}

    while True:
        stream = app.stream(state_input, config, stream_mode="values")
        for event in stream:
            print(f"Current Event: {event}")
            print(
                f"State.next: {app.get_state(config).next}"
            )  # Debug state transitions

        # After stream completes, check the state
        state = app.get_state(config)
        print(f"Final State.next: {state.next}")

        if state.tasks and state.tasks[0].interrupts:  # Interrupt detected
            interrupt_data = state.tasks[0].interrupts[0].value
            print(f"Interrupt detected: {interrupt_data}")
            user_response = input(f"{interrupt_data['question']} (yes/no): ")
            state_input = Command(resume=user_response)
        elif state.next == ():
            print("Graph execution completed successfully.")
            print(app.get_state(config=config))
            print(app.get_state(config=config).values["final_result"])
            break
        elif state.next == ("add",):
            print("Looping back to 'add' due to 'no' response.")
            state_input = None  # Continue from current state
        else:
            print(f"Unexpected state with next: {state.next}, breaking.")
            break
