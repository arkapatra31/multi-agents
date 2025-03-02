from multi_agent_langgraph.orchestrator import run_orchestrator


if __name__ == "__main__":
    app = run_orchestrator()
    result = app.invoke({"query": "Show me NSE index changes in last 10 days"})
    print(result)
