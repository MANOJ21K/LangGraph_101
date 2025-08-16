This Jupyter Notebook demonstrates how to build a parallel workflow using [LangGraph](https://langchain-ai.github.io/langgraph/) for calculating cricket batsman statistics. The workflow computes multiple metrics in parallel and then summarizes the results.

## Overview

- **LangGraph** is a Python library for building stateful, composable, and parallelizable workflows.
- This notebook showcases how to define a custom state, create parallel nodes, and aggregate their results using LangGraph.

## Features

- **Parallel Node Execution:** Calculates Strike Rate, Balls Per Boundary, and Boundary Percentage in parallel.
- **State Management:** Uses a TypedDict (`BatsmanState`) to manage and pass state between nodes.
- **Graph Visualization:** Visualizes the workflow graph.
- **Summary Generation:** Aggregates all computed metrics into a human-readable summary.

## Workflow Steps

1. **Define State:**  
    A `TypedDict` called `BatsmanState` holds all relevant batsman statistics.

2. **Node Functions:**  
    - `calculate_sr`: Computes the strike rate.
    - `calculate_bpb`: Computes balls per boundary.
    - `calculate_boundary_percentage`: Computes boundary percentage.
    - `summary`: Aggregates all metrics into a summary string.

3. **Graph Construction:**  
    - Nodes are added to the graph.
    - Edges are defined so that the three calculation nodes run in parallel from the `START` node, and all feed into the `summary` node, which then leads to `END`.

4. **Graph Compilation & Visualization:**  
    - The graph is compiled into a workflow.
    - The workflow graph is visualized using Mermaid.

5. **Execution:**  
    - The workflow is invoked with an initial state (sample batsman stats).
    - The output is a summary of the batsman's performance.

## Usage

1. **Install LangGraph:**
    ```bash
    pip install langgraph
    ```

2. **Run the Notebook:**
    - Execute each cell in order.
    - The workflow will process the initial state and output a summary.

3. **Customize:**
    - Modify the `initial_state` dictionary to analyze different batsman statistics.

## Example Output

After running the workflow with the provided `initial_state`: