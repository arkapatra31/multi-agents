from multi_agent_langgraph.orchestrator import run_orchestrator


if __name__ == "__main__":
    app = run_orchestrator()
    result = app.invoke({"query": "Show me the income taxes paid in India over last 5 years"})
    print(result)
