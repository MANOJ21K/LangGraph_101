# LangGraph 101

A hands-on guide to **[LangGraph](https://langchain-ai.github.io/langgraph/)** — the framework for building stateful, multi-actor LLM applications. Each module is a self-contained example that builds intuition for a different graph pattern, plus a working chatbot app you can run end-to-end.

## What's inside

| Module | What it covers |
|---|---|
| [`sequential_workflow/`](sequential_workflow) | The simplest graph: nodes that run one after another. The "hello world" of LangGraph. |
| [`parallel_workflow/`](parallel_workflow) | Fan-out / fan-in patterns — running multiple nodes concurrently and merging their results. |
| [`conditional_workflow/`](conditional_workflow) | Branching with conditional edges based on graph state. |
| [`Iterative_workflow/`](Iterative_workflow) | Loops, retries, and self-correcting agents. The pattern behind reflection and actor–critic setups. |
| [`chatbot/`](chatbot) | Stateful chatbots — with and without memory, plus threads and checkpointers for persistence. |
| [`chatbot_app/`](chatbot_app) | A full-stack chatbot app (backend + frontend) putting the concepts together. |

## Who this is for

Engineers comfortable with Python and LangChain who want a concrete, runnable tour of LangGraph's core abstractions before building production agents. Each notebook stands alone — start with `sequential_workflow` and work your way down the table.

## Setup

```bash
git clone https://github.com/MANOJ21K/LangGraph_101.git
cd LangGraph_101
pip install langgraph langchain langchain-openai jupyter
```

Set your `OPENAI_API_KEY` (or whichever model provider each notebook uses) and open the `.ipynb` files in Jupyter or VS Code.

## License

MIT
