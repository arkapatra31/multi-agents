from multi_agent_langgraph.orchestrator import run_orchestrator


if __name__ == "__main__":
    app = run_orchestrator()
    result = app.invoke({"query": "Find a simple Python problem from LeetCode"})
    print(result)
