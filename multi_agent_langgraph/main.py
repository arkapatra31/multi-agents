from multi_agent_langgraph.orchestrator import run_orchestrator


if __name__ == "__main__":
    app = run_orchestrator()
    result = app.invoke({"query": "Show me India's GDP growth rate for last 5 years"})
    print(result)
