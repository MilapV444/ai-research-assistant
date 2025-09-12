# main.py

from research_agent.graph import build_graph

def run_cli():
    app = build_graph()
    print("🤖 Research Assistant ready! (type 'exit' to quit)\n")

    state = {"query": "", "history": []}

    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        state["query"] = query
        result = app.invoke(state)

        print(f"Assistant: {result['final_answer']}\n")

if __name__ == "__main__":
    run_cli()