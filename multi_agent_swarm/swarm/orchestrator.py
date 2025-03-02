from multi_agent_swarm.flight_search_agent import run_flight_agent
from multi_agent_swarm.hotel_search_agent import run_hotel_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_swarm


def run_orchestrator():
    # flight_agent = run_flight_agent()
    # hotel_agent = run_hotel_agent()

    workflow = create_swarm(
       agents=[run_flight_agent.__name__, run_hotel_agent.__name__],
         default_active_agent="run_flight_agent"
    )

    app = workflow.compile()

    return app


__all__ = [run_orchestrator]
