from swarm.orchestrator import run_orchestrator

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1", "user_id": "1"}}
    app = run_orchestrator()
    result = app.invoke(
        {"user_query": "I want to go to Hyderabad on 10th March"},
        config
    )
    print(result)
