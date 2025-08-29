from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
# for memory management
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    user_input: str
    response: str
    messages: Annotated[list[BaseMessage], add_messages]  # Changed from chat_history to messages

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
    
    # Get previous messages from state
    previous_messages = state.get('messages', [])
    
    # Create the conversation context
    # Start with system message
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    # Add previous messages in the correct format
    for msg in previous_messages:
        if isinstance(msg, HumanMessage):
            conversation.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            conversation.append({"role": "assistant", "content": msg.content})
    
    # Add current user input
    conversation.append({"role": "user", "content": user_input})
    
    # Get response from LLM
    response = llm.invoke(conversation)
    
    # Return state with new messages added
    # The add_messages reducer will automatically handle adding the new messages
    return {
        "user_input": user_input,
        "response": response.content,
        "messages": [
            HumanMessage(content=user_input),
            AIMessage(content=response.content)
        ]
    }

# Create the workflow
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

checkpointer = MemorySaver()
workflow = graph.compile(checkpointer=checkpointer)