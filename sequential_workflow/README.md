This notebook demonstrates how to use [LangGraph](https://github.com/langchain-ai/langgraph) to build a simple sequential workflow for calculating BMI (Body Mass Index).

## What does this notebook do?

- **Defines a state** using Python's `TypedDict` to hold weight, height, and BMI.
- **Implements a function** to calculate BMI from weight and height.
- **Builds a LangGraph workflow** with a single calculation node.
- **Executes the workflow** with sample data.

---

## Step-by-step Walkthrough

1. **Install LangGraph**  
   Uncomment and run:
   ```python
   # !pip install langgraph
   ```

2. **Import dependencies**  
   - `StateGraph`, `START`, `END` from `langgraph.graph`
   - `TypedDict` from `typing`

3. **Define the State**  
   ```python
   class BMIState(TypedDict):
       weight_kg: float
       height_m: float
       bmi: float
   ```

4. **Create the Calculation Function**  
   ```python
   def calculating_bmi(state: BMIState) -> BMIState:
       weight = state['weight_kg']
       height = state['height_m']
       bmi = weight / (height ** 2)
       state['bmi'] = round(bmi, 2)
       return state
   ```

5. **Build the Graph**  
   - Initialize:  
     ```python
     graph = StateGraph(BMIState)
     ```
   - Add node:  
     ```python
     graph.add_node('calculate_bmi', calculating_bmi)
     ```
   - Add edges:  
     ```python
     graph.add_edge(START, 'calculate_bmi')
     graph.add_edge('calculate_bmi', END)
     ```

6. **Compile and Run**  
   ```python
   workflow = graph.compile()
   initial_state = {'weight_kg': 72, 'height_m': 1.75}
   final_state = workflow.invoke(initial_state)
   print(final_state)
   # Output: {'weight_kg': 72, 'height_m': 1.75, 'bmi': 23.51}
   ```

---

## Why is this useful?

- Shows how to use LangGraph for simple, stateful workflows.
- Demonstrates the basics of graph-based computation in Python.
- Easy to extend: add more nodes for more complex calculations!

---

## Tips

- Change the `initial_state` values to try different weights/heights.
- Add more nodes to the graph for additional processing steps.
- Check out the [LangGraph documentation](https://github.com/langchain-ai/langgraph) for advanced features.

---

Happy coding!