from swarm.orchestrator import run_orchestrator

if __name__ == "__main__":
    app = run_orchestrator()
    result = app.invoke({"query": "I want to go to Hyderabad on 10th March"})
    print(result)
