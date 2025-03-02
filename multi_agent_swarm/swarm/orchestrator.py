from typing import TypedDict

from multi_agent_swarm.flight_search_agent import run_flight_agent
from multi_agent_swarm.hotel_search_agent import run_hotel_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_swarm


def run_orchestrator():

    workflow = create_swarm(
        [run_flight_agent(), run_hotel_agent()], default_active_agent="flight_agent"
    )

    app = workflow.compile(checkpointer=InMemorySaver())

    return app


__all__ = [run_orchestrator]
