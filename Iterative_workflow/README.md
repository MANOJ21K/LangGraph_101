# Iterative Flow with LangGraph

This Jupyter Notebook demonstrates how to use the [LangGraph](https://github.com/langchain-ai/langgraph) library to build and execute an iterative workflow using a state machine approach.

## Overview

The notebook defines a simple iterative process:
- Start with an initial state containing a number.
- Print the current number.
- Decrement the number.
- Repeat the process until the number reaches zero or below.
- Mark the process as finished.

## Key Components

- **State Definition**: The state is defined using a `TypedDict` with fields for the current number and a result string.
- **Nodes**: Functions (`print_number`, `decrement`) represent steps in the workflow.
- **Conditional Logic**: The `check_number` function determines whether to continue iterating or finish.
- **Graph Construction**: Nodes and conditional edges are added to the `StateGraph` to define the flow.
- **Execution**: The workflow is compiled and invoked with an initial state.

## Flow Diagram

The workflow can be visualized as a directed graph:
1. **START** → Print Number → Decrement → [Check Number]
2. If number > 0: loop back to Print Number.
3. If number <= 0: transition to END (Finished).

## Usage

- Modify the `initial_state` to change the starting number.
- Run the notebook cells to see the iterative process in action.
- The graph visualization cell provides a diagram of the workflow.

## Requirements

- `langgraph`
- `IPython` (for visualization)

---

This notebook serves as a template for building more complex iterative or conditional workflows using LangGraph.