from typing import TypedDict
from langgraph.graph import StateGraph
from multi_agent_langgraph.python_agent import run_python_agent
from multi_agent_langgraph.research_agent import run_research_agent


def research_python_problem(agent_state):
    research_agent_output = run_research_agent(agent_state)
    return {"question": research_agent_output}


def generate_python_code(agent_state):
    python_agent_output = run_python_agent(agent_state["question"])
    return {"python_code": python_agent_output}


def run_orchestrator():
    class AgentState(TypedDict):
        query: str
        question: str
        python_code: str

    agent_workflow = StateGraph(AgentState)

    # Add the nodes to the workflow
    agent_workflow.add_node("research_agent", research_python_problem)
    agent_workflow.add_node("python_agent", generate_python_code)

    # Set the entry point
    agent_workflow.set_entry_point("research_agent")

    # Add the edges to the workflow
    agent_workflow.add_edge("research_agent", "python_agent")
    agent_workflow.set_finish_point("python_agent")

    return agent_workflow.compile()


__all__ = [run_orchestrator]
