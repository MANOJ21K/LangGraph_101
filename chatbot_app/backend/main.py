from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
# for memory management
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

class ChatState(TypedDict):
    user_input: str
    response: str
    chat_history: Annotated[list[BaseMessage], add_messages]

from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    streaming=True
)

def chat_node(state: ChatState) -> ChatState:
    user_input = state['user_input']
    
    previous_chat_history = state.get('chat_history', [])
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
        ]

    response = llm.invoke(messages)

    # update state after streaming
    state["response"] = response
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

