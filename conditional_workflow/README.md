This notebook demonstrates how to build a conditional workflow using [LangGraph](https://github.com/langchain-ai/langgraph).

## Overview

A conditional workflow allows you to define different execution paths based on the state or data at runtime. In this example, we classify a number as even or odd using a simple state machine.

## Key Components

- **State Definition**: We use a `TypedDict` to define the state structure.
- **Nodes**: Each node is a function that processes the state.
- **Conditional Edges**: The workflow branches based on the result of a function (`number_classify`), directing the flow to either the `even_action` or `odd_action` node.

## Workflow Steps

1. **Check Number**: Ensures the number is non-negative.
2. **Classify Number**: Determines if the number is even or odd.
3. **Even/Odd Action**: Updates the state with a message indicating if the number is even or odd.
4. **End**: The workflow terminates.