from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
# for memory management
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    user_input: str
    response: str
    chat_history: Annotated[list[BaseMessage], add_messages]

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_node(state: ChatState) -> ChatState:
    user_input = state['user_input']
    
    previous_chat_history = state.get('chat_history', [])
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"""Here is the previous chat history: {previous_chat_history} and
                            This is the current user input: {user_input}""",
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    
    response = chat_completion.choices[0].message.content
    state['response'] = response
    state['chat_history'].append(HumanMessage(content=user_input))
    state['chat_history'].append(AIMessage(content=response))
    return state

# Create the workflow
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

checkpointer = MemorySaver()
workflow = graph.compile(checkpointer=checkpointer)

def run_chat_loop():
    """Function to run the command-line chat loop"""
    thread_id = '1'
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting the chatbot.")
            break
        
        initial_state = {
            'user_input': user_input
        }
        
        config = {'configurable': {'thread_id': thread_id}}
        result = workflow.invoke(initial_state, config=config)
        response = result['response']
        print(f"User: {user_input}")
        print(f"Assistant: {response}")

# Only run the chat loop if this file is executed directly
if __name__ == "__main__":
    run_chat_loop()